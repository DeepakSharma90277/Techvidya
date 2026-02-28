# TechVidya AI Assessment & Study Assistant

An intelligent AI-powered system that provides personalized assessment recommendations and study assistance for TechVidya students.

## 🌟 Features

### 1. **Personalized Assessment Recommendations**
- Analyzes enrolled courses to recommend relevant tests and quizzes
- Filters by difficulty level and assessment type
- Real assessment links from educational platforms (via Tavily web search)
- Direct links to practice problems and coding challenges

### 2. **AI Study Chat Assistant**
- Interactive chat interface for study-related queries
- Real-time web search integration using Tavily API
- Context-aware responses based on enrolled courses
- Provides explanations, study tips, and learning resources

### 3. **Learning Dashboard**
- Track enrolled courses and progress
- View assessment completion statistics
- Monitor study streaks and scores
- Quick access to course-specific tests

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit (Python-based web framework)
- **LLM**: Groq API (fast, free-tier LLM)
- **Web Search**: Tavily API (AI-powered web search)
- **Backend**: Express.js (Node.js)
- **Database**: MongoDB (via existing TechVidya backend)

### System Components

```
┌─────────────────────┐
│  Streamlit UI       │
│  - Chat Interface   │
│  - Recommendations  │
│  - Dashboard        │
└──────────┬──────────┘
           │
           ├──────────────┬──────────────┐
           │              │              │
     ┌─────▼─────┐  ┌────▼────┐  ┌─────▼──────┐
     │ Groq API  │  │ Tavily  │  │  Backend   │
     │   (LLM)   │  │ (Search)│  │    API     │
     └───────────┘  └─────────┘  └────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ (for backend)
- Tavily API key ([Get it here](https://tavily.com))
- Groq API key ([Get it here](https://console.groq.com))

### Step 1: Install Python Dependencies

```bash
cd ai-agent
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# API Keys
TAVILY_API_KEY=tvly-xxx...
GROQ_API_KEY=gsk_xxx...

# Backend Configuration
BACKEND_BASE_URL=http://localhost:4000/api/v1

# LLM Configuration
LLM_PROVIDER=groq
LLM_MODEL=mixtral-8x7b-32768
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024

# Tavily Configuration
TAVILY_SEARCH_DEPTH=advanced
TAVILY_MAX_RESULTS=5
```

### Step 3: Start the Backend (if not running)

```bash
cd server
npm install
npm run dev
```

### Step 4: Run the Streamlit App

```bash
cd ai-agent
streamlit run app.py
```

The AI Assistant will be available at: **http://localhost:8501**

## 🚀 Usage

### 1. Access the AI Assistant

From the TechVidya navbar, click on **"AI Assistant"** (marked with a "New" badge), or navigate directly to `http://localhost:8501`.

### 2. Login with User ID

Enter your TechVidya User ID in the sidebar to load your profile and courses.

**Demo Mode**: If the backend is unavailable, the system will use demo data for testing.

### 3. Get Assessment Recommendations

Navigate to the **"Assessment Recommendations"** tab:
- Select a course from your enrolled courses
- Apply filters (difficulty, type)
- Click "Generate Recommendations"
- View personalized test recommendations with links

### 4. Chat with AI Assistant

Navigate to the **"AI Study Chat"** tab:
- Type your question or study-related query
- Toggle "Search Web" to enable real-time information retrieval
- Use quick action buttons for common tasks
- View sources for AI-generated responses

### 5. Track Progress

Navigate to the **"Dashboard"** tab:
- View your enrolled courses
- Check completion metrics
- Monitor study statistics

## 🔑 API Keys Setup

### Getting Tavily API Key

1. Visit [tavily.com](https://tavily.com)
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key to `.env`

**Free Tier**: 1,000 searches/month

### Getting Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API keys section
4. Create a new API key
5. Copy your API key to `.env`

**Free Tier**: High request limits, very fast inference

## 📁 Project Structure

```
ai-agent/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Documentation
│
├── components/                # UI Components
│   ├── __init__.py
│   ├── chat_interface.py     # Chat UI
│   ├── assessment_rec.py     # Recommendation UI
│   └── sidebar.py            # Sidebar & auth
│
├── services/                  # Business Logic
│   ├── __init__.py
│   ├── tavily_service.py     # Tavily API integration
│   ├── llm_service.py        # Groq LLM integration
│   └── recommendation_engine.py  # Recommendation logic
│
└── utils/                     # Utilities
    ├── __init__.py
    ├── api_client.py         # Backend API client
    └── helpers.py            # Helper functions
```

## 🔧 Configuration Options

### LLM Models (Groq)

Available models in free tier:
- `mixtral-8x7b-32768` (Recommended - Best balance)
- `llama2-70b-4096` (Faster, shorter context)
- `gemma-7b-it` (Lightweight)

### Tavily Search Depth

- `basic`: Faster, fewer results
- `advanced`: More comprehensive, better for complex queries

## 🐛 Troubleshooting

### Backend Connection Issues

If you see "Using demo data for testing":
- Ensure the backend server is running (`npm run dev` in server folder)
- Check `BACKEND_BASE_URL` in `.env`
- Verify backend route `/api/v1/aiagent/user-context/:userId` exists

### API Rate Limits

**Tavily**: 1,000 searches/month on free tier
- Solution: Cache results, use sparingly

**Groq**: High limits but may throttle
- Solution: Add retry logic, reduce request frequency

### Streamlit Performance

If the app is slow:
- Clear Streamlit cache: Click ☰ menu → Clear Cache
- Restart the app
- Check API response times

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for all sensitive data
- Implement rate limiting for production
- Add authentication for user-specific features

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub repository
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Add environment variables in dashboard
5. Deploy!

### Environment Variables for Production

Set these in your deployment platform:
```
TAVILY_API_KEY=...
GROQ_API_KEY=...
BACKEND_BASE_URL=https://your-backend-url.com/api/v1
```

## 📝 Future Enhancements

- [ ] Save assessment progress to database
- [ ] Track completed assessments
- [ ] Spaced repetition algorithm for reviews
- [ ] Study plan generation
- [ ] Peer comparison and leaderboards
- [ ] Mobile responsive design
- [ ] Voice input for questions
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of TechVidya educational platform.

## 💬 Support

For issues or questions:
- Open an issue on GitHub
- Contact: support@techvidya.com

---

**Built with ❤️ for TechVidya students**
