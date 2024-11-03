# 🌟 Gemini Python API

<div align="center">

![Gemini API](https://img.shields.io/badge/Gemini-API-blue?style=for-the-badge&logo=google)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

*An unofficial Python client for interacting with Google's Gemini chat model* 🚀

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

## ✨ Features

- 🔐 Cookie-based authentication
- 🔄 Session management with automatic cookie handling
- 🌐 Support for conversation context
- 🖼️ Image extraction from responses
- 🔧 Customizable timeout settings
- 🎭 Random User-Agent generation
- 🔄 Conversation tracking with IDs

## 📋 Requirements

- Python 3.6+
- `requests`
- `fake-useragent`
- Google account with access to Gemini

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gemini-python-api.git
cd gemini-python-api
```

2. **Install dependencies**
```bash
pip install requests fake-useragent
```

3. **Cookie Setup** 🍪

Install the Cookie-Editor extension:
- [Chrome Extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
- [Edge Extension](https://microsoftedge.microsoft.com/addons/detail/cookie-editor/neaplmfkghagebokkhpjpoebhdledlfi)

To export your cookies:
1. Visit [gemini.google.com](https://gemini.google.com/)
2. Open Cookie-Editor
3. Click "Export" (This will copy cookies to clipboard)
4. Create `cookie.json` in your project directory
5. Paste the exported cookies into `cookie.json`

## 🚀 Quick Start

```python
from gemini import Gemini

# Initialize with cookie file
gemini = Gemini('cookie.json')

# Send a simple message
response = gemini.ask("Hello, Gemini!")
print(response["content"])
```

## 📖 Documentation

### Gemini Class

```python
class Gemini:
    def __init__(self, cookie_path: str, timeout: int = 30)
```

#### Parameters:
- `cookie_path`: Path to the JSON file containing cookies
- `timeout`: Request timeout in seconds (default: 30)

### Methods

#### `ask(question: str, sys_prompt: str = "") -> Optional[dict]`

Sends a question to Gemini and returns the response.

**Parameters:**
- `question`: The message to send
- `sys_prompt`: System prompt (not used, kept for compatibility)

**Returns:**
```python
{
    "content": str,          # The response text
    "conversation_id": str,  # Conversation identifier
    "response_id": str,      # Response identifier
    "images": List[str]      # List of image URLs (if any)
}
```

### Response Structure

The response dictionary contains:
- `content`: The main text response
- `conversation_id`: ID for tracking the conversation
- `response_id`: ID for the specific response
- `images`: List of image URLs (if present in the response)

## 🔍 Error Handling

The API handles several types of errors:
- Cookie file not found
- Invalid JSON format in cookie file
- Missing required cookies
- Network request failures
- Response parsing errors

## ⚠️ Important Notes

1. **Cookie Management**
   - Cookies must contain `__Secure-1PSID` and `__Secure-1PSIDTS`
   - Keep your cookies secure and don't share them
   - Update cookies if they expire

2. **Rate Limiting**
   - Implement appropriate rate limiting in your applications
   - Monitor response status for API limitations

3. **Session Management**
   - Each instance maintains its own session
   - Conversations are tracked using IDs

## 🤖 Example Usage

### Basic Conversation
```python
gemini = Gemini('cookie.json')
response = gemini.ask("What is quantum computing?")
print(response["content"])
```

### With Custom Timeout
```python
gemini = Gemini('cookie.json', timeout=60)
response = gemini.ask("Can you explain machine learning?")
print(response["content"])
```

### Handling Images in Response
```python
gemini = Gemini('cookie.json')
response = gemini.ask("Show me an example of a neural network")
print(response["content"])
for image_url in response["images"]:
    print(f"Image URL: {image_url}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">

## ⭐ Support

If you found this project helpful, give it a star!

[Report Bug](https://github.com/OE-LUCIFER/Gemini-Chat-API/issues) • [Request Feature](https://github.com/OE-LUCIFER/Gemini-Chat-API/issues)

</div>

---

<div align="center">

Made with ❤️ by Vortex for the AI community

</div>
