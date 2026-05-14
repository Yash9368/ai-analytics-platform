# 🚀 AI-Powered Analytics Platform

A production-grade, AI-powered analytics dashboard that tracks website traffic using Google Analytics 4 (GA4), serves data through a Python FastAPI backend, integrates Claude MCP for AI-powered insights, and displays everything in a modern Next.js frontend.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │Dashboard │  │  Charts  │  │  Cards   │  │  AI Insights │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       └──────────────┴──────────────┴───────────────┘         │
│                          │ Axios HTTP                         │
└──────────────────────────┼───────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────┐
│                     BACKEND (FastAPI)                         │
│  ┌─────────┐  ┌──────────┴──────┐  ┌──────────────────────┐  │
│  │  Routes  │  │Analytics Service│  │  Claude MCP Server   │  │
│  └────┬─────┘  └────┬───────────┘  └──────────┬───────────┘  │
│       │              │                         │              │
│       │    ┌─────────┴──────────┐    ┌─────────┴──────────┐  │
│       │    │ GA4 Data API       │    │ Anthropic SDK       │  │
│       │    │ (Service Account)  │    │ (AI Insights)       │  │
│       │    └────────────────────┘    └────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────┐
│              GOOGLE ANALYTICS 4 (GA4)                        │
│  ┌────────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │  GA4 Property   │  │  Web Stream   │  │  Events/Views  │  │
│  └────────────────┘  └───────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧰 Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Frontend   | Next.js, TypeScript, TailwindCSS, Recharts, Axios |
| Backend    | Python, FastAPI, Uvicorn, Pydantic      |
| Analytics  | Google Analytics 4, GA4 Data API        |
| AI Layer   | Claude MCP, Python MCP Server, Anthropic SDK |
| Auth       | Google Service Account (JSON credentials) |
| Deployment | Render (frontend + backend), GitHub     |

---

## 📁 Project Structure

```
ai-analytics-platform/
├── frontend/           # Next.js dashboard application
├── backend/            # Python FastAPI server
├── docs/               # Project documentation
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🔐 Authentication

This project uses **Google Service Account** authentication:
- Works with **personal Gmail** accounts
- Does NOT require Google Workspace
- Uses secure JSON key files (never committed to git)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Google Cloud account (free tier works)
- GA4 property configured

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📄 License

MIT License

---

## 🏷️ Status

🟡 **Phase 1** — Project Foundation (In Progress)
