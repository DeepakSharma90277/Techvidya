# Quick Setup Guide - TechVidya AI Assistant

## ⚡ Quick Start (5 minutes)

### 1. Get API Keys

#### Tavily API Key (Required)
```
1. Visit: https://tavily.com
2. Sign up (free)
3. Go to Dashboard → API Keys
4. Copy your key
```

#### Groq API Key (Required)
```
1. Visit: https://console.groq.com
2. Sign up (free)
3. Go to API Keys → Create New Key
4. Copy your key
```

### 2. Install Dependencies

Open terminal in the `ai-agent` folder:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in `ai-agent` folder:

```env
TAVILY_API_KEY=your_tavily_key_here
GROQ_API_KEY=your_groq_key_here
BACKEND_BASE_URL=http://localhost:4000/api/v1
LLM_PROVIDER=groq
LLM_MODEL=mixtral-8x7b-32768
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
TAVILY_SEARCH_DEPTH=advanced
TAVILY_MAX_RESULTS=5
```

### 4. Run Backend (in root folder)

```bash
cd server
npm install
npm run dev
```

### 5. Run AI Assistant

Open a new terminal in `ai-agent` folder:

```bash
streamlit run app.py
```

### 6. Access the App

- **AI Assistant**: http://localhost:8501
- **Main Platform**: http://localhost:3000
- **Backend API**: http://localhost:4000

## 📋 Testing the System

### Test User ID
Use any valid MongoDB ObjectId from your database, or use demo mode by entering any 24-character hex string.

### Example Usage

1. **Enter User ID** in sidebar (left panel)
2. **Click Login** button
3. Navigate to **"Assessment Recommendations"** tab
4. Select a course and click **"Generate Recommendations"**
5. Navigate to **"AI Study Chat"** tab
6. Type: "Explain React hooks" and click Send

## 🔍 Verification Checklist

- [ ] Python dependencies installed
- [ ] `.env` file created with API keys
- [ ] Backend server running on port 4000
- [ ] Streamlit app running on port 8501
- [ ] Can access AI Assistant from navbar
- [ ] Can login with User ID
- [ ] Can generate recommendations
- [ ] Can chat with AI assistant

## 🐛 Common Issues

### "TAVILY_API_KEY is not set"
→ Check `.env` file exists in `ai-agent` folder
→ Verify key is correct without quotes

### "Backend connection failed"
→ Ensure backend is running: `cd server && npm run dev`
→ Check backend URL in terminal output

### "Module not found"
→ Run: `pip install -r requirements.txt`
→ Ensure you're in the `ai-agent` folder

### Streamlit not found
→ Run: `pip install streamlit`

## 📞 Need Help?

Check the full README.md for detailed documentation.

---

## 🎉 You're All Set!

Access your AI Assistant from the TechVidya navbar: **"AI Assistant"** (with "New" badge)
