import { useState, Fragment } from 'react';
import TraceDetail from './TraceDetail';
import './TraceTable.css';

function TraceTable({ traces }) {
    const [expandedId, setExpandedId] = useState(null);

    if (traces.length === 0) {
        return (
            <div className="empty-state">
                <span className="empty-icon">📭</span>
                <p>No traces found.</p>
            </div>
        );
    }

    const toggleRow = (id) => {
        setExpandedId(expandedId === id ? null : id);
    };

    const truncate = (text, maxLen = 80) =>
        text.length > maxLen ? text.slice(0, maxLen) + '…' : text;

    const formatTime = (ts) => {
        const d = new Date(ts);
        return d.toLocaleString();
    };

    const categoryClass = (cat) =>
        `category-badge badge-${cat.toLowerCase().replace(/\s/g, '-')}`;

    return (
        <div className="trace-table-wrapper">
            <table className="trace-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>User Message</th>
                        <th>Bot Response</th>
                        <th>Category</th>
                        <th>Response Time</th>
                    </tr>
                </thead>
                <tbody>
                    {traces.map((trace) => (
                        <Fragment key={trace.id}>
                            <tr
                                className={`trace-row ${expandedId === trace.id ? 'expanded' : ''}`}
                                onClick={() => toggleRow(trace.id)}
                            >
                                <td className="col-time">{formatTime(trace.timestamp)}</td>
                                <td className="col-msg">{truncate(trace.user_message)}</td>
                                <td className="col-msg">{truncate(trace.bot_response)}</td>
                                <td>
                                    <span className={categoryClass(trace.category)}>
                                        {trace.category}
                                    </span>
                                </td>
                                <td className="col-rt">{trace.response_time_ms}ms</td>
                            </tr>
                            {expandedId === trace.id && (
                                <tr key={`${trace.id}-detail`} className="trace-detail-row">
                                    <td colSpan="5">
                                        <TraceDetail trace={trace} />
                                    </td>
                                </tr>
                            )}
                        </Fragment>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default TraceTable;
