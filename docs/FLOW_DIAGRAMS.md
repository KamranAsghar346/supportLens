# SupportLens — Flow Diagrams

This document contains Mermaid diagrams for the SupportLens platform. Render in GitHub, VS Code (Mermaid extension), or [mermaid.live](https://mermaid.live).

---

## 1. System Architecture

```
Browser → Frontend (React) → Vite Proxy (/api) → Backend (FastAPI) → SQLite + OpenAI
```

```mermaid
flowchart TB
    subgraph Client["Client"]
        Browser["Browser"]
    end

    subgraph Frontend["Frontend - React + Vite :5173"]
        App[App.jsx]
        Dashboard[Dashboard]
        ChatBot[ChatBot]
        API[api.js]
    end

    subgraph Proxy["Vite Proxy"]
        Rule["/api → :8000"]
    end

    subgraph Backend["Backend - FastAPI :8000"]
        Chat[POST /chat]
        Traces[GET /traces]
        Analytics[GET /analytics]
        CreateTrace[POST /traces]
    end

    subgraph External["External"]
        OpenAI[OpenAI GPT-4o-mini]
        DB[(SQLite)]
    end

    Browser --> App
    App --> Dashboard
    App --> ChatBot
    Dashboard --> API
    ChatBot --> API
    API --> Proxy
    Proxy --> Backend
    Chat --> OpenAI
    Chat --> DB
    Traces --> DB
    Analytics --> DB
    CreateTrace --> OpenAI
    CreateTrace --> DB
```

---

## 2. Component Hierarchy

```mermaid
flowchart TD
    App[App]
    Header[Header]
    Dashboard[Dashboard]
    ChatBot[ChatBot]
    AggregateStats[AggregateStats]
    TraceTable[TraceTable]
    TraceDetail[TraceDetail]

    App --> Header
    App --> Dashboard
    App --> ChatBot
    Dashboard --> AggregateStats
    Dashboard --> TraceTable
    TraceTable --> TraceDetail
```

---

## 3. Chat Message Flow (Sequence)

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant C as ChatBot
    participant A as api.js
    participant B as Backend
    participant O as OpenAI
    participant D as SQLite

    U->>C: Send message
    C->>A: sendChatMessage(msg)
    A->>B: POST /chat
    B->>O: Generate response
    O-->>B: bot_response
    B->>O: Classify trace
    O-->>B: category
    B->>D: INSERT trace
    B-->>A: TraceResponse
    A-->>C: trace
    C->>C: onNewTrace()
    C-->>U: Show response + badge
```

---

## 4. Dashboard Data Flow

```mermaid
flowchart LR
    subgraph User
        Open[Open Dashboard]
        Filter[Change Category]
        Refresh[Click Refresh]
    end

    subgraph Dashboard
        Fetch[fetchData]
        Stats[AggregateStats]
        Table[TraceTable]
    end

    subgraph API
        GetTraces[GET /traces]
        GetAnalytics[GET /analytics]
    end

    Open --> Fetch
    Filter --> Fetch
    Refresh --> Fetch
    Fetch --> GetTraces
    Fetch --> GetAnalytics
    GetTraces --> Stats
    GetTraces --> Table
    GetAnalytics --> Stats
```

---

## 5. Trace Classification Logic

```mermaid
flowchart TD
    A[user_message + bot_response] --> B[Build prompt]
    B --> C[OpenAI: gpt-4o-mini]
    C --> D[raw = response.strip().lower]
    D --> E{Exact match?}
    E -->|Yes| F[Return category]
    E -->|No| G{Partial match?}
    G -->|Yes| F
    G -->|No| H[Return General Inquiry]
```

---

## 6. State Flow (React)

```mermaid
stateDiagram-v2
    [*] --> App
    App --> Dashboard: activeTab=dashboard
    App --> ChatBot: activeTab=chatbot

    state Dashboard {
        [*] --> Loading
        Loading --> Ready: data fetched
        Ready --> Loading: category/refreshKey change
    }

    state ChatBot {
        [*] --> Idle
        Idle --> Loading: send message
        Loading --> Idle: response received
    }
```

---

## 7. Data Model

```mermaid
erDiagram
    TRACES {
        string id PK
        string user_message
        string bot_response
        string category
        datetime timestamp
        int response_time_ms
    }
```

---

## 8. Feature Map

```mermaid
mindmap
  root((SupportLens))
    Chatbot
      BillEase Support
      Suggestion Chips
      Category Badge
      Response Time
      Error Handling
    Dashboard
      Total Traces
      Avg Response Time
      Category Breakdown
      Trace Table
      Expandable Detail
      Category Filter
    Backend
      POST /chat
      POST /traces
      GET /traces
      GET /analytics
      LLM Classification
```

---

*Render these diagrams in any Mermaid-compatible viewer for best results.*
