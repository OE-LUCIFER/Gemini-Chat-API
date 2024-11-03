import requests
import json
import re
from typing import Optional, Dict
from fake_useragent import UserAgent

class GeminiConversation:
    def __init__(self):
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""

class Gemini:
    def __init__(self, cookie_path: str, timeout: int = 30):
        """
        Initializes the Gemini client with the provided cookie.

        Args:
            cookie_path (str): Path to the cookie JSON file
            timeout (int, optional): Request timeout in seconds. Defaults to 30
        """
        self.session_auth1, self.session_auth2 = self._load_cookies(cookie_path)
        self.session = self._init_session()
        self.SNlM0e = self._get_snlm0e()
        self.conversations: Dict[str, GeminiConversation] = {}
        self.timeout = timeout
        self.current_conversation = None

    def _init_session(self) -> requests.Session:
        """Initialize and configure requests session"""
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Host": "gemini.google.com",
            "Origin": "https://gemini.google.com",
            "Referer": "https://gemini.google.com/",
            "User-Agent": UserAgent().random,
            "X-Same-Domain": "1",
        })
        session.cookies.set("__Secure-1PSID", self.session_auth1)
        session.cookies.set("__Secure-1PSIDTS", self.session_auth2)
        return session

    @staticmethod
    def _load_cookies(cookie_path: str) -> tuple:
        """
        Load cookies from the provided JSON file.

        Args:
            cookie_path (str): Path to the cookie JSON file

        Returns:
            tuple: (__Secure-1PSID, __Secure-1PSIDTS) values
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

    def _get_snlm0e(self) -> str:
        """Get the SNlM0e value required for Gemini requests"""
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

    def create_conversation(self, conversation_name: str = None) -> str:
        """
        Create a new conversation.

        Args:
            conversation_name (str, optional): Name for the conversation. 
                If None, generates a unique name.

        Returns:
            str: Conversation name
        """
        if conversation_name is None:
            conversation_name = f"conversation_{len(self.conversations) + 1}"
        
        if conversation_name in self.conversations:
            raise ValueError(f"Conversation '{conversation_name}' already exists")
        
        self.conversations[conversation_name] = GeminiConversation()
        self.current_conversation = conversation_name
        return conversation_name

    def switch_conversation(self, conversation_name: str) -> None:
        """
        Switch to a different conversation.

        Args:
            conversation_name (str): Name of the conversation to switch to
        """
        if conversation_name not in self.conversations:
            raise ValueError(f"Conversation '{conversation_name}' does not exist")
        self.current_conversation = conversation_name

    def list_conversations(self) -> list:
        """List all available conversations"""
        return list(self.conversations.keys())

    def delete_conversation(self, conversation_name: str) -> None:
        """
        Delete a conversation.

        Args:
            conversation_name (str): Name of the conversation to delete
        """
        if conversation_name not in self.conversations:
            raise ValueError(f"Conversation '{conversation_name}' does not exist")
        
        del self.conversations[conversation_name]
        if self.current_conversation == conversation_name:
            self.current_conversation = None if not self.conversations else next(iter(self.conversations))

    def ask(self, question: str, conversation_name: str = None) -> Optional[dict]:
        """
        Send a question to Gemini and get the response.

        Args:
            question (str): The question to ask
            conversation_name (str, optional): Name of the conversation to use. 
                If None, uses current conversation

        Returns:
            Optional[dict]: Response containing content and images
        """
        if conversation_name:
            self.switch_conversation(conversation_name)
        elif not self.current_conversation:
            self.create_conversation()

        conv = self.conversations[self.current_conversation]

        try:
            params = {
                "bl": "boq_assistant-bard-web-server_20230713.13_p0",
                "_reqid": "0",
                "rt": "c",
            }

            message_struct = [
                [question],
                None,
                [conv.conversation_id, conv.response_id, conv.choice_id],
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
            
            chat_data = json.loads(response.content.splitlines()[3])[0][2]
            if not chat_data:
                return {"content": None, "images": []}

            json_chat_data = json.loads(chat_data)
            images = []
            if len(json_chat_data) >= 3 and len(json_chat_data[4][0]) >= 4 and json_chat_data[4][0][4]:
                for img_data in json_chat_data[4][0][4]:
                    try:
                        images.append(img_data[0][0][0])
                    except (IndexError, TypeError):
                        continue

            results = {
                "content": json_chat_data[4][0][1][0] if len(json_chat_data[4][0][1]) > 0 else None,
                "conversation_id": json_chat_data[1][0],
                "response_id": json_chat_data[1][1],
                "images": images,
            }

            # Update conversation state
            conv.conversation_id = results["conversation_id"]
            conv.response_id = results["response_id"]
            conv.choice_id = json_chat_data[4][0][0] if len(json_chat_data[4][0]) > 0 else ""

            return results

        except Exception as e:
            return {"content": f"Error: {str(e)}", "images": []}

def main():
    """Example usage of the Gemini client"""
    gemini = Gemini('cookie.json')
    
    # Create a few conversations
    gemini.create_conversation("daily_chat")
    # gemini.create_conversation("coding_help")
    
    print("Available conversations:", gemini.list_conversations())

    # Show current conversation
    print(f"\nCurrent conversation: {gemini.current_conversation}")
    print("\nCommands:")
    print("  /switch <name> - Switch to a different conversation")
    print("  /new <name> - Create a new conversation")
    print("  /list - List all conversations")
    print("  /delete <name> - Delete a conversation")
    print("  /quit - Exit the program")

    # Chat in different conversations
    while True:
        try:          
            user_input = input("\n>>> ")
            
            # Handle commands
            if user_input.startswith('/'):
                cmd_parts = user_input.split()
                cmd = cmd_parts[0].lower()
                
                if cmd == '/switch' and len(cmd_parts) > 1:
                    gemini.switch_conversation(cmd_parts[1])
                elif cmd == '/new' and len(cmd_parts) > 1:
                    gemini.create_conversation(cmd_parts[1])
                elif cmd == '/list':
                    print("Conversations:", gemini.list_conversations())
                elif cmd == '/delete' and len(cmd_parts) > 1:
                    gemini.delete_conversation(cmd_parts[1])
                elif cmd == '/quit':
                    break
                else:
                    print("Invalid command")
                continue
            
            # Send message and get response
            response = gemini.ask(user_input)
            if response and response["content"]:
                print("\nGemini:", response["content"])
                if response["images"]:
                    print("\nImages:", response["images"])
            else:
                print("\nNo response received")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
