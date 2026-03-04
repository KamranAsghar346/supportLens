const API_BASE = '/api';

export async function sendChatMessage(userMessage) {
    const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: userMessage }),
    });
    if (!res.ok) throw new Error('Failed to send message');
    return res.json();
}

export async function getTraces(category = null) {
    const params = category ? `?category=${encodeURIComponent(category)}` : '';
    const res = await fetch(`${API_BASE}/traces${params}`);
    if (!res.ok) throw new Error('Failed to fetch traces');
    return res.json();
}

export async function getAnalytics() {
    const res = await fetch(`${API_BASE}/analytics`);
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
}
