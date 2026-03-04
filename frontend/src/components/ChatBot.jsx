import { useState } from 'react';
import { sendChatMessage } from '../api';
import './ChatBot.css';

function ChatBot({ onNewTrace }) {
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!message.trim() || loading) return;

        const userMsg = message.trim();
        setMessage('');
        setConversation((prev) => [...prev, { role: 'user', text: userMsg }]);
        setLoading(true);

        try {
            const trace = await sendChatMessage(userMsg);
            setConversation((prev) => [
                ...prev,
                {
                    role: 'bot',
                    text: trace.bot_response,
                    category: trace.category,
                    responseTime: trace.response_time_ms,
                },
            ]);
            if (onNewTrace) onNewTrace();
        } catch (err) {
            setConversation((prev) => [
                ...prev,
                { role: 'error', text: 'Failed to get response. Please try again.' },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="chatbot">
            <div className="chat-container">
                <div className="chat-header">
                    <span className="chat-avatar">🤖</span>
                    <div>
                        <h2>BillEase Support</h2>
                        <span className="chat-status">Online</span>
                    </div>
                </div>

                <div className="chat-messages">
                    {conversation.length === 0 && (
                        <div className="chat-welcome">
                            <div className="welcome-icon">💬</div>
                            <h3>Welcome to BillEase Support</h3>
                            <p>Ask me anything about billing, refunds, account access, or your subscription.</p>
                            <div className="suggestion-chips">
                                {[
                                    "What are your pricing plans?",
                                    "I need a refund",
                                    "I can't log in to my account",
                                    "Cancel my subscription",
                                ].map((s) => (
                                    <button
                                        key={s}
                                        className="chip"
                                        onClick={() => {
                                            setMessage(s);
                                        }}
                                    >
                                        {s}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {conversation.map((msg, i) => (
                        <div key={i} className={`chat-bubble ${msg.role}`}>
                            {msg.role === 'bot' && <span className="bot-avatar">🤖</span>}
                            <div className="bubble-content">
                                <p>{msg.text}</p>
                                {msg.role === 'bot' && (
                                    <div className="bubble-meta">
                                        <span className={`category-badge badge-${msg.category?.toLowerCase().replace(/\s/g, '-')}`}>
                                            {msg.category}
                                        </span>
                                        <span className="response-time">{msg.responseTime}ms</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="chat-bubble bot">
                            <span className="bot-avatar">🤖</span>
                            <div className="bubble-content">
                                <div className="typing-indicator">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                <div className="chat-input-area">
                    <input
                        id="chat-input"
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your message..."
                        disabled={loading}
                    />
                    <button
                        id="chat-send-btn"
                        className="send-btn"
                        onClick={handleSend}
                        disabled={!message.trim() || loading}
                    >
                        ➤
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ChatBot;
