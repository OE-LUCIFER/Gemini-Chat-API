<div align="center">

# 🌟 Gemini Python API

![Gemini API](https://img.shields.io/badge/Gemini-API-blue?style=for-the-badge&logo=google)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

[![GitHub stars](https://img.shields.io/github/stars/OE-LUCIFER/Gemini-Chat-API.svg?style=social&label=Star)](https://github.com/OE-LUCIFER/Gemini-Chat-API)
[![GitHub forks](https://img.shields.io/github/forks/OE-LUCIFER/Gemini-Chat-API.svg?style=social&label=Fork)](https://github.com/OE-LUCIFER/Gemini-Chat-API/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/OE-LUCIFER/Gemini-Chat-API.svg?style=social&label=Watch)](https://github.com/OE-LUCIFER/Gemini-Chat-API)

Unleash the power of Google's Gemini in your Python projects! 🚀

[Features](#-features-showcase) • [Installation](#%EF%B8%8F-installation--setup) • [Usage](#-quick-start-guide) • [Documentation](#-comprehensive-documentation) • [Contributing](#-contribution-guidelines)

</div>

<div align="center">

## 🌈 Features Showcase

</div>

<table align="center">
  <tr>
    <td align="center">🔐<br>Secure Authentication</td>
    <td align="center">🔄<br>Dynamic Sessions</td>
    <td align="center">💬<br>Multi-Conversation Support</td>
    <td align="center">🌐<br>Context Preservation</td>
  </tr>
  <tr>
    <td align="center">🖼️<br>Image Response Handling</td>
    <td align="center">⏱️<br>Customizable Timeouts</td>
    <td align="center">🎭<br>User-Agent Randomization</td>
    <td align="center">🔍<br>Conversation Tracking</td>
  </tr>
</table>

<div align="center">

## 🛠️ Installation & Setup

</div>

<details>
<summary><strong>Click to expand detailed setup instructions</strong></summary>

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/OE-LUCIFER/Gemini-Chat-API.git
   cd Gemini-Chat-API
   ```

2. **Set Up Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cookie Configuration:**
   - Install [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension
   - Visit [gemini.google.com](https://gemini.google.com/)
   - Export cookies and save as `cookie.json` in the project root

5. **Verify Installation:**
   ```bash
   python -c "from gemini import Gemini; print('Setup successful!')"
   ```

</details>

<div align="center">

## 🚀 Quick Start Guide

</div>

```python
from gemini import Gemini

# Initialize Gemini client
gemini = Gemini('cookie.json')

# Create a new conversation
chat = gemini.create_conversation("AI_Ethics")

# Ask a question
response = gemini.ask("What are the key ethical considerations in AI development?", chat)

print(f"Gemini says: {response['content']}")

# Handle image responses
if response['images']:
    print(f"Related images: {response['images']}")
```

<div align="center">

## 📘 Comprehensive Documentation

</div>

<details>
<summary><strong>Expand for API details and advanced usage</strong></summary>

### Gemini Class
```python
class Gemini:
    def __init__(self, cookie_path: str, timeout: int = 30)
```

### Core Methods
- `create_conversation(name: str) -> str`
- `switch_conversation(name: str) -> None`
- `list_conversations() -> list`
- `delete_conversation(name: str) -> None`
- `ask(question: str, conversation: str = None) -> dict`

### Advanced Usage Examples

#### Managing Multiple Conversations
```python
gemini.create_conversation("Science")
gemini.create_conversation("Philosophy")

gemini.switch_conversation("Science")
science_response = gemini.ask("Explain quantum entanglement")

gemini.switch_conversation("Philosophy")
philosophy_response = gemini.ask("Discuss the trolley problem")
```

#### Handling Image Responses
```python
response = gemini.ask("Show me a diagram of a black hole")
if response['images']:
    for img_url in response['images']:
        # Process or display the image
        print(f"Image URL: {img_url}")
```

For exhaustive method descriptions, usage scenarios, and best practices, refer to our [detailed API documentation](https://github.com/OE-LUCIFER/Gemini-Chat-API/wiki).

</details>

<div align="center">

## 🛡️ Error Handling & Reliability

</div>

Our robust error handling system ensures smooth operation:

- 🔒 Authentication Issues
- 🌐 Network Connectivity Problems
- ⏱️ Timeout Management
- 🧩 Response Parsing Errors

Implement try-except blocks for graceful error management in your applications.

<div align="center">

## 🔧 Configuration & Customization

</div>

Tailor the Gemini API to your needs:

- ⚙️ Adjust timeout settings
- 🔀 Implement custom conversation management
- 🎨 Extend functionality with additional methods

<div align="center">

## 📊 Performance Optimization

</div>

Tips for optimal performance:

- 🚀 Use async operations for concurrent requests
- 💾 Implement caching for frequent queries
- 🔍 Optimize conversation context management

<div align="center">

## 🤝 Contribution Guidelines

</div>

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 🖊️ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 🚀 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

Check out our [Contribution Guide](CONTRIBUTING.md) for more details.

<div align="center">

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

</div>

<div align="center">

## 💖 Support & Community

[![GitHub issues](https://img.shields.io/github/issues/OE-LUCIFER/Gemini-Chat-API.svg)](https://github.com/OE-LUCIFER/Gemini-Chat-API/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/OE-LUCIFER/Gemini-Chat-API.svg)](https://github.com/OE-LUCIFER/Gemini-Chat-API/pulls)

[Report a Bug](https://github.com/OE-LUCIFER/Gemini-Chat-API/issues/new?template=bug_report.md) • [Request a Feature](https://github.com/OE-LUCIFER/Gemini-Chat-API/issues/new?template=feature_request.md) • [Join our Discord](https://discord.gg/your-discord-link)

</div>

---

<div align="center">

<img src="https://img.shields.io/github/followers/OE-LUCIFER.svg?style=social&label=Follow" alt="Follow on GitHub">

Crafted with ❤️ by [OE-LUCIFER](https://github.com/OE-LUCIFER)


If you find this project helpful, consider supporting our work:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow.svg)](https://www.buymeacoffee.com/OEvortex)

</div>

<div align="center">

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OE-LUCIFER/Gemini-Chat-API&type=Date)](https://star-history.com/#OE-LUCIFER/Gemini-Chat-API&Date)

</div>
