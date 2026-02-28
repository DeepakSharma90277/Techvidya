# 🎓 TechVidya - Ed-Tech Learning Platform

A comprehensive MERN stack Learning Management System (LMS) with AI-powered assessment recommendations and study assistance.

## ✨ Features

### Core Platform
- 👥 **Multi-role System**: Student, Instructor, and Admin roles
- 📚 **Course Management**: Create, edit, and manage courses with sections and subsections
- 🎥 **Video Learning**: Integrated video player with progress tracking
- 💳 **Payment Integration**: Razorpay payment gateway for course purchases
- ⭐ **Ratings & Reviews**: Course rating and review system
- 📊 **Analytics Dashboard**: Instructor and student dashboards with insights
- 🛒 **Shopping Cart**: Add multiple courses before checkout
- 🔐 **Secure Authentication**: JWT-based authentication with OTP verification

### 🤖 NEW: AI Assessment & Study Assistant
- **Personalized Recommendations**: Get test recommendations based on your enrolled courses
- **AI Chat Assistant**: Ask questions and get real-time study help using Tavily web search
- **Learning Dashboard**: Track progress, assessments, and study streaks
- **Smart Search**: Find relevant study materials and resources automatically

## 🏗️ Tech Stack

### Frontend
- React 18
- Redux Toolkit (State Management)
- React Router v7
- Tailwind CSS
- Chart.js (Analytics)

### Backend
- Node.js + Express
- MongoDB + Mongoose
- JWT Authentication
- Cloudinary (Media Storage)
- Razorpay (Payments)

### AI Agent
- **Streamlit** (Python web framework)
- **Groq API** (Fast LLM inference)
- **Tavily API** (AI-powered web search)

## 🚀 Quick Start

### Prerequisites
- Node.js 14+
- Python 3.8+ (for AI Agent)
- MongoDB
- Tavily API Key ([Get here](https://tavily.com))
- Groq API Key ([Get here](https://console.groq.com))

### Option 1: Automatic Setup (Recommended)

Run the PowerShell script to start all services:

```powershell
.\start-dev.ps1
```

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
# Root directory (Frontend)
npm install

# Backend
cd server
npm install

# AI Agent
cd ../ai-agent
pip install -r requirements.txt
```

#### 2. Configure Environment

**Backend** - Create `server/.env`:
```env
MONGODB_URL=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
RAZORPAY_KEY=your_razorpay_key
RAZORPAY_SECRET=your_razorpay_secret
```

**AI Agent** - Create `ai-agent/.env`:
```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
BACKEND_BASE_URL=http://localhost:4000/api/v1
```

See `ai-agent/SETUP.md` for detailed AI Agent configuration.

#### 3. Start Services

**Terminal 1 - Backend:**
```bash
cd server
npm run dev
```

**Terminal 2 - AI Agent:**
```bash
cd ai-agent
streamlit run app.py
```

**Terminal 3 - Frontend:**
```bash
npm start
```

### Access the Application

- **Frontend**: http://localhost:3000
- **AI Agent**: http://localhost:8501  
- **Backend API**: http://localhost:4000

## 📖 Documentation

- **AI Agent Setup**: [ai-agent/SETUP.md](ai-agent/SETUP.md)
- **AI Agent Documentation**: [ai-agent/README.md](ai-agent/README.md)
- **Run Scripts**: [ai-agent/RUN_SCRIPTS.md](ai-agent/RUN_SCRIPTS.md)

## 🎯 Using the AI Assistant

1. **Access**: Click "AI Assistant" in the navigation bar (marked with "New" badge)
2. **Login**: Enter your User ID from the TechVidya platform
3. **Get Recommendations**: Navigate to "Assessment Recommendations" tab and select your course
4. **Chat**: Use the "AI Study Chat" to ask questions and get study resources
5. **Track Progress**: View your dashboard for metrics and enrolled courses

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
