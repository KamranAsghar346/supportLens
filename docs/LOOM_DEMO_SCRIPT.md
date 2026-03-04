# SupportLens — Loom Demo Presentation Script (3–5 Minutes)

A presentation-style script for your submission video. Aim for 3–5 minutes total.

---

## Before You Start

1. Start the backend: `cd backend && python main.py`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:5173` in your browser
4. Start the Loom recording

---

## Presentation Script

---

### [SLIDE 1] Opening

*[Pause briefly. Face the camera.]*

"Good [morning / afternoon]. My name is [Your Name].

Today I'm presenting SupportLens — a customer support chatbot observability platform that I built for the Core Edge Solutions case study.

The platform has two main components: a support chatbot that acts as a billing assistant for BillEase, and an observability dashboard that monitors every conversation. Every message is logged as a trace and classified into one of five categories using an LLM.

Let me walk you through a live demo."

---

### [SLIDE 2] Chatbot — First Question

*[Switch to Chatbot tab. Type and send.]*

"For my first question, I'll ask about payment methods."

**[Type and send:]** *"What payment methods do you accept?"*

*[Wait for response.]*

"As you can see, the chatbot responded — and notice the badge here. This conversation was automatically classified as **Billing**. We also see the response time in milliseconds."

---

### [SLIDE 3] Chatbot — Second Question

*[Type and send.]*

"Second question. I'll simulate a customer who was charged twice."

**[Type and send:]** *"I was double-charged, I need a refund for the extra payment"*

*[Wait for response.]*

"The chatbot handled the refund request. And the classification engine correctly identified this as **Refund** — the primary intent of the customer."

---

### [SLIDE 4] Chatbot — Third Question

*[Type and send.]*

"My third question is about account access."

**[Type and send:]** *"I can't log in — it says my password is wrong"*

*[Wait for response.]*

"Here the chatbot helped with a login issue. And you can see the classification: **Account Access**. Each response shows its category and response time directly in the chat."

---

### [SLIDE 5] Dashboard — Traces

*[Switch to Dashboard tab.]*

"Now let's look at the observability dashboard."

*[Point to the trace table.]*

"The dashboard has refreshed. These three conversations are now visible here. Each row shows the timestamp, user message, bot response, category badge, and response time. The categories are color-coded for quick scanning."

*[Click a row to expand.]*

"When I click a row, it expands to show the full user message and bot response."

---

### [SLIDE 6] Dashboard — Filter & Stats

*[Use the category filter dropdown.]*

"You can filter by category — for example, to view only Billing or only Refund traces."

*[Point to the top stats.]*

"At the top, we have the aggregate statistics: total traces processed, average response time, and a category breakdown with count and percentage. This gives operators a clear view of what customers are asking about and how the chatbot is performing."

---

### [SLIDE 7] Closing

"That concludes my demo of SupportLens. Thank you for watching. The repository link and setup instructions are in the description below."

---

## Quick Reference: 3 Questions

| # | Question | Expected Category |
|---|----------|-------------------|
| 1 | "What payment methods do you accept?" | Billing |
| 2 | "I was double-charged, I need a refund for the extra payment" | Refund |
| 3 | "I can't log in — it says my password is wrong" | Account Access |

---

## Timing Guide (Total: ~3–5 minutes)

| Section | Duration |
|---------|----------|
| Opening | 30–45 sec |
| Chatbot (3 questions) | 1.5–2 min |
| Dashboard | 1–1.5 min |
| Closing | 15–20 sec |

---

## Presentation Tips

- Speak clearly and at a steady pace.
- Pause briefly between sections.
- Move the cursor deliberately so the viewer can follow.
- Keep the browser window clean — hide DevTools if needed.
- End with a clear thank you and mention the repo link.
