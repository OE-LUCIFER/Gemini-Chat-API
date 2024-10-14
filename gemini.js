const axios = require('axios');
const fs = require('fs').promises;
const { v4: uuidv4 } = require('uuid');

class Gemini {
  constructor(cookiePath, timeout = 30000) {
    this.cookiePath = cookiePath;
    this.timeout = timeout;
    this.sessionAuth1 = '';
    this.sessionAuth2 = '';
    this.SNlM0e = '';
    this.conversationId = '';
    this.responseId = '';
    this.choiceId = '';
  }

  async initialize() {
    await this.loadCookies();
    this.SNlM0e = await this.getSnlm0e();
  }

  async loadCookies() {
    try {
      const cookieData = await fs.readFile(this.cookiePath, 'utf8');
      const cookies = JSON.parse(cookieData);
      this.sessionAuth1 = cookies.find(item => item.name === '__Secure-1PSID')?.value;
      this.sessionAuth2 = cookies.find(item => item.name === '__Secure-1PSIDTS')?.value;

      if (!this.sessionAuth1 || !this.sessionAuth2) {
        throw new Error('Required cookies not found in the cookie file.');
      }
    } catch (error) {
      throw new Error(`Failed to load cookies: ${error.message}`);
    }
  }

  async getSnlm0e() {
    try {
      const response = await axios.get('https://gemini.google.com/app', {
        timeout: 10000,
        headers: this.getHeaders(),
      });

      const match = response.data.match(/"SNlM0e":"(.*?)"/);
      if (!match) {
        throw new Error('SNlM0e value not found in response.');
      }

      return match[1];
    } catch (error) {
      throw new Error(`Failed to retrieve SNlM0e: ${error.message}`);
    }
  }

  getHeaders() {
    return {
      'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
      'Host': 'gemini.google.com',
      'Origin': 'https://gemini.google.com',
      'Referer': 'https://gemini.google.com/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'X-Same-Domain': '1',
      'Cookie': `__Secure-1PSID=${this.sessionAuth1}; __Secure-1PSIDTS=${this.sessionAuth2}`,
    };
  }

  async ask(question, sysPrompt = '') {
    try {
      const params = {
        bl: 'boq_assistant-bard-web-server_20230713.13_p0',
        _reqid: '0',
        rt: 'c',
      };

      const messageStruct = [
        [question],
        null,
        [this.conversationId, this.responseId, this.choiceId],
      ];

      const data = new URLSearchParams({
        'f.req': JSON.stringify([null, JSON.stringify(messageStruct)]),
        'at': this.SNlM0e,
      });

      const response = await axios.post(
        'https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate',
        data.toString(),
        {
          params,
          headers: this.getHeaders(),
          timeout: this.timeout,
        }
      );

      const lines = response.data.split('\n');
      const chatData = JSON.parse(lines[3])[0][2];
      if (!chatData) {
        return { content: null, images: [] };
      }

      const jsonChatData = JSON.parse(chatData);
      const images = [];

      if (jsonChatData[4]?.[0]?.[4]) {
        for (const imgData of jsonChatData[4][0][4]) {
          if (imgData?.[0]?.[0]?.[0]) {
            images.push(imgData[0][0][0]);
          }
        }
      }

      const results = {
        content: jsonChatData[4]?.[0]?.[1]?.[0] || null,
        conversationId: jsonChatData[1][0],
        responseId: jsonChatData[1][1],
        images,
      };

      this.conversationId = results.conversationId;
      this.responseId = results.responseId;
      this.choiceId = jsonChatData[4]?.[0]?.[0] || '';

      return results;
    } catch (error) {
      console.error(`An error occurred: ${error.message}`);
      return { content: null, images: [] };
    }
  }
}

module.exports = Gemini;

// Example usage:
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function main() {
  const gemini = new Gemini('cookie.json');
  await gemini.initialize();

  readline.question('>>> ', async (question) => {
    const response = await gemini.ask(question);
    console.log(response.content);
    readline.close();
  });
}

main().catch(console.error);
