import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  Users, 
  Search, 
  ShieldAlert, 
  Clock, 
  AlertTriangle, 
  FileText, 
  BotMessageSquare, 
  CheckCircle2, 
  ArrowRight,
  TrendingUp,
  UserCheck
} from 'lucide-react';

export default function Customers({ 
  selectedCustomerId, 
  onSelectCustomer, 
  onSelectTransaction, 
  onOpenCopilot,
  onCreateInvestigation 
}) {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [activeCustId, setActiveCustId] = useState(selectedCustomerId || 'CUST-1008');
  const [customerDetail, setCustomerDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    loadCustomers();
  }, [search]);

  useEffect(() => {
    if (selectedCustomerId) {
      setActiveCustId(selectedCustomerId);
    }
  }, [selectedCustomerId]);

  useEffect(() => {
    if (activeCustId) {
      loadCustomerDetail(activeCustId);
    }
  }, [activeCustId]);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const data = await api.getCustomers({ search: search || undefined });
      setCustomers(data);
      if (!activeCustId && data.length > 0) {
        setActiveCustId(data[0].customer_id);
      }
    } catch (err) {
      console.error("Failed to load customers:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadCustomerDetail = async (id) => {
    try {
      setDetailLoading(true);
      const detail = await api.getCustomerDetail(id);
      setCustomerDetail(detail);
    } catch (err) {
      console.error(`Failed to load customer detail for ${id}:`, err);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="customers-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Customer Risk Intelligence</h1>
          <p className="page-subtitle">360-degree compliance profiles, historical baselines, and chronological activity timelines</p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: 24 }}>
        {/* Left Sidebar: Customer Directory */}
        <div className="card" style={{ padding: 18, height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
          <div className="input-group" style={{ marginBottom: 14 }}>
            <Search size={16} color="var(--text-muted)" />
            <input 
              type="text" 
              className="input-field" 
              placeholder="Search customers..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 8 }}>
            {loading ? (
              <div style={{ textAlign: 'center', padding: 20, color: 'var(--text-muted)' }}>Loading...</div>
            ) : (
              customers.map((c) => {
                const isSelected = activeCustId === c.customer_id;
                return (
                  <div
                    key={c.customer_id}
                    onClick={() => {
                      setActiveCustId(c.customer_id);
                      if (onSelectCustomer) onSelectCustomer(c.customer_id);
                    }}
                    style={{
                      padding: '12px 14px',
                      background: isSelected ? 'rgba(59, 130, 246, 0.16)' : 'var(--bg-input)',
                      border: isSelected ? '1px solid var(--accent-blue)' : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
                      <span style={{ fontWeight: 600, color: isSelected ? '#93c5fd' : '#fff', fontSize: '0.9rem' }}>
                        {c.full_name}
                      </span>
                      <span className={`risk-badge ${c.risk_level.toLowerCase()}`}>
                        {c.risk_score}
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      <span>{c.customer_id} • {c.occupation}</span>
                      {c.is_pep && <span style={{ color: '#fb923c', fontWeight: 700 }}>PEP</span>}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Content: Customer 360 Risk Profile */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {detailLoading || !customerDetail ? (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              Loading customer dossier...
            </div>
          ) : (
            <>
              {/* Customer Header Card */}
              <div className="card" style={{ background: 'var(--kpi-gradient)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 6 }}>
                      <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                        {customerDetail.full_name}
                      </h2>
                      <span className={`risk-badge ${customerDetail.risk_level.toLowerCase()}`}>
                        {customerDetail.risk_level} RISK ({customerDetail.risk_score}/100)
                      </span>
                      {customerDetail.is_pep && (
                        <span className="risk-badge high">Politically Exposed Person (PEP)</span>
                      )}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                      {customerDetail.customer_id} • {customerDetail.occupation} • {customerDetail.country} • Account: <strong>{customerDetail.account_type}</strong> • KYC: <strong>{customerDetail.kyc_status}</strong>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: 10 }}>
                    <button 
                      className="btn btn-secondary btn-sm"
                      onClick={() => onOpenCopilot(`Why is customer ${customerDetail.customer_id} considered high risk?`)}
                    >
                      <BotMessageSquare size={14} /> Ask Copilot Why
                    </button>
                    <button 
                      className="btn btn-primary btn-sm"
                      onClick={() => onCreateInvestigation(customerDetail)}
                    >
                      <FileText size={14} /> Open Investigation
                    </button>
                  </div>
                </div>

                {/* Baseline vs Current Deviation Cards */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14, marginTop: 20 }}>
                  <div style={{ background: 'var(--bg-input)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Historical Baseline Avg</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff', marginTop: 4 }}>
                      ₹{customerDetail.baseline_avg_amount.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: '#38bdf8' }}>Declared Normal Profile</div>
                  </div>

                  <div style={{ background: 'var(--bg-input)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Monthly Volume Cap</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff', marginTop: 4 }}>
                      ₹{customerDetail.baseline_monthly_volume.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>30-day baseline threshold</div>
                  </div>

                  <div style={{ background: 'var(--bg-input)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Total Observed Flow</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: 700, color: customerDetail.flagged_transaction_count > 0 ? '#f87171' : '#fff', marginTop: 4 }}>
                      ₹{customerDetail.total_volume.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{customerDetail.transaction_count} total transfers</div>
                  </div>

                  <div style={{ background: 'var(--bg-input)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Suspicious Flagged</div>
                    <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#f87171', marginTop: 4 }}>
                      {customerDetail.flagged_transaction_count} Transfers
                    </div>
                    <div style={{ fontSize: '0.72rem', color: '#f87171' }}>Exceeding risk limit</div>
                  </div>
                </div>
              </div>

              {/* Suspicious Activity Chronological Timeline */}
              <div className="card">
                <div className="card-title">
                  <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Clock size={18} color="var(--accent-blue)" />
                    Chronological Risk & Suspicious Activity Timeline
                  </span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {customerDetail.timeline.length} Recorded Incidents
                  </span>
                </div>

                {customerDetail.timeline.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No suspicious activity recorded for this customer profile.</p>
                ) : (
                  <div className="timeline">
                    {customerDetail.timeline.map((event, idx) => (
                      <div key={idx} className="timeline-item">
                        <div className={`timeline-dot ${event.severity.toLowerCase()}`}>
                          <AlertTriangle size={10} color={event.severity === 'CRITICAL' ? '#ef4444' : '#f97316'} />
                        </div>
                        <div className="timeline-content">
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                            <span className="timeline-date">{new Date(event.timestamp).toLocaleString()}</span>
                            <span className={`risk-badge ${event.severity.toLowerCase()}`}>{event.severity}</span>
                          </div>
                          <div className="timeline-title">{event.title}</div>
                          <div className="timeline-desc">{event.description}</div>
                          {event.reference_id && event.reference_id.startsWith('TXN') && (
                            <div style={{ marginTop: 8 }}>
                              <button 
                                className="btn btn-secondary btn-sm"
                                onClick={() => onSelectTransaction(event.reference_id)}
                              >
                                View Flagged Transfer {event.reference_id} <ArrowRight size={12} />
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Recent Transactions Table */}
              <div className="card">
                <div className="card-title">
                  <span>Recent Transaction History</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Latest Transfers</span>
                </div>

                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Txn ID</th>
                        <th>Amount</th>
                        <th>Destination</th>
                        <th>Category</th>
                        <th>Risk Score</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {customerDetail.recent_transactions.map((tx) => (
                        <tr 
                          key={tx.transaction_id}
                          className={tx.is_flagged ? 'highlighted-row' : ''}
                          onClick={() => onSelectTransaction(tx.transaction_id)}
                        >
                          <td style={{ fontWeight: 700, color: tx.is_flagged ? '#f87171' : 'var(--accent-blue)', fontFamily: 'var(--font-mono)' }}>
                            {tx.transaction_id}
                          </td>
                          <td><strong>₹{tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong></td>
                          <td>{tx.destination_country}</td>
                          <td>{tx.merchant_category || 'General'}</td>
                          <td>
                            <span className={`risk-badge ${tx.risk_level.toLowerCase()}`}>
                              {tx.risk_level} ({tx.risk_score})
                            </span>
                          </td>
                          <td>
                            <span className={`status-badge ${tx.status.toLowerCase().replace(' ', '-')}`}>
                              {tx.status}
                            </span>
                          </td>
                          <td>
                            <button 
                              className="btn btn-secondary btn-sm"
                              onClick={(e) => {
                                e.stopPropagation();
                                onSelectTransaction(tx.transaction_id);
                              }}
                            >
                              Explain
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
