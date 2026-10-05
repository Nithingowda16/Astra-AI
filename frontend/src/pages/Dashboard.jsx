import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { 
  ShieldAlert, 
  AlertTriangle, 
  Users, 
  FileCheck2, 
  ArrowUpRight, 
  Globe2, 
  TrendingUp, 
  Activity,
  ArrowRight,
  ExternalLink
} from 'lucide-react';

export default function Dashboard({ onSelectTransaction, onSelectCustomer, onOpenCopilot }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '60px 0', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <Activity className="animate-spin" size={32} style={{ margin: '0 auto 16px', color: 'var(--accent-blue)' }} />
        <p>Loading real-time executive risk intelligence...</p>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="card" style={{ borderColor: 'var(--risk-critical)', color: 'var(--risk-critical)' }}>
        <AlertTriangle size={24} style={{ marginBottom: 8 }} />
        <p>Failed to load dashboard data: {error}</p>
        <button className="btn btn-secondary btn-sm" style={{ marginTop: 12 }} onClick={loadStats}>Retry</button>
      </div>
    );
  }

  const { risk_distribution } = stats;
  const totalRiskCount = (risk_distribution.low + risk_distribution.medium + risk_distribution.high + risk_distribution.critical) || 1;

  return (
    <div className="dashboard-page">
      {/* Top Banner with Alert Highlight */}
      <div className="card" style={{ 
        marginBottom: 24, 
        background: 'linear-gradient(90deg, rgba(29, 78, 216, 0.18), rgba(6, 182, 212, 0.1))',
        borderColor: 'rgba(59, 130, 246, 0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 16
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
            <span className="risk-badge critical">Active Alert</span>
            <span style={{ fontWeight: 700, color: '#fff', fontSize: '1.05rem' }}>
              High-Risk Transfer Detected: TXN-1024 (₹12,50,000.00 to Cayman Islands)
            </span>
          </div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Customer <strong>Vikramaditya Singhania (CUST-1008)</strong> triggered Statutory AML Rule 01 (Large Value CDD) and Rule 03 (High-Risk Jurisdiction).
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button 
            className="btn btn-primary btn-sm" 
            onClick={() => onSelectTransaction('TXN-1024')}
          >
            Review TXN-1024 <ArrowRight size={14} />
          </button>
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={() => onOpenCopilot('Why was transaction TXN-1024 flagged?')}
          >
            Ask Copilot
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Total Transactions</span>
            <div className="kpi-icon" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa' }}>
              <Activity size={20} />
            </div>
          </div>
          <div className="kpi-value">{stats.total_transactions}</div>
          <div className="kpi-subtext">Monitored Volume: ₹{stats.total_monitored_volume.toLocaleString('en-IN')}</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Suspicious Transactions</span>
            <div className="kpi-icon" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171' }}>
              <AlertTriangle size={20} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#f87171' }}>
            {stats.suspicious_transactions}
            <span style={{ fontSize: '1rem', fontWeight: 500, color: 'var(--text-secondary)', marginLeft: 8 }}>
              ({stats.suspicious_percentage}%)
            </span>
          </div>
          <div className="kpi-subtext">Triggered explainable rule thresholds</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">High-Risk Customers</span>
            <div className="kpi-icon" style={{ background: 'rgba(249, 115, 22, 0.15)', color: '#fb923c' }}>
              <Users size={20} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#fb923c' }}>{stats.high_risk_customers}</div>
          <div className="kpi-subtext">Subject to Enhanced Due Diligence (EDD)</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-label">Open Investigations</span>
            <div className="kpi-icon" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
              <FileCheck2 size={20} />
            </div>
          </div>
          <div className="kpi-value">{stats.open_investigations}</div>
          <div className="kpi-subtext">Active cases under compliance review</div>
        </div>
      </div>

      {/* Middle Section: Risk Distribution & 14-Day Trend Chart */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.6fr', gap: 24, marginBottom: 24 }}>
        {/* Risk Score Distribution */}
        <div className="card">
          <div className="card-title">
            <span>Risk Score Distribution</span>
            <ShieldAlert size={18} color="var(--accent-cyan)" />
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: 4 }}>
                <span style={{ color: '#f87171', fontWeight: 600 }}>Critical Risk (85-100)</span>
                <span style={{ fontWeight: 700 }}>{risk_distribution.critical} txns</span>
              </div>
              <div style={{ width: '100%', height: 8, background: 'var(--border-color)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(risk_distribution.critical / totalRiskCount) * 100}%`, height: '100%', background: 'var(--risk-critical)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: 4 }}>
                <span style={{ color: '#fb923c', fontWeight: 600 }}>High Risk (65-84)</span>
                <span style={{ fontWeight: 700 }}>{risk_distribution.high} txns</span>
              </div>
              <div style={{ width: '100%', height: 8, background: 'var(--border-color)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(risk_distribution.high / totalRiskCount) * 100}%`, height: '100%', background: 'var(--risk-high)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: 4 }}>
                <span style={{ color: '#facc15', fontWeight: 600 }}>Medium Risk (40-64)</span>
                <span style={{ fontWeight: 700 }}>{risk_distribution.medium} txns</span>
              </div>
              <div style={{ width: '100%', height: 8, background: 'var(--border-color)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(risk_distribution.medium / totalRiskCount) * 100}%`, height: '100%', background: 'var(--risk-medium)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: 4 }}>
                <span style={{ color: '#34d399', fontWeight: 600 }}>Low Risk (0-39)</span>
                <span style={{ fontWeight: 700 }}>{risk_distribution.low} txns</span>
              </div>
              <div style={{ width: '100%', height: 8, background: 'var(--border-color)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(risk_distribution.low / totalRiskCount) * 100}%`, height: '100%', background: 'var(--risk-low)' }} />
              </div>
            </div>
          </div>

          <div style={{ marginTop: 24, padding: 12, background: 'rgba(255, 255, 255, 0.03)', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Evaluated by the <strong>Deterministic Risk Engine</strong> using baseline deviation, FATF corridor checks, and burst frequency.
          </div>
        </div>

        {/* 14-Day Suspicious Activity Trend Chart */}
        <div className="card">
          <div className="card-title">
            <span>Suspicious Volume & Alerts Timeline (14 Days)</span>
            <TrendingUp size={18} color="var(--accent-blue)" />
          </div>

          <div style={{ height: 200, display: 'flex', alignItems: 'flex-end', gap: 8, padding: '16px 0 8px' }}>
            {stats.volume_trends.map((item, idx) => {
              const maxVol = Math.max(...stats.volume_trends.map(t => t.total_volume), 1);
              const heightPct = Math.max(8, Math.round((item.total_volume / maxVol) * 100));
              const hasFlagged = item.suspicious_count > 0;
              return (
                <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end' }}>
                  <div 
                    title={`${item.date}: ₹${item.total_volume.toLocaleString()} total, ${item.suspicious_count} flagged`}
                    style={{ 
                      width: '100%', 
                      height: `${heightPct}%`, 
                      background: hasFlagged ? 'linear-gradient(180deg, #ef4444 0%, #b91c1c 100%)' : 'linear-gradient(180deg, #3b82f6 0%, #1d4ed8 100%)',
                      borderRadius: '4px 4px 0 0',
                      transition: 'all 0.2s ease',
                      position: 'relative',
                      cursor: 'pointer'
                    }} 
                  >
                    {hasFlagged && (
                      <span style={{ 
                        position: 'absolute', 
                        top: -18, 
                        left: '50%', 
                        transform: 'translateX(-50%)', 
                        fontSize: '0.68rem', 
                        fontWeight: 700, 
                        color: '#f87171' 
                      }}>
                        {item.suspicious_count}
                      </span>
                    )}
                  </div>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: 6, transform: 'rotate(-30deg)', whiteSpace: 'nowrap' }}>
                    {item.date}
                  </span>
                </div>
              );
            })}
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: 20, marginTop: 18, fontSize: '0.78rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--text-secondary)' }}>
              <span style={{ width: 10, height: 10, background: '#3b82f6', borderRadius: 2 }}></span> Normal Transactions
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6, color: '#f87171', fontWeight: 600 }}>
              <span style={{ width: 10, height: 10, background: '#ef4444', borderRadius: 2 }}></span> Suspicious / Flagged Activity
            </span>
          </div>
        </div>
      </div>

      {/* Bottom Section: Priority Alerts Feed & Country Risk Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 24 }}>
        {/* Priority Alerts Feed */}
        <div className="card">
          <div className="card-title">
            <span>Priority Risk Alerts</span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Latest Triggered Events</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {stats.recent_alerts.map((alert) => (
              <div 
                key={alert.alert_id}
                onClick={() => onSelectTransaction(alert.transaction_id)}
                style={{ 
                  background: 'var(--bg-input)', 
                  border: '1px solid var(--border-color)', 
                  borderRadius: 'var(--radius-sm)', 
                  padding: '12px 16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  transition: 'background 0.15s ease'
                }}
                className="hover-card"
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span className={`risk-badge ${alert.severity.toLowerCase()}`}>
                    {alert.severity}
                  </span>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#fff' }}>
                      {alert.alert_type}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      <strong>{alert.customer_name}</strong> • ₹{alert.transaction_amount?.toLocaleString('en-IN')} to {alert.destination_country}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--accent-cyan)', fontWeight: 600 }}>
                    {alert.transaction_id}
                  </span>
                  <ExternalLink size={14} color="var(--text-muted)" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* High-Risk Geographic Corridors */}
        <div className="card">
          <div className="card-title">
            <span>Monitored Corridors</span>
            <Globe2 size={18} color="var(--accent-cyan)" />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {stats.country_risk_breakdown.map((c, i) => (
              <div 
                key={i} 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  padding: '10px 12px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.88rem', color: '#fff' }}>
                    {c.country}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    {c.transaction_count} transactions total
                  </div>
                </div>

                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: c.high_risk_count > 0 ? '#f87171' : '#34d399' }}>
                    {c.high_risk_count > 0 ? `${c.high_risk_count} Flagged` : '0 Flagged'}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    ₹{c.total_volume.toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
