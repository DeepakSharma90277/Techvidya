# 🚀 TechVidya AI Agent - Run Scripts

## Windows - PowerShell Scripts

### Start Everything (Development Mode)

Run this in PowerShell from the root `Techvidya` directory:

```powershell
# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd .\server; npm run dev"

# Wait 5 seconds for backend to start
Start-Sleep -Seconds 5

# Start AI Agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd .\ai-agent; streamlit run app.py"

# Wait 3 seconds for AI agent to start
Start-Sleep -Seconds 3

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"

Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🤖 AI Agent: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:4000" -ForegroundColor Cyan
```

Save this as `start-dev.ps1` in the root folder and run:
```powershell
.\start-dev.ps1
```

### Start Individual Services

#### Backend Only
```powershell
cd server
npm run dev
```

#### AI Agent Only
```powershell
cd ai-agent
streamlit run app.py
```

#### Frontend Only
```powershell
npm start
```

## Linux/Mac - Bash Scripts

Save as `start-dev.sh`:

```bash
#!/bin/bash

# Start Backend
cd server && npm run dev &
BACKEND_PID=$!

sleep 5

# Start AI Agent
cd ../ai-agent && streamlit run app.py &
AGENT_PID=$!

sleep 3

# Start Frontend
cd .. && npm start &
FRONTEND_PID=$!

echo "✅ All services started!"
echo "📱 Frontend: http://localhost:3000"
echo "🤖 AI Agent: http://localhost:8501"
echo "🔧 Backend API: http://localhost:4000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait
```

Make executable and run:
```bash
chmod +x start-dev.sh
./start-dev.sh
```

## Package.json Scripts

Add to root `package.json`:

```json
{
  "scripts": {
    "start": "concurrently -n \"client,server\" -c \"bgBlue,bgYellow\" \"react-scripts start\" \"npm run server\"",
    "server": "cd server && npm run dev",
    "ai-agent": "cd ai-agent && streamlit run app.py",
    "dev:all": "concurrently -n \"client,server,ai\" -c \"bgBlue,bgYellow,bgGreen\" \"react-scripts start\" \"npm run server\" \"npm run ai-agent\""
  }
}
```

Then run:
```bash
npm run dev:all
```

## Docker Compose (Optional)

Create `docker-compose.yml` in root:

```yaml
version: '3.8'

services:
  backend:
    build: ./server
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=development
    volumes:
      - ./server:/app
      - /app/node_modules

  ai-agent:
    build: ./ai-agent
    ports:
      - "8501:8501"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./ai-agent:/app

  frontend:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - backend
      - ai-agent
```

Run with:
```bash
docker-compose up
```

## Stop All Services

### Windows PowerShell
```powershell
# Kill by port
Get-NetTCPConnection -LocalPort 3000,4000,8501 | % { Stop-Process -Id $_.OwningProcess -Force }
```

### Linux/Mac
```bash
# Kill by port
lsof -ti:3000,4000,8501 | xargs kill -9
```

## Health Check Script

Save as `health-check.ps1` (Windows) or `health-check.sh` (Linux/Mac):

```powershell
# health-check.ps1
$services = @{
    "Frontend" = "http://localhost:3000"
    "Backend" = "http://localhost:4000"
    "AI Agent" = "http://localhost:8501"
}

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-WebRequest -Uri $service.Value -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ $($service.Key): Running" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($service.Key): Not responding" -ForegroundColor Red
    }
}
```

## VS Code Task Configuration

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd server && npm run dev",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start AI Agent",
      "type": "shell",
      "command": "cd ai-agent && streamlit run app.py",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "npm start",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start All Services",
      "dependsOn": ["Start Backend", "Start AI Agent", "Start Frontend"],
      "problemMatcher": []
    }
  ]
}
```

Access via: `Ctrl+Shift+P` → "Tasks: Run Task" → "Start All Services"
