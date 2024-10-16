import requests
import json
import re
from typing import Optional, List
from fake_useragent import UserAgent

class Gemini:
    def __init__(self, cookie_path: str, timeout: int = 30):
        """
        Initializes the Gemini client with the provided cookie.

        :param cookie_path: Path to the cookie JSON file.
        """
        self.session_auth1, self.session_auth2 = self.load_cookies(cookie_path)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Host": "gemini.google.com",
            "Origin": "https://gemini.google.com",
            "Referer": "https://gemini.google.com/",
            "User-Agent": UserAgent().random,
            "X-Same-Domain": "1",
        })
        self.session.cookies.set("__Secure-1PSID", self.session_auth1)
        self.session.cookies.set("__Secure-1PSIDTS", self.session_auth2)
        self.SNlM0e = self.get_snlm0e()
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""
        self.timeout = timeout

    @staticmethod
    def load_cookies(cookie_path: str) -> tuple:
        """
        Loads cookies from the provided JSON file.

        :param cookie_path: Path to the cookie JSON file.
        :return: Tuple containing __Secure-1PSID and __Secure-1PSIDTS values.
        """
        try:
            with open(cookie_path, 'r') as file:
                cookies = json.load(file)
            session_auth1 = next(item['value'] for item in cookies if item['name'] == '__Secure-1PSID')
            session_auth2 = next(item['value'] for item in cookies if item['name'] == '__Secure-1PSIDTS')
            return session_auth1, session_auth2
        except FileNotFoundError:
            raise Exception(f"Cookie file not found at path: {cookie_path}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format in the cookie file.")
        except StopIteration:
            raise Exception("Required cookies not found in the cookie file.")

    def get_snlm0e(self) -> str:
        """
        Retrieves the SNlM0e value required for Gemini requests.

        :return: SNlM0e value.
        """
        try:
            resp = self.session.get(
                "https://gemini.google.com/app",
                timeout=10,
            )
            resp.raise_for_status()
            SNlM0e = re.search(r'"SNlM0e":"(.*?)"', resp.text)
            if not SNlM0e:
                raise Exception("SNlM0e value not found in response.")
            return SNlM0e.group(1)
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve SNlM0e: {e}")

    def ask(self, question: str, sys_prompt: str = "") -> Optional[dict]:
        """
        Sends a question to the Gemini model and retrieves the answer, including images.

        :param question: The question to ask.
        :param sys_prompt: System prompt (not used in Gemini, kept for compatibility).
        :return: A dictionary containing the model's answer and a list of images, or None if the request fails.
        """
        try:
            params = {
                "bl": "boq_assistant-bard-web-server_20230713.13_p0",
                "_reqid": "0",
                "rt": "c",
            }

            message_struct = [
                [question],
                None,
                [self.conversation_id, self.response_id, self.choice_id],
            ]

            data = {
                "f.req": json.dumps([None, json.dumps(message_struct)]),
                "at": self.SNlM0e,
            }

            response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                params=params,
                data=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            try:
                chat_data = json.loads(response.content.splitlines()[3])[0][2]
            except (IndexError, json.JSONDecodeError) as e:
                print(f"Error parsing response: {e}")
                return {"content": None, "images": []}

            if not chat_data:
                return {"content": None, "images": []}

            json_chat_data = json.loads(chat_data)
            images = []
            try:
                if len(json_chat_data) >= 3 and len(json_chat_data[4][0]) >= 4 and json_chat_data[4][0][4]:
                    for img_data in json_chat_data[4][0][4]:
                        try:
                            images.append(img_data[0][0][0])
                        except (IndexError, TypeError):
                            pass
            except (IndexError, TypeError) as e:
                print(f"Error extracting images from response: {e}")
                pass

            results = {
                "content": json_chat_data[4][0][1][0] if len(json_chat_data[4][0][1]) > 0 else None,
                "conversation_id": json_chat_data[1][0],
                "response_id": json_chat_data[1][1],
                "images": images,
            }
            self.conversation_id = results["conversation_id"]
            self.response_id = results["response_id"]
            self.choice_id = json_chat_data[4][0][0] if len(json_chat_data[4][0]) > 0 else ""

            return results
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {"content": None, "images": []}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"content": None, "images": []}

if __name__ == "__main__":
    gemini = Gemini('cookie.json')
    response = gemini.ask(input(">>> "))
    for chat in response["content"]:
        print(chat, end="", flush=True)
