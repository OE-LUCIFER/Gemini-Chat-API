# Gemini Chat API 🌟✨

Welcome to the **Gemini Chat API**! 🎉 This is an unofficial API designed to interact with Google's Gemini chat model. With this API, you can easily integrate Gemini's powerful language capabilities into your projects. 🚀💫

## Prerequisites 🛠️

Before you dive in, make sure you have the following:

1. **Python** installed on your machine. 🐍
2. Installation of Requirements 📦

To install all required packages, you can use:
```
pip install -r requirements.txt
```

3. Install the **Cookie-Editor** extension for either Chrome or Edge:
   - [Chrome Extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - [Edge Extension](https://microsoftedge.microsoft.com/addons/detail/cookie-editor/neaplmfkghagebokkhpjpoebhdledlfi)

### Exporting Cookies 🍪

Once you have the Cookie-Editor installed, follow these steps to export your cookies:

1. Open [https://gemini.google.com/](https://gemini.google.com/) in your browser. 🌐
2. Click on the Cookie-Editor extension icon. 🔍
3. Click the "Export" button to save your cookies in JSON format. 💾
4. Create a file in your working directory named `cookie.json`. 🗂️
5. Paste the data copied from the Cookie-Editor into `cookie.json` and save it. ✨

## Usage Limits 📊

Please note that usage limits for the unofficial Gemini API are not publicly documented. Be mindful of your usage to avoid potential restrictions. 🚦

## Example Usage 💻💖

Let's explore some fun examples of how to use the Gemini Chat API! 🎈

### 🌈 Storytelling Example

Imagine you want to ask Gemini to tell you a heartwarming story. Here's how you can do it:

```python
gemini = GeminiWithCookie('cookie.json')
response = gemini.ask("🌟 Can you tell me a magical story about a brave little girl and her talking cat? 🐱✨")
print(response)
```

### 🧠 Problem-Solving Example

Let's say you want Gemini to help you solve a riddle. Here's how you can ask:

```python
gemini = GeminiWithCookie('cookie.json')
response = gemini.ask("""
🤔 Can you help me solve this riddle?

I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?
""")
print(response)
```

### 🎨 Creative Writing Example

Want to spark your creativity? Ask Gemini for a writing prompt:

```python
gemini = GeminiWithCookie('cookie.json')
response = gemini.ask("🖋️ Give me an intriguing writing prompt for a science fiction short story. 🚀")
print(response)
```

## Contributing 🤝💕

We welcome contributions! If you have suggestions or improvements, feel free to open an issue or submit a pull request. Your input means the world to us! 🌍❤️

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the **Gemini Chat API**! We hope you find it helpful and enjoyable! If you have any questions, feel free to reach out. Happy coding! 🎊💖
