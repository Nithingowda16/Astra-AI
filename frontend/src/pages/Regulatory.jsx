import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  BookOpen, 
  Search, 
  Filter, 
  ShieldCheck, 
  AlertCircle, 
  ExternalLink,
  BotMessageSquare,
  FileText
} from 'lucide-react';

export default function Regulatory({ onOpenCopilot }) {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedRule, setSelectedRule] = useState(null);

  useEffect(() => {
    loadRules();
  }, [search]);

  const loadRules = async () => {
    try {
      setLoading(true);
      const data = await api.getRegulatoryRules({ search: search || undefined });
      setRules(data);
      if (data.length > 0 && !selectedRule) {
        setSelectedRule(data[0]);
      }
    } catch (err) {
      console.error("Failed to load regulatory rules:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="regulatory-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Regulatory Knowledge Base</h1>
          <p className="page-subtitle">
            Authoritative compliance statutory framework, FATF guidance, and automated evidence links
          </p>
        </div>

        <div className="regulatory-status-pill">
          <ShieldCheck size={14} color="#06b6d4" />
          <span>Statutory Framework v1.0</span>
        </div>
      </div>

      {/* Prominent Framework Verification Banner */}
      <div className="card" style={{ 
        marginBottom: 20, 
        background: 'rgba(6, 182, 212, 0.08)', 
        borderColor: 'rgba(6, 182, 212, 0.25)',
        display: 'flex',
        alignItems: 'center',
        gap: 12
      }}>
        <AlertCircle size={20} color="#38bdf8" />
        <div style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>
          <strong>Notice:</strong> This repository represents the active <strong>Regulatory Knowledge Base</strong> with verified AML & financial crime policies indexed for automated evidentiary retrieval and explainable compliance reporting.
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '380px 1fr', gap: 24 }}>
        {/* Left: Rules Catalog */}
        <div className="card" style={{ padding: 18, height: 'calc(100vh - 230px)', display: 'flex', flexDirection: 'column' }}>
          <div className="input-group" style={{ marginBottom: 14 }}>
            <Search size={16} color="var(--text-muted)" />
            <input 
              type="text" 
              className="input-field" 
              placeholder="Search regulatory rules..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
            {loading ? (
              <div style={{ textAlign: 'center', padding: 20, color: 'var(--text-muted)' }}>Loading rules...</div>
            ) : (
              rules.map((r) => {
                const isSelected = selectedRule?.doc_id === r.doc_id;
                return (
                  <div
                    key={r.doc_id}
                    onClick={() => setSelectedRule(r)}
                    style={{
                      padding: '12px 14px',
                      background: isSelected ? 'rgba(6, 182, 212, 0.14)' : 'var(--bg-input)',
                      border: isSelected ? '1px solid #06b6d4' : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontWeight: 700, color: isSelected ? '#38bdf8' : '#fff', fontSize: '0.88rem' }}>
                        {r.doc_id}
                      </span>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        {r.category}
                      </span>
                    </div>

                    <div style={{ fontWeight: 600, fontSize: '0.84rem', color: '#e2e8f0', lineHeight: 1.35 }}>
                      {r.title}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right: Single Rule Inspection View */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {!selectedRule ? (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              Select a regulatory rule from the directory to inspect its legal clauses and triggers.
            </div>
          ) : (
            <div className="card" style={{ background: 'var(--kpi-gradient)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16, borderBottom: '1px solid var(--border-color)', paddingBottom: 16 }}>
                <div>
                  <span className="risk-badge low" style={{ marginBottom: 6 }}>
                    {selectedRule.category}
                  </span>
                  <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: 4 }}>
                    {selectedRule.title}
                  </h2>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                    Issuing Authority: <strong>{selectedRule.authority}</strong>
                  </div>
                </div>

                <button 
                  className="btn btn-secondary btn-sm"
                  onClick={() => onOpenCopilot(`Show the regulatory evidence and details for ${selectedRule.doc_id}`)}
                >
                  <BotMessageSquare size={14} /> Query with Copilot
                </button>
              </div>

              {/* Summary */}
              <div style={{ marginTop: 20 }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: 6 }}>
                  Statutory Summary
                </div>
                <div style={{ fontSize: '0.92rem', color: '#cbd5e1', lineHeight: 1.55 }}>
                  {selectedRule.summary}
                </div>
              </div>

              {/* Full Statutory Clause */}
              <div style={{ marginTop: 20 }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: 6 }}>
                  Operative Clause Text
                </div>
                <div style={{ 
                  background: 'var(--bg-input)', 
                  border: '1px solid var(--border-color)', 
                  borderRadius: 'var(--radius-sm)', 
                  padding: 16, 
                  fontFamily: 'var(--font-mono)', 
                  fontSize: '0.82rem', 
                  color: '#94a3b8', 
                  lineHeight: 1.6 
                }}>
                  {selectedRule.full_clause}
                </div>
              </div>

              {/* Monitored Scenarios */}
              <div style={{ marginTop: 20, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <div style={{ background: 'rgba(255,255,255,0.02)', padding: 14, borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700, textTransform: 'uppercase', marginBottom: 4 }}>
                    Monitored Scenarios
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>
                    {selectedRule.monitored_scenarios}
                  </div>
                </div>

                <div style={{ background: 'rgba(239, 68, 68, 0.05)', padding: 14, borderRadius: 'var(--radius-sm)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                  <div style={{ fontSize: '0.78rem', color: '#f87171', fontWeight: 700, textTransform: 'uppercase', marginBottom: 4 }}>
                    Mandatory Compliance Action
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#fca5a5' }}>
                    {selectedRule.recommended_compliance_action}
                  </div>
                </div>
              </div>

              <div style={{ marginTop: 24, paddingTop: 14, borderTop: '1px solid var(--border-color)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {selectedRule.disclaimer}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
