import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  Search, 
  Filter, 
  ArrowUpDown, 
  ShieldAlert, 
  X, 
  UserCheck, 
  ExternalLink, 
  BotMessageSquare, 
  ArrowRight,
  BookOpen
} from 'lucide-react';

export default function Transactions({ 
  selectedTxnId, 
  onSelectCustomer, 
  onOpenCopilot, 
  onOpenRegulatoryRule 
}) {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTxn, setActiveTxn] = useState(null);
  const [activeTxnLoading, setActiveTxnLoading] = useState(false);

  // Filters
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [flaggedOnly, setFlaggedOnly] = useState(false);
  const [countryFilter, setCountryFilter] = useState('');
  const [sortBy, setSortBy] = useState('timestamp');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    loadTransactions();
  }, [search, riskFilter, flaggedOnly, countryFilter, sortBy, sortOrder]);

  useEffect(() => {
    if (selectedTxnId) {
      loadTransactionDetail(selectedTxnId);
    }
  }, [selectedTxnId]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const params = {
        search: search || undefined,
        risk_level: riskFilter || undefined,
        flagged_only: flaggedOnly ? true : undefined,
        destination_country: countryFilter || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        limit: 100
      };
      const data = await api.getTransactions(params);
      setTransactions(data);
    } catch (err) {
      console.error("Failed to load transactions:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadTransactionDetail = async (id) => {
    try {
      setActiveTxnLoading(true);
      const detail = await api.getTransactionDetail(id);
      setActiveTxn(detail);
    } catch (err) {
      console.error(`Failed to load detail for ${id}:`, err);
    } finally {
      setActiveTxnLoading(false);
    }
  };

  return (
    <div className="transactions-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Transaction Monitoring</h1>
          <p className="page-subtitle">Real-time risk scoring, explainable rule breakdown, and behavioral anomalies</p>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="card" style={{ marginBottom: 20, padding: '14px 18px' }}>
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          {/* Search Box */}
          <div className="input-group" style={{ minWidth: 260, flex: 1 }}>
            <Search size={16} color="var(--text-muted)" />
            <input 
              type="text" 
              className="input-field" 
              placeholder="Search by ID, Customer ID, or Merchant..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {search && (
              <X size={14} style={{ cursor: 'pointer' }} onClick={() => setSearch('')} />
            )}
          </div>

          {/* Risk Level Filter */}
          <select 
            className="select-field"
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
          >
            <option value="">All Risk Levels</option>
            <option value="CRITICAL">Critical Risk (85-100)</option>
            <option value="HIGH">High Risk (65-84)</option>
            <option value="MEDIUM">Medium Risk (40-64)</option>
            <option value="LOW">Low Risk (0-39)</option>
          </select>

          {/* Destination Country Filter */}
          <select 
            className="select-field"
            value={countryFilter}
            onChange={(e) => setCountryFilter(e.target.value)}
          >
            <option value="">All Corridors</option>
            <option value="Cayman Islands">Cayman Islands (Offshore)</option>
            <option value="Panama">Panama (Offshore)</option>
            <option value="Vanuatu">Vanuatu (Offshore)</option>
            <option value="Switzerland">Switzerland</option>
            <option value="India">Domestic (India)</option>
          </select>

          {/* Flagged Only Checkbox */}
          <label style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.85rem', color: '#fff', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={flaggedOnly} 
              onChange={(e) => setFlaggedOnly(e.target.checked)} 
            />
            Flagged Only
          </label>

          {/* Sort By */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <ArrowUpDown size={14} color="var(--text-muted)" />
            <select 
              className="select-field"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="timestamp">Sort by Time</option>
              <option value="amount">Sort by Amount</option>
              <option value="risk_score">Sort by Risk Score</option>
            </select>
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            >
              {sortOrder.toUpperCase()}
            </button>
          </div>
        </div>
      </div>

      {/* Transaction Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Txn ID</th>
              <th>Customer</th>
              <th>Amount</th>
              <th>Corridor</th>
              <th>Type / Category</th>
              <th>Risk Score</th>
              <th>Status</th>
              <th>Time</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                  Loading transactions...
                </td>
              </tr>
            ) : transactions.length === 0 ? (
              <tr>
                <td colSpan="9" style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                  No transactions match the selected filters.
                </td>
              </tr>
            ) : (
              transactions.map((tx) => {
                const isSelected = activeTxn?.transaction_id === tx.transaction_id;
                return (
                  <tr 
                    key={tx.transaction_id}
                    className={tx.is_flagged ? 'highlighted-row' : ''}
                    style={{ background: isSelected ? 'rgba(59, 130, 246, 0.15)' : undefined }}
                    onClick={() => loadTransactionDetail(tx.transaction_id)}
                  >
                    <td>
                      <span style={{ fontWeight: 700, color: tx.is_flagged ? '#f87171' : 'var(--accent-blue)', fontFamily: 'var(--font-mono)' }}>
                        {tx.transaction_id}
                      </span>
                    </td>
                    <td>
                      <span 
                        style={{ color: '#93c5fd', cursor: 'pointer', textDecoration: 'underline' }}
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectCustomer(tx.customer_id);
                        }}
                      >
                        {tx.customer_id}
                      </span>
                    </td>
                    <td>
                      <strong style={{ fontSize: '0.95rem' }}>
                        ₹{tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </strong>
                    </td>
                    <td>
                      {tx.source_country} → <strong>{tx.destination_country}</strong>
                    </td>
                    <td>
                      <div>{tx.transaction_type}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{tx.merchant_category || 'General'}</div>
                    </td>
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
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                      {new Date(tx.timestamp).toLocaleString()}
                    </td>
                    <td>
                      <button 
                        className="btn btn-secondary btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          loadTransactionDetail(tx.transaction_id);
                        }}
                      >
                        Explain <ArrowRight size={12} />
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Transaction Details Slide-over Drawer */}
      {activeTxn && (
        <div className="drawer-overlay" onClick={() => setActiveTxn(null)}>
          <div className="drawer-panel" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: 16 }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff' }}>{activeTxn.transaction_id}</h2>
                  <span className={`risk-badge ${activeTxn.risk_level.toLowerCase()}`}>
                    {activeTxn.risk_level} ({activeTxn.risk_score}/100)
                  </span>
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Timestamp: {new Date(activeTxn.timestamp).toUTCString()}
                </div>
              </div>
              <button 
                className="btn btn-secondary btn-sm" 
                onClick={() => setActiveTxn(null)}
                style={{ borderRadius: '50%', width: 32, height: 32, padding: 0 }}
              >
                <X size={16} />
              </button>
            </div>

            {/* Transaction Overview Card */}
            <div className="card" style={{ background: 'var(--bg-input)' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>AMOUNT</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fff' }}>
                    ₹{activeTxn.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>CUSTOMER</div>
                  <div style={{ fontWeight: 600, color: '#93c5fd', cursor: 'pointer' }} onClick={() => onSelectCustomer(activeTxn.customer_id)}>
                    {activeTxn.customer_name} ({activeTxn.customer_id})
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>DESTINATION CORRIDOR</div>
                  <div style={{ fontWeight: 600 }}>{activeTxn.destination_country}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>TYPE & CATEGORY</div>
                  <div style={{ fontWeight: 600 }}>{activeTxn.transaction_type} • {activeTxn.merchant_category}</div>
                </div>
              </div>
            </div>

            {/* EXPLAINABILITY SECTION: Why was it flagged? */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <ShieldAlert size={18} color="var(--risk-critical)" />
                  Explainable Risk Breakdown ({activeTxn.evaluations.length} Rules Triggered)
                </h3>
              </div>

              {activeTxn.evaluations.length === 0 ? (
                <div style={{ padding: 16, background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)', color: '#34d399', fontSize: '0.85rem' }}>
                  No suspicious indicators triggered. Transaction parameters align with normal historical profile.
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  {activeTxn.evaluations.map((ev) => (
                    <div key={ev.evaluation_id} className="rule-eval-card">
                      <div className="rule-eval-header">
                        <span className="rule-name">{ev.rule_name}</span>
                        <span className="rule-score-badge">+{ev.score_contribution} pts</span>
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, fontSize: '0.78rem', background: 'rgba(0,0,0,0.2)', padding: '6px 10px', borderRadius: 4 }}>
                        <div><strong style={{ color: 'var(--text-muted)' }}>Observed:</strong> {ev.observed_value}</div>
                        <div><strong style={{ color: 'var(--text-muted)' }}>Threshold:</strong> {ev.threshold_value}</div>
                      </div>

                      <p className="rule-explanation">{ev.explanation}</p>

                      {ev.regulatory_ref && (
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 4 }}>
                          <span 
                            className="rule-evidence-link"
                            onClick={() => onOpenRegulatoryRule(ev.regulatory_ref)}
                          >
                            <BookOpen size={12} /> Cites Policy: {ev.regulatory_ref}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Quick Actions Footer */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 'auto', paddingTop: 16, borderTop: '1px solid var(--border-color)' }}>
              <button 
                className="btn btn-primary"
                onClick={() => onSelectCustomer(activeTxn.customer_id)}
              >
                <UserCheck size={16} /> Open Customer 360 Profile ({activeTxn.customer_id})
              </button>

              <button 
                className="btn btn-secondary"
                onClick={() => onOpenCopilot(`Why was transaction ${activeTxn.transaction_id} flagged?`)}
              >
                <BotMessageSquare size={16} /> Investigate with Copilot
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
