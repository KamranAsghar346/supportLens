# SupportLens

Customer Support Chatbot Observability Platform.

SupportLens is a lightweight observability tool for monitoring a customer support chatbot. It includes a support chatbot interface and a dashboard that displays every conversation trace with LLM-based classification and aggregate statistics.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React, Vite
- **LLM:** OpenAI GPT-4o-mini (chatbot responses & trace classification)

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **OpenAI API Key**

## Setup & Running Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd SupportLens
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

Start the backend:

```bash
python main.py
```

The API will be available at `http://localhost:8000`. On first startup, the database is automatically seeded with 22 sample traces.

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## How It Works

1. **Chatbot** — A user sends a message through the chat interface. The backend generates a response using an LLM (GPT-4o-mini acting as a SaaS billing support agent).
2. **Trace Logging** — Each query/response pair is saved as a trace with a measured response time.
3. **Classification** — A second LLM call classifies the trace into one of five categories: Billing, Refund, Account Access, Cancellation, or General Inquiry.
4. **Dashboard** — The observability dashboard displays aggregate statistics (total traces, category breakdown, average response time) and a filterable trace log.

## API Endpoints

| Method | Endpoint      | Description                                              |
|--------|---------------|----------------------------------------------------------|
| POST   | `/chat`       | Send a message, get a response, and log the trace        |
| POST   | `/traces`     | Submit a trace for classification and storage            |
| GET    | `/traces`     | Get all traces (newest first), with optional `?category=` filter |
| GET    | `/analytics`  | Get aggregate stats (totals, category breakdown, avg response time) |

## Classification Categories

| Category         | Description                                              |
|------------------|----------------------------------------------------------|
| Billing          | Invoices, charges, payment methods, pricing              |
| Refund           | Returns, refunds, disputes, credits                      |
| Account Access   | Login issues, password resets, locked accounts, MFA      |
| Cancellation     | Cancel subscriptions, downgrade plans, close accounts    |
| General Inquiry  | Feature questions, product info, how-to, feedback        |

## Project Structure

```
├── backend/
│   ├── main.py            # FastAPI app with all endpoints & LLM prompts
│   ├── models.py          # SQLAlchemy Trace model
│   ├── database.py        # SQLite database configuration
│   ├── seed.py            # 22 pre-classified seed traces
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variable template
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main app with tab navigation
│   │   ├── api.js         # API client functions
│   │   └── components/
│   │       ├── ChatBot.jsx        # Chat interface
│   │       ├── Dashboard.jsx      # Dashboard container
│   │       ├── AggregateStats.jsx # Stats cards & category breakdown
│   │       ├── TraceTable.jsx     # Trace log table
│   │       └── TraceDetail.jsx    # Expanded trace view
│   ├── index.html
│   └── vite.config.js     # Vite config with API proxy
└── README.md
```
