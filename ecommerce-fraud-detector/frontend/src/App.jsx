import React, { useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

function App() {
  const [formData, setFormData] = useState({
    order_amount: 45.50,
    session_duration_sec: 120,
    click_count: 22
  });

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || 0 });
  };

  const handleSimulate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', formData);
      setHistory([response.data, ...history]);
    } catch (err) {
      alert("Error connecting to backend API.");
    } finally {
      setLoading(false);
    }
  };

  // CSV Export Logic
  const exportToCSV = () => {
    if (history.length === 0) return alert("No transactions to export!");
    
    const headers = "Order Amount ($),Session Duration (s),Click Count,Risk Score (%),Status\n";
    const rows = history.map(item => 
      `${item.details.order_amount},${item.details.session_duration_sec},${item.details.click_count},${item.fraud_probability},"${item.status}"`
    ).join("\n");

    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fraud_audit_log_${Date.now()}.csv`;
    a.click();
  };

  // Prepare data for Scatter Plot (X = Duration, Y = Order Amount)
  const approvedPoints = history
    .filter(i => !i.status.includes('FLAGGED') && !i.status.includes('REVIEW'))
    .map(i => ({ x: i.details.session_duration_sec, y: i.details.order_amount }));

  const reviewPoints = history
    .filter(i => i.status.includes('REVIEW'))
    .map(i => ({ x: i.details.session_duration_sec, y: i.details.order_amount }));

  const flaggedPoints = history
    .filter(i => i.status.includes('FLAGGED'))
    .map(i => ({ x: i.details.session_duration_sec, y: i.details.order_amount }));

  const chartData = {
    datasets: [
      {
        label: 'Approved (Normal)',
        data: approvedPoints,
        backgroundColor: '#52c41a',
        pointRadius: 6,
      },
      {
        label: 'Needs Review',
        data: reviewPoints,
        backgroundColor: '#faad14',
        pointRadius: 6,
      },
      {
        label: 'Flagged (Bot/Fraud)',
        data: flaggedPoints,
        backgroundColor: '#ff4d4f',
        pointRadius: 8,
      },
    ],
  };

  const chartOptions = {
    scales: {
      x: { title: { display: true, text: 'Session Duration (seconds)' } },
      y: { title: { display: true, text: 'Order Amount ($)' } },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: '850px', margin: '40px auto', padding: '0 20px' }}>
      <h2>🛡️ E-Commerce Fraud & Bot Detector</h2>
      <p style={{ color: '#aaa' }}>
        Simulate order checkouts and inspect ML anomaly classifications in real-time.
      </p>

      {/* Input Form */}
      <form onSubmit={handleSimulate} style={{ background: '#1f1f1f', padding: '20px', borderRadius: '8px', color: '#fff', marginBottom: '30px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' }}>
          <div>
            <label><b>Order Amount ($):</b></label>
            <input 
              type="number" 
              name="order_amount" 
              value={formData.order_amount} 
              onChange={handleChange}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          <div>
            <label><b>Session Duration (s):</b></label>
            <input 
              type="number" 
              name="session_duration_sec" 
              value={formData.session_duration_sec} 
              onChange={handleChange}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          <div>
            <label><b>Clicks Before Checkout:</b></label>
            <input 
              type="number" 
              name="click_count" 
              value={formData.click_count} 
              onChange={handleChange}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
        </div>

        <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
          <button type="submit" disabled={loading} style={{ background: '#0070f3', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '5px', cursor: 'pointer' }}>
            {loading ? "Analyzing..." : "Process Checkout"}
          </button>
          
          <button 
            type="button" 
            onClick={() => setFormData({ order_amount: 1450, session_duration_sec: 1.2, click_count: 1 })}
            style={{ background: '#ff4d4f', color: '#fff', border: 'none', padding: '10px 15px', borderRadius: '5px', cursor: 'pointer' }}
          >
            ⚡ Preset: Bot Attack
          </button>

          <button 
            type="button" 
            onClick={() => setFormData({ order_amount: 55, session_duration_sec: 180, click_count: 28 })}
            style={{ background: '#52c41a', color: '#fff', border: 'none', padding: '10px 15px', borderRadius: '5px', cursor: 'pointer' }}
          >
            👤 Preset: Normal Human
          </button>
        </div>
      </form>

      {/* Visual Chart Section */}
      {history.length > 0 && (
        <div style={{ background: '#fff', padding: '20px', borderRadius: '8px', marginBottom: '30px', border: '1px solid #ddd' }}>
          <h3>📊 Real-Time Cluster Visualization</h3>
          <div style={{ height: '300px' }}>
            <Scatter data={chartData} options={chartOptions} />
          </div>
        </div>
      )}

      {/* Audit Log Header & Export Button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3>Audit Log ({history.length})</h3>
        {history.length > 0 && (
          <button onClick={exportToCSV} style={{ background: '#333', color: '#fff', border: 'none', padding: '8px 12px', borderRadius: '5px', cursor: 'pointer' }}>
            📥 Export CSV
          </button>
        )}
      </div>

      {/* Log Feed */}
      {history.length === 0 ? (
        <p style={{ color: '#888' }}>No transactions evaluated yet. Submit a test above!</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {history.map((item, index) => (
            <div 
              key={index} 
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '15px',
                borderRadius: '6px',
                borderLeft: `6px solid ${
                  item.status.includes('FLAGGED') ? '#ff4d4f' : item.status.includes('REVIEW') ? '#faad14' : '#52c41a'
                }`,
                background: '#fff',
                boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
              }}
            >
              <div>
                <strong>${item.details.order_amount}</strong> | Session: {item.details.session_duration_sec}s | Clicks: {item.details.click_count}
                <br />
                <small style={{ color: '#666' }}>
                  Risk Score: <b>{item.fraud_probability}%</b> | DBSCAN Outlier: <b>{item.is_anomaly ? "Yes" : "No"}</b>
                </small>
              </div>

              <div style={{ fontWeight: 'bold' }}>
                {item.status.includes('FLAGGED') && <span style={{ color: '#ff4d4f' }}>🚨 FLAGGED</span>}
                {item.status.includes('REVIEW') && <span style={{ color: '#faad14' }}>⚠️ REVIEW</span>}
                {item.status.includes('APPROVED') && <span style={{ color: '#52c41a' }}>✅ APPROVED</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;