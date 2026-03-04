import './AggregateStats.css';

const CATEGORY_COLORS = {
    'Billing': '#6366f1',
    'Refund': '#f43f5e',
    'Account Access': '#f59e0b',
    'Cancellation': '#ef4444',
    'General Inquiry': '#22c55e',
};

const CATEGORY_ICONS = {
    'Billing': '💳',
    'Refund': '💸',
    'Account Access': '🔐',
    'Cancellation': '❌',
    'General Inquiry': '❓',
};

function AggregateStats({ analytics }) {
    if (!analytics) return null;

    return (
        <div className="aggregate-stats">
            <div className="stats-row">
                <div className="stat-card total-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-info">
                        <span className="stat-value">{analytics.total_traces}</span>
                        <span className="stat-label">Total Traces</span>
                    </div>
                </div>
                <div className="stat-card time-card">
                    <div className="stat-icon">⏱️</div>
                    <div className="stat-info">
                        <span className="stat-value">{analytics.average_response_time_ms.toFixed(0)}ms</span>
                        <span className="stat-label">Avg Response Time</span>
                    </div>
                </div>
            </div>

            <div className="category-breakdown">
                <h3>Category Breakdown</h3>
                <div className="category-cards">
                    {analytics.categories
                        .sort((a, b) => b.count - a.count)
                        .map((cat) => (
                            <div
                                key={cat.category}
                                className="category-card"
                                style={{ '--cat-color': CATEGORY_COLORS[cat.category] || '#64748b' }}
                            >
                                <div className="cat-header">
                                    <span className="cat-icon">{CATEGORY_ICONS[cat.category] || '📋'}</span>
                                    <span className="cat-name">{cat.category}</span>
                                </div>
                                <div className="cat-stats">
                                    <span className="cat-count">{cat.count}</span>
                                    <span className="cat-pct">{cat.percentage}%</span>
                                </div>
                                <div className="cat-bar">
                                    <div
                                        className="cat-bar-fill"
                                        style={{ width: `${cat.percentage}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                </div>
            </div>
        </div>
    );
}

export default AggregateStats;
