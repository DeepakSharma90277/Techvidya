# 🏗️ TechVidya AI Agent - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│                                                                  │
│  ┌────────────────────────┐        ┌──────────────────────────┐│
│  │   React Frontend       │        │   Streamlit AI Agent     ││
│  │   (Port 3000)          │        │   (Port 8501)            ││
│  │                        │        │                          ││
│  │  - Course Catalog      │◄──────►│  - Assessment Recomm.   ││
│  │  - Dashboard           │        │  - AI Chat              ││
│  │  - Video Player        │        │  - Learning Dashboard   ││
│  │  - Cart & Payments     │        │                         ││
│  │  - Navbar (AI Link) ───┼────────┼─► Opens in New Tab      ││
│  └────────┬───────────────┘        └──────────┬──────────────┘│
└───────────┼──────────────────────────────────┼────────────────┘
            │                                   │
            │ REST API                          │ REST API
            │                                   │
┌───────────▼───────────────────────────────────▼────────────────┐
│                   Express.js Backend                            │
│                   (Port 4000)                                   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │   Routes     │  │ Controllers  │  │   Middleware       │  │
│  │              │  │              │  │                    │  │
│  │ - User       │  │ - Auth       │  │ - JWT Auth         │  │
│  │ - Course     │  │ - Course     │  │ - File Upload      │  │
│  │ - Payment    │  │ - Payment    │  │ - Error Handler    │  │
│  │ - AI Agent ◄─┼──┼─ AI Agent◄──┼──┤                    │  │
│  └──────────────┘  └──────────────┘  └────────────────────┘  │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            │ Mongoose ODM
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      MongoDB Database                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Users   │  │ Courses  │  │ Payments │  │ CourseProgr. │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    External Services                              │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐│
│  │ Groq API    │  │ Tavily API  │  │ Cloudinary / Razorpay    ││
│  │ (LLM)       │  │ (Search)    │  │ (Media / Payments)       ││
│  └─────────────┘  └─────────────┘  └──────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow - Assessment Recommendations

```
1. User Action
   │
   ├─► User logs into AI Agent with User ID
   │
2. Fetch User Context
   │
   ├─► Streamlit → Backend API
   │   GET /api/v1/aiagent/user-context/:userId
   │
   ├─► Backend queries MongoDB
   │   - User profile
   │   - Enrolled courses
   │   - Course progress
   │
   └─► Returns user data to Streamlit
   │
3. Generate Recommendations
   │
   ├─► User selects course & filters
   │
   ├─► Recommendation Engine processes:
   │   ├─► Analyzes course content
   │   ├─► Calls Groq LLM for suggestions
   │   └─► Searches Tavily for real links
   │
   └─► Displays recommendation cards
   │
4. User Interaction
   │
   ├─► Click "Take Assessment" → Opens external link
   ├─► Click "Study Materials" → Tavily search
   └─► Click "Save" → Store in session state
```

## Data Flow - AI Chat Assistant

```
1. User asks question
   │
   ├─► "Explain React hooks"
   │
2. Context Building
   │
   ├─► Gather user's enrolled courses
   ├─► Include recent chat history
   └─► Build system prompt
   │
3. Web Search (if enabled)
   │
   ├─► Tavily API search:
   │   "React hooks tutorial"
   │
   ├─► Returns top 3-5 results:
   │   - Title
   │   - URL
   │   - Content snippet
   │
   └─► Formats as context
   │
4. LLM Generation
   │
   ├─► Groq API call with:
   │   - System prompt
   │   - User context
   │   - Web search results
   │   - User question
   │
   ├─► LLM generates response
   │
   └─► Returns answer with sources
   │
5. Display Response
   │
   ├─► Show LLM answer
   ├─► Show source citations
   └─► Update chat history
```

## Component Architecture - Streamlit App

```
app.py (Main Application)
│
├── Session State Management
│   ├── chat_history
│   ├── recommendations
│   ├── user_context
│   └── llm_initialized
│
├── Components (UI)
│   │
│   ├── sidebar.py
│   │   ├── User login
│   │   ├── Configuration status
│   │   └── Quick links
│   │
│   ├── chat_interface.py
│   │   ├── Message display
│   │   ├── Input handling
│   │   ├── Quick actions
│   │   └── Source citations
│   │
│   └── assessment_rec.py
│       ├── Course selection
│       ├── Filters
│       ├── Recommendation cards
│       └── Study materials
│
├── Services (Business Logic)
│   │
│   ├── llm_service.py
│   │   ├── Groq client init
│   │   ├── Response generation
│   │   ├── System prompt builder
│   │   └── Assessment recommendations
│   │
│   ├── tavily_service.py
│   │   ├── Web search
│   │   ├── Educational content search
│   │   ├── Assessment resource search
│   │   └── Context extraction
│   │
│   └── recommendation_engine.py
│       ├── LLM-based generation
│       ├── Template-based fallback
│       ├── Link enrichment
│       └── Topic extraction
│
└── Utils (Helpers)
    │
    ├── api_client.py
    │   ├── Backend communication
    │   ├── User context fetching
    │   └── Recommendation saving
    │
    └── helpers.py
        ├── Text formatting
        ├── Duration conversion
        ├── Topic parsing
        └── Validation
```

