import './TraceDetail.css';

function TraceDetail({ trace }) {
    return (
        <div className="trace-detail">
            <div className="detail-section">
                <h4>👤 User Message</h4>
                <p className="detail-text">{trace.user_message}</p>
            </div>
            <div className="detail-section">
                <h4>🤖 Bot Response</h4>
                <p className="detail-text">{trace.bot_response}</p>
            </div>
            <div className="detail-meta">
                <span>
                    <strong>Category:</strong>{' '}
                    <span className={`category-badge badge-${trace.category.toLowerCase().replace(/\s/g, '-')}`}>
                        {trace.category}
                    </span>
                </span>
                <span><strong>Response Time:</strong> {trace.response_time_ms}ms</span>
                <span><strong>ID:</strong> {trace.id}</span>
            </div>
        </div>
    );
}

export default TraceDetail;
