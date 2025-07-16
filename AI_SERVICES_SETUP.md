# Free AI Services Setup Guide

This project uses **FREE AI services** instead of OpenAI to generate professional email content. Here's how to set up each option:

## 🚀 Option 1: Groq (Recommended)

**Why Groq?**
- ✅ **Completely FREE** tier with generous limits
- ✅ **Fastest inference** (often under 1 second)
- ✅ **High-quality models** (Mixtral-8x7B, Llama-2, etc.)
- ✅ **No credit card required** for free tier
- ✅ **Simple API** compatible with OpenAI format

**Setup Steps:**
1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up with your email (free account)
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add to your `.env` file:
   ```bash
   AI_SERVICE=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```

**Available Models:**
- `mixtral-8x7b-32768` (recommended - very smart)
- `llama2-70b-4096` (good balance)
- `llama2-7b-2048` (fastest)

---

## 🤗 Option 2: Hugging Face (Completely Free)

**Why Hugging Face?**
- ✅ **100% FREE** with no limits
- ✅ **Open source models** 
- ✅ **No registration fees** ever
- ✅ **Privacy focused** (models run on HF infrastructure)
- ✅ **Thousands of models** available

**Setup Steps:**
1. Go to [https://huggingface.co/](https://huggingface.co/)
2. Create a free account
3. Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
4. Create a new token (read access is enough)
5. Copy the token and add to your `.env` file:
   ```bash
   AI_SERVICE=huggingface
   HUGGINGFACE_API_KEY=your_hf_token_here
   ```

**Available Models:**
- `meta-llama/Llama-2-7b-chat-hf` (default)
- `microsoft/DialoGPT-large`
- `facebook/blenderbot-3B`

---

## 🔧 Option 3: OpenAI (Backup)

**Only use if you already have OpenAI credits**

**Setup Steps:**
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Create account and add payment method
3. Generate API key
4. Add to your `.env` file:
   ```bash
   AI_SERVICE=openai
   OPENAI_API_KEY=your_openai_key_here
   ```

---

## 🎯 Recommended Configuration

For the best experience, use **Groq** with this configuration in your `.env` file:

```bash
# AI Service Configuration
AI_SERVICE=groq
GROQ_API_KEY=your_groq_api_key_here

# Server Configuration  
HOST=localhost
PORT=8000
DEBUG=True
```

---

## 🔍 How to Verify Your Setup

1. Start the backend: `cd backend && python main.py`
2. Check the startup logs - you should see:
   ```
   ✅ AI content generation (GROQ)
   ```
3. If you see warnings about missing API keys, check your `.env` file

---

## 🛠️ Troubleshooting

### Groq Issues
- **"Invalid API key"**: Double-check you copied the entire key
- **"Rate limit exceeded"**: Wait a moment, free tier has limits
- **"Model not found"**: Check the model name in the code

### Hugging Face Issues  
- **"Authorization failed"**: Ensure your token has read access
- **"Model loading timeout"**: HF models sometimes take time to load
- **"Inference error"**: Try a different model or wait and retry

### General Issues
- **"AI service not working"**: Check your internet connection
- **"Fallback content used"**: This is normal - the app will work even if AI fails
- **"No .env file"**: Run the setup script first

---

## 💡 Pro Tips

1. **Start with Groq** - it's the easiest and fastest
2. **Keep your API keys secret** - never commit them to git
3. **Test with simple requests first** - try "send an email about vacation"
4. **Check the browser console** for any error messages
5. **The app works even without AI** - it will use fallback templates

---

## 🆓 Why We Use Free Services

This project demonstrates **browser automation**, not AI capabilities. The AI is just used to generate email content. By using free services:

- ✅ **Anyone can run this** without spending money
- ✅ **No barriers to testing** the browser automation
- ✅ **Focus stays on the core feature** (browser control)
- ✅ **Demonstrates real-world constraints** (most developers use free tiers)

The browser automation works exactly the same regardless of which AI service you choose!
