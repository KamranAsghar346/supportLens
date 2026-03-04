import { useState, useEffect, useCallback } from 'react';
import { getTraces, getAnalytics } from '../api';
import AggregateStats from './AggregateStats';
import TraceTable from './TraceTable';
import './Dashboard.css';

function Dashboard({ refreshKey }) {
    const [traces, setTraces] = useState([]);
    const [analytics, setAnalytics] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const [tracesData, analyticsData] = await Promise.all([
                getTraces(selectedCategory || null),
                getAnalytics(),
            ]);
            setTraces(tracesData);
            setAnalytics(analyticsData);
        } catch (err) {
            console.error('Failed to fetch data:', err);
        } finally {
            setLoading(false);
        }
    }, [selectedCategory]);

    useEffect(() => {
        fetchData();
    }, [fetchData, refreshKey]);

    const categories = [
        'Billing',
        'Refund',
        'Account Access',
        'Cancellation',
        'General Inquiry',
    ];

    return (
        <div className="dashboard">
            {analytics && <AggregateStats analytics={analytics} />}

            <div className="traces-section">
                <div className="traces-header">
                    <h2>Trace Log</h2>
                    <div className="traces-controls">
                        <select
                            id="category-filter"
                            className="category-filter"
                            value={selectedCategory}
                            onChange={(e) => setSelectedCategory(e.target.value)}
                        >
                            <option value="">All Categories</option>
                            {categories.map((cat) => (
                                <option key={cat} value={cat}>
                                    {cat}
                                </option>
                            ))}
                        </select>
                        <button className="refresh-btn" onClick={fetchData} disabled={loading}>
                            {loading ? '⟳' : '↻'} Refresh
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div className="loading-state">
                        <div className="spinner"></div>
                        <p>Loading traces...</p>
                    </div>
                ) : (
                    <TraceTable traces={traces} />
                )}
            </div>
        </div>
    );
}

export default Dashboard;