## Technology Stack Details

### Frontend Stack
```
React Application
├── UI Framework: React 18
├── State Management: Redux Toolkit
├── Routing: React Router v7
├── Styling: Tailwind CSS
├── Icons: React Icons
├── Charts: Chart.js
├── Forms: React Hook Form
└── HTTP Client: Axios
```

### Backend Stack
```
Express Server
├── Runtime: Node.js
├── Framework: Express.js
├── Database: MongoDB
├── ODM: Mongoose
├── Auth: JWT + bcrypt
├── File Upload: express-fileupload
├── Email: Nodemailer
├── Payments: Razorpay
└── Storage: Cloudinary
```

### AI Agent Stack
```
Streamlit Application
├── Framework: Streamlit
├── Language: Python 3.8+
├── LLM: Groq API
├── Search: Tavily API
├── HTTP: requests / httpx
├── Config: python-dotenv
└── Data: pandas, numpy
```

## Security Flow

```
Request Flow with Security

1. React Frontend
   ├─► User logs in
   ├─► Receives JWT token
   └─► Stores in localStorage
   
2. All API Requests
   ├─► Includes Authorization header
   ├─► "Bearer <jwt_token>"
   └─► Sent to Express backend
   
3. Backend Middleware
   ├─► auth.js validates JWT
   ├─► Extracts user ID
   ├─► Attaches to req.user
   └─► Proceeds to controller
   
4. AI Agent
   ├─► Uses User ID (not JWT)
   ├─► Public endpoints for demo
   ├─► Can be protected if needed
   └─► API keys in .env only
```

## Deployment Architecture

```
Production Environment

┌─────────────────────────────────────┐
│   Frontend (Vercel / Netlify)       │
│   - React build (static files)      │
│   - CDN distributed                 │
└──────────────┬──────────────────────┘
               │
               │ HTTPS
               │
┌──────────────▼──────────────────────┐
│   Backend (Heroku / AWS / DigitalOcean)│
│   - Express server                  │
│   - Environment variables           │
└──────────────┬──────────────────────┘
               │
               │ MongoDB Atlas
               │
┌──────────────▼──────────────────────┐
│   Database (MongoDB Atlas)          │
│   - Managed MongoDB                 │
│   - Automated backups               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   AI Agent (Streamlit Cloud)        │
│   - Python application              │
│   - Environment variables           │
│   - Auto-scaling                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   External APIs (SaaS)              │
│   - Groq (LLM)                      │
│   - Tavily (Search)                 │
│   - Cloudinary (Media)              │
│   - Razorpay (Payments)             │
└─────────────────────────────────────┘
```

## Development Environment Ports

| Service | Port | URL |
|---------|------|-----|
| React Frontend | 3000 | http://localhost:3000 |
| Express Backend | 4000 | http://localhost:4000 |
| Streamlit AI Agent | 8501 | http://localhost:8501 |
| MongoDB | 27017 | mongodb://localhost:27017 |

## File Organization

```
Techvidya/
│
├── Frontend (React)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Common/
│   │   │   │   └── Navbar.jsx ◄── AI Agent Link
│   │   │   └── core/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── slices/ (Redux)
│   │   └── data/
│   │       └── navbar-links.js ◄── AI Assistant Entry
│   ├── package.json
│   └── tailwind.config.js
│
├── Backend (Express)
│   ├── config/
│   ├── controllers/
│   │   └── aiAgent.js ◄── NEW
│   ├── models/
│   ├── routes/
│   │   └── aiAgent.js ◄── NEW
│   ├── middleware/
│   ├── utils/
│   ├── index.js ◄── Updated
│   └── package.json
│
├── AI Agent (Streamlit)
│   ├── components/ ◄── NEW
│   ├── services/ ◄── NEW
│   ├── utils/ ◄── NEW
│   ├── app.py ◄── NEW
│   ├── config.py ◄── NEW
│   ├── requirements.txt ◄── NEW
│   ├── .env.example ◄── NEW
│   ├── README.md ◄── NEW
│   └── SETUP.md ◄── NEW
│
├── Documentation
│   ├── README.md ◄── Updated
│   ├── AI_AGENT_SUMMARY.md ◄── NEW
│   └── start-dev.ps1 ◄── NEW
│
└── Configuration
    ├── package.json
    ├── tailwind.config.js
    └── postcss.config.js
```

---

This architecture provides:
- ✅ Scalability
- ✅ Maintainability
- ✅ Security
- ✅ Performance
- ✅ Extensibility
