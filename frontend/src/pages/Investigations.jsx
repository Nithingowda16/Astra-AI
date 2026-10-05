import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  FileSearch, 
  PlusCircle, 
  Printer, 
  Download, 
  Send, 
  CheckCircle2, 
  Clock, 
  ShieldAlert, 
  FileText, 
  X,
  BookOpen,
  ArrowRight
} from 'lucide-react';

export default function Investigations({ 
  onSelectCustomer, 
  onSelectTransaction,
  incomingCaseData
}) {
  const [investigations, setInvestigations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeInvId, setActiveInvId] = useState('INV-2024-008');
  const [activeInv, setActiveInv] = useState(null);
  const [report, setReport] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);

  // New Note state
  const [newNote, setNewNote] = useState('');
  const [savingNote, setSavingNote] = useState(false);

  // New Case Modal state
  const [showNewCaseModal, setShowNewCaseModal] = useState(false);
  const [newCaseForm, setNewCaseForm] = useState({
    title: '',
    customer_id: '',
    primary_transaction_id: '',
    priority: 'High',
    assigned_analyst: 'Senior Compliance Officer',
    summary: '',
    analyst_notes: ''
  });

  useEffect(() => {
    loadInvestigations();
  }, []);

  useEffect(() => {
    if (incomingCaseData) {
      setNewCaseForm({
        title: `Investigation into ${incomingCaseData.full_name || incomingCaseData.customer_id}`,
        customer_id: incomingCaseData.customer_id || '',
        primary_transaction_id: incomingCaseData.primary_transaction_id || '',
        priority: 'High',
        assigned_analyst: 'Senior Compliance Officer',
        summary: incomingCaseData.summary || `Escalation regarding customer ${incomingCaseData.customer_id}.`,
        analyst_notes: 'Initial intake from compliance triage.'
      });
      setShowNewCaseModal(true);
    }
  }, [incomingCaseData]);

  useEffect(() => {
    if (activeInvId) {
      loadInvestigationDetail(activeInvId);
    }
  }, [activeInvId]);

  const loadInvestigations = async () => {
    try {
      setLoading(true);
      const data = await api.getInvestigations();
      setInvestigations(data);
      if (!activeInvId && data.length > 0) {
        setActiveInvId(data[0].investigation_id);
      }
    } catch (err) {
      console.error("Failed to load investigations:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadInvestigationDetail = async (id) => {
    try {
      const data = await api.getInvestigationDetail(id);
      setActiveInv(data);
    } catch (err) {
      console.error(`Failed to load investigation ${id}:`, err);
    }
  };

  const handleStatusChange = async (newStatus) => {
    if (!activeInv) return;
    try {
      const updated = await api.updateInvestigation(activeInv.investigation_id, { status: newStatus });
      setActiveInv(updated);
      loadInvestigations();
    } catch (err) {
      alert(`Error updating status: ${err.message}`);
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!newNote.trim() || !activeInv) return;
    try {
      setSavingNote(true);
      const updated = await api.updateInvestigation(activeInv.investigation_id, { new_note: newNote.trim() });
      setActiveInv(updated);
      setNewNote('');
    } catch (err) {
      alert(`Error saving note: ${err.message}`);
    } finally {
      setSavingNote(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!activeInv) return;
    try {
      setReportLoading(true);
      const rep = await api.getInvestigationReport(activeInv.investigation_id);
      setReport(rep);
      setShowReportModal(true);
    } catch (err) {
      alert(`Error generating report: ${err.message}`);
    } finally {
      setReportLoading(false);
    }
  };

  const handleCreateCaseSubmit = async (e) => {
    e.preventDefault();
    try {
      const created = await api.createInvestigation(newCaseForm);
      setShowNewCaseModal(false);
      await loadInvestigations();
      setActiveInvId(created.investigation_id);
    } catch (err) {
      alert(`Failed to create investigation: ${err.message}`);
    }
  };

  return (
    <div className="investigations-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Investigation Workflow & Case Management</h1>
          <p className="page-subtitle">Evidence correlation, audit trail logs, and formal compliance report generator</p>
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => {
            setNewCaseForm({
              title: 'Suspicious Fund Diversion Case',
              customer_id: 'CUST-1008',
              primary_transaction_id: 'TXN-1024',
              priority: 'High',
              assigned_analyst: 'Senior Compliance Officer',
              summary: 'Investigation into offshore transactions to Cayman Islands.',
              analyst_notes: 'Initial intake.'
            });
            setShowNewCaseModal(true);
          }}
        >
          <PlusCircle size={16} /> New Investigation Case
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: 24 }}>
        {/* Left: Cases List */}
        <div className="card" style={{ padding: 18, height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
          <div className="card-title">
            <span>Active Cases</span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{investigations.length} cases</span>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
            {loading ? (
              <div style={{ textAlign: 'center', padding: 20, color: 'var(--text-muted)' }}>Loading cases...</div>
            ) : (
              investigations.map((inv) => {
                const isSelected = activeInvId === inv.investigation_id;
                return (
                  <div
                    key={inv.investigation_id}
                    onClick={() => setActiveInvId(inv.investigation_id)}
                    style={{
                      padding: '12px 14px',
                      background: isSelected ? 'rgba(59, 130, 246, 0.16)' : 'var(--bg-input)',
                      border: isSelected ? '1px solid var(--accent-blue)' : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontWeight: 700, color: isSelected ? '#93c5fd' : '#fff', fontSize: '0.88rem' }}>
                        {inv.investigation_id}
                      </span>
                      <span className={`status-badge ${inv.status.toLowerCase().replace(' ', '-')}`}>
                        {inv.status}
                      </span>
                    </div>

                    <div style={{ fontWeight: 600, fontSize: '0.85rem', color: '#e2e8f0', marginBottom: 4 }}>
                      {inv.title}
                    </div>

                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Customer: <strong style={{ color: '#cbd5e1' }}>{inv.customer_name}</strong> • Priority: {inv.priority}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right: Active Case Detail & Workflow */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {!activeInv ? (
            <div className="card" style={{ padding: 40, textAlign: 'center', color: 'var(--text-muted)' }}>
              Select a case to inspect evidence and workflow.
            </div>
          ) : (
            <>
              {/* Case Header Card */}
              <div className="card" style={{ background: 'var(--kpi-gradient)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
                      <span style={{ fontWeight: 800, fontSize: '1.25rem', color: 'var(--text-primary)' }}>
                        {activeInv.investigation_id}: {activeInv.title}
                      </span>
                      <span className={`status-badge ${activeInv.status.toLowerCase().replace(' ', '-')}`}>
                        {activeInv.status}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      Assigned Officer: <strong>{activeInv.assigned_analyst}</strong> • Priority: <strong>{activeInv.priority}</strong> • Created: {new Date(activeInv.created_at).toLocaleString()}
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: 10 }}>
                    <button 
                      className="btn btn-primary"
                      onClick={handleGenerateReport}
                      disabled={reportLoading}
                    >
                      <FileText size={16} /> Generate Compliance Report
                    </button>
                  </div>
                </div>

                {/* Workflow Status Picker */}
                <div style={{ marginTop: 20, paddingTop: 16, borderTop: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Update Case Status:</span>
                  {['Open', 'Under Review', 'Escalated', 'Resolved', 'False Positive'].map((st) => (
                    <button
                      key={st}
                      className={`btn btn-sm ${activeInv.status === st ? 'btn-primary' : 'btn-secondary'}`}
                      onClick={() => handleStatusChange(st)}
                    >
                      {st}
                    </button>
                  ))}
                </div>
              </div>

              {/* Case Context & Evidence Links */}
              <div className="card">
                <div className="card-title">
                  <span>Target Profile & Evidence Links</span>
                  <ShieldAlert size={18} color="var(--accent-cyan)" />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                  <div style={{ background: 'var(--bg-input)', padding: 14, borderRadius: 'var(--radius-sm)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>CUSTOMER UNDER INQUIRY</div>
                    <div style={{ fontSize: '1rem', fontWeight: 700, color: '#93c5fd', cursor: 'pointer', marginTop: 4 }} onClick={() => onSelectCustomer(activeInv.customer_id)}>
                      {activeInv.customer_name} ({activeInv.customer_id}) <ArrowRight size={12} style={{ display: 'inline' }} />
                    </div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                      Risk Level: {activeInv.customer_risk_level}
                    </div>
                  </div>

                  <div style={{ background: 'var(--bg-input)', padding: 14, borderRadius: 'var(--radius-sm)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>PRIMARY FLAGGED TRANSACTION</div>
                    {activeInv.primary_transaction_id ? (
                      <div style={{ fontSize: '1rem', fontWeight: 700, color: '#f87171', cursor: 'pointer', marginTop: 4 }} onClick={() => onSelectTransaction(activeInv.primary_transaction_id)}>
                        {activeInv.primary_transaction_id} <ArrowRight size={12} style={{ display: 'inline' }} />
                      </div>
                    ) : (
                      <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: 4 }}>No primary single transaction specified</div>
                    )}
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: 4 }}>
                      Evidence links: {activeInv.evidence_links || 'TXN-1024, REG-AML-01'}
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: 16 }}>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 4 }}>EXECUTIVE FINDINGS</div>
                  <div style={{ fontSize: '0.88rem', color: '#cbd5e1', background: 'rgba(0,0,0,0.2)', padding: 12, borderRadius: 6, lineHeight: 1.5 }}>
                    {activeInv.findings || 'Evidence gathering underway.'}
                  </div>
                </div>
              </div>

              {/* Notes Log & Audit History */}
              <div className="card">
                <div className="card-title">
                  <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Clock size={18} color="var(--accent-blue)" />
                    Investigation Audit Log
                  </span>
                </div>

                <div style={{ 
                  background: 'var(--bg-input)', 
                  padding: 16, 
                  borderRadius: 'var(--radius-sm)', 
                  fontFamily: 'var(--font-mono)', 
                  fontSize: '0.82rem', 
                  color: '#94a3b8',
                  whiteSpace: 'pre-wrap',
                  maxHeight: 220,
                  overflowY: 'auto',
                  lineHeight: 1.6
                }}>
                  {activeInv.analyst_notes || 'No notes logged yet.'}
                </div>

                {/* Add Note Form */}
                <form onSubmit={handleAddNote} style={{ display: 'flex', gap: 10, marginTop: 14 }}>
                  <input 
                    type="text" 
                    className="input-field" 
                    placeholder="Append new investigation observation or evidence finding..." 
                    value={newNote}
                    onChange={(e) => setNewNote(e.target.value)}
                    style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '10px 14px' }}
                  />
                  <button type="submit" className="btn btn-secondary" disabled={savingNote || !newNote.trim()}>
                    <Send size={14} /> Append
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Formal Compliance Report Modal */}
      {showReportModal && report && (
        <div className="drawer-overlay" onClick={() => setShowReportModal(false)}>
          <div 
            style={{ 
              background: '#0d131f', 
              width: '90%', 
              maxWidth: 900, 
              maxHeight: '90vh', 
              overflowY: 'auto', 
              margin: 'auto', 
              borderRadius: 'var(--radius-lg)', 
              border: '1px solid var(--border-color)',
              padding: 32,
              boxShadow: 'var(--shadow-lg)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <FileText size={22} color="var(--accent-blue)" />
                <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#fff' }}>Official Investigation Summary Report</h2>
              </div>
              <div style={{ display: 'flex', gap: 10 }}>
                <button 
                  className="btn btn-secondary btn-sm"
                  onClick={() => window.print()}
                >
                  <Printer size={14} /> Print / Save as PDF
                </button>
                <button 
                  className="btn btn-secondary btn-sm"
                  onClick={() => setShowReportModal(false)}
                >
                  <X size={16} />
                </button>
              </div>
            </div>

            {/* Printable Report View */}
            <div className="printable-report" id="printable-report">
              <div className="report-header">
                <div>
                  <h1 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }}>
                    FINANCIAL COMPLIANCE & RISK AUDIT REPORT
                  </h1>
                  <div style={{ fontSize: '0.82rem', color: '#475569', marginTop: 4 }}>
                    REPORT ID: <strong>{report.report_id}</strong> • GENERATED: {new Date(report.generated_at).toUTCString()}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.78rem', color: '#64748b', fontWeight: 600 }}>ENTERPRISE COMPLIANCE PLATFORM</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#0f172a' }}>REGULATORY AUDIT DOSSIER</div>
                </div>
              </div>

              {/* Case Meta */}
              <div className="report-section">
                <div className="report-section-title">Case Metadata</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, fontSize: '0.85rem' }}>
                  <div><strong>Case ID:</strong> {report.investigation_id}</div>
                  <div><strong>Case Status:</strong> {report.status}</div>
                  <div><strong>Assigned Officer:</strong> {report.assigned_analyst}</div>
                </div>
              </div>

              {/* Target Customer */}
              <div className="report-section">
                <div className="report-section-title">Customer Risk Dossier</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, fontSize: '0.85rem' }}>
                  <div><strong>Customer Name:</strong> {report.customer.full_name} ({report.customer.customer_id})</div>
                  <div><strong>Risk Rating:</strong> {report.customer.risk_level} ({report.customer.risk_score}/100)</div>
                  <div><strong>Declared Occupation:</strong> {report.customer.occupation}</div>
                  <div><strong>Account Type & KYC:</strong> {report.customer.account_type} / {report.customer.kyc_status}</div>
                  <div><strong>Historical Baseline Average:</strong> ₹{report.customer.baseline_avg_amount?.toLocaleString('en-IN')}</div>
                  <div><strong>Politically Exposed Person (PEP):</strong> {report.customer.is_pep ? 'YES' : 'NO'}</div>
                </div>
              </div>

              {/* Primary Incident */}
              {report.primary_transaction && (
                <div className="report-section">
                  <div className="report-section-title">Primary Incident Flagged</div>
                  <div style={{ background: '#f8fafc', padding: 12, borderRadius: 6, fontSize: '0.85rem', border: '1px solid #e2e8f0' }}>
                    <div><strong>Transaction ID:</strong> {report.primary_transaction.transaction_id}</div>
                    <div><strong>Amount:</strong> ₹{report.primary_transaction.amount?.toLocaleString('en-IN', { minimumFractionDigits: 2 })} {report.primary_transaction.currency}</div>
                    <div><strong>Destination Corridor:</strong> {report.primary_transaction.destination_country} (Risk Score: {report.primary_transaction.risk_score}/100)</div>
                    <div><strong>Reason:</strong> {report.primary_transaction.flagged_reason_summary}</div>
                  </div>
                </div>
              )}

              {/* Triggered Explainable Rules */}
              <div className="report-section">
                <div className="report-section-title">Triggered Regulatory Rules ({report.triggered_rules.length})</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {report.triggered_rules.map((r, i) => (
                    <div key={i} style={{ background: '#f8fafc', padding: 10, borderRadius: 4, borderLeft: '3px solid #ef4444', fontSize: '0.82rem' }}>
                      <div style={{ fontWeight: 700, color: '#0f172a' }}>{r.rule_name} (Rule: {r.rule_id})</div>
                      <div style={{ color: '#475569', marginTop: 2 }}>{r.explanation}</div>
                      {r.regulatory_ref && (
                        <div style={{ color: '#0369a1', fontWeight: 600, marginTop: 4 }}>Citing Regulatory Framework: {r.regulatory_ref}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Regulatory Citations */}
              <div className="report-section">
                <div className="report-section-title">Regulatory Framework Citations (Statutory KB)</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {report.regulatory_citations.map((c, i) => (
                    <div key={i} style={{ border: '1px solid #cbd5e1', padding: 10, borderRadius: 4, fontSize: '0.82rem' }}>
                      <div style={{ fontWeight: 700, color: '#0f172a' }}>{c.doc_id}: {c.title}</div>
                      <div style={{ color: '#64748b', fontSize: '0.75rem' }}>Authority: {c.authority}</div>
                      <div style={{ color: '#334155', marginTop: 4 }}>{c.summary}</div>
                      <div style={{ color: '#b91c1c', marginTop: 4, fontWeight: 600 }}>Action: {c.recommended_compliance_action}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommended Action */}
              <div className="report-section">
                <div className="report-section-title">Final Compliance Recommendation</div>
                <div style={{ background: '#f0fdf4', border: '1px solid #86efac', padding: 14, borderRadius: 6, fontSize: '0.88rem', color: '#166534', fontWeight: 600 }}>
                  {report.compliance_recommendation}
                </div>
              </div>

              {/* Disclaimer */}
              <div style={{ marginTop: 24, paddingTop: 16, borderTop: '1px solid #e2e8f0', fontSize: '0.75rem', color: '#94a3b8', textAlign: 'center' }}>
                {report.disclaimer} • Generated by Risk, Fraud & Regulatory Intelligence Copilot
              </div>
            </div>
          </div>
        </div>
      )}

      {/* New Case Creation Modal */}
      {showNewCaseModal && (
        <div className="drawer-overlay" onClick={() => setShowNewCaseModal(false)}>
          <div 
            style={{ 
              background: 'var(--bg-card)', 
              width: '90%', 
              maxWidth: 550, 
              margin: 'auto', 
              borderRadius: 'var(--radius-lg)', 
              border: '1px solid var(--border-color)',
              padding: 28,
              boxShadow: 'var(--shadow-lg)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff' }}>Create New Compliance Case</h2>
              <button className="btn btn-secondary btn-sm" onClick={() => setShowNewCaseModal(false)}>
                <X size={16} />
              </button>
            </div>

            <form onSubmit={handleCreateCaseSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Case Title</label>
                <input 
                  type="text" 
                  className="input-field" 
                  value={newCaseForm.title}
                  onChange={(e) => setNewCaseForm({...newCaseForm, title: e.target.value})}
                  required
                  style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '8px 12px' }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Customer ID</label>
                  <input 
                    type="text" 
                    className="input-field" 
                    value={newCaseForm.customer_id}
                    onChange={(e) => setNewCaseForm({...newCaseForm, customer_id: e.target.value})}
                    required
                    style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '8px 12px' }}
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Primary Transaction</label>
                  <input 
                    type="text" 
                    className="input-field" 
                    value={newCaseForm.primary_transaction_id}
                    onChange={(e) => setNewCaseForm({...newCaseForm, primary_transaction_id: e.target.value})}
                    placeholder="e.g. TXN-1024"
                    style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '8px 12px' }}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Priority</label>
                  <select 
                    className="select-field" 
                    value={newCaseForm.priority}
                    onChange={(e) => setNewCaseForm({...newCaseForm, priority: e.target.value})}
                    style={{ width: '100%' }}
                  >
                    <option value="Critical">Critical</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>
                </div>

                <div>
                  <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Assigned Officer</label>
                  <input 
                    type="text" 
                    className="input-field" 
                    value={newCaseForm.assigned_analyst}
                    onChange={(e) => setNewCaseForm({...newCaseForm, assigned_analyst: e.target.value})}
                    style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '8px 12px' }}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: 4 }}>Summary / Hypothesis</label>
                <textarea 
                  className="input-field" 
                  rows="3"
                  value={newCaseForm.summary}
                  onChange={(e) => setNewCaseForm({...newCaseForm, summary: e.target.value})}
                  style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '8px 12px' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowNewCaseModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create Case</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
