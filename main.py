import requests
import json
import re
from typing import Optional
from fake_useragent import UserAgent

class Gemini:
    def __init__(self, cookie_path: str):
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

    def ask(self, question: str, sys_prompt: str = "") -> Optional[str]:
        """
        Sends a question to the Gemini model and retrieves the answer.

        :param question: The question to ask.
        :param sys_prompt: System prompt (not used in Gemini, kept for compatibility).
        :return: The model's answer or None if the request fails.
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
            )
            response.raise_for_status()
            
            chat_data = json.loads(response.content.splitlines()[3])[0][2]
            if not chat_data:
                return None
            
            json_chat_data = json.loads(chat_data)
            content = json_chat_data[4][0][1][0]
            
            self.conversation_id = json_chat_data[1][0]
            self.response_id = json_chat_data[1][1]
            self.choice_id = json_chat_data[4][0][0]
            
            return content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    gemini = Gemini('cookie.json')
    response = gemini.ask(input(">>> "))
    for chunk in response:
        print(chunk, end="", flush=True)
