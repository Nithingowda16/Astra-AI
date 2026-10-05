import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { 
  BotMessageSquare, 
  Send, 
  Sparkles, 
  ShieldAlert, 
  BookOpen, 
  ArrowRight, 
  ExternalLink,
  CheckCircle,
  HelpCircle,
  User,
  AlertTriangle
} from 'lucide-react';

export default function Copilot({ 
  initialQuery = '', 
  onSelectTransaction, 
  onSelectCustomer, 
  onOpenRegulatoryRule 
}) {
  const [messages, setMessages] = useState([
    {
      sender: 'copilot',
      text: "Hello! I am your **Risk, Fraud & Regulatory Intelligence Copilot**. I analyze transaction patterns, customer baseline deviations, and cite the Regulatory Knowledge Base. What would you like to investigate?",
      data: null
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const samplePrompts = [
    "Why was transaction TXN-1024 flagged?",
    "Why is customer CUST-1008 considered high risk?",
    "Show me high-risk transactions above ₹5 lakh.",
    "Show suspicious transactions involving high-risk countries.",
    "Show the regulatory evidence supporting this finding.",
    "Generate an investigation summary for customer CUST-1008."
  ];

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const text = (queryText || input).trim();
    if (!text) return;

    const userMsg = { sender: 'user', text, data: null };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.queryCopilot(text);
      const copilotMsg = {
        sender: 'copilot',
        text: response.answer,
        data: response
      };
      setMessages(prev => [...prev, copilotMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          sender: 'copilot',
          text: `Error communicating with Copilot reasoning engine: ${err.message}`,
          data: null
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="copilot-page">
      <div className="page-header">
        <div>
          <h1 className="page-title" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <Sparkles size={24} color="#38bdf8" />
            Astra AI Copilot
          </h1>
          <p className="page-subtitle">
            Explainable conversational intelligence grounded in transaction graphs and the Regulatory Knowledge Base
          </p>
        </div>
      </div>

      <div className="copilot-container">
        {/* Left Sidebar: Quick Prompts & Context Guide */}
        <div className="copilot-sidebar">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            <HelpCircle size={16} color="var(--accent-blue)" />
            <span>Recommended Queries</span>
          </div>

          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Select any standard inquiry to run the full audit & explanation pipeline:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {samplePrompts.map((prompt, idx) => (
              <button
                key={idx}
                className="prompt-pill"
                onClick={() => handleSend(prompt)}
                disabled={loading}
              >
                {prompt}
              </button>
            ))}
          </div>

          <div style={{ marginTop: 'auto', paddingTop: 16, borderTop: '1px solid var(--border-color)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <strong style={{ color: 'var(--accent-cyan)' }}>Grounded Reasoning:</strong> Responses dynamically correlate database transactions, baseline averages, and Regulatory Knowledge Base clauses without hallucinating.
          </div>
        </div>

        {/* Right Area: Interactive Chat Stream */}
        <div className="copilot-chat-area">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`message-bubble ${msg.sender === 'user' ? 'message-user' : 'message-copilot'}`}
              >
                {/* Header tag */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, fontSize: '0.75rem', opacity: 0.8 }}>
                  {msg.sender === 'user' ? (
                    <>
                      <User size={12} />
                      <strong>Compliance Officer</strong>
                    </>
                  ) : (
                    <>
                      <BotMessageSquare size={12} color="#38bdf8" />
                      <strong>Investigation Copilot</strong>
                    </>
                  )}
                </div>

                {/* Render Answer */}
                <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.55 }}>
                  {msg.text}
                </div>

                {/* Structured Evidence & Action Cards (Copilot message) */}
                {msg.data && msg.data.data_found && (
                  <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {/* Entity Badges */}
                    {msg.data.entities && msg.data.entities.length > 0 && (
                      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>Identified Records:</span>
                        {msg.data.entities.map((ent, i) => (
                          <span
                            key={i}
                            className="status-badge"
                            style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#93c5fd', cursor: 'pointer', border: '1px solid rgba(59, 130, 246, 0.4)' }}
                            onClick={() => {
                              if (ent.type === 'transaction') onSelectTransaction(ent.id);
                              if (ent.type === 'customer') onSelectCustomer(ent.id);
                              if (ent.type === 'rule') onOpenRegulatoryRule(ent.id);
                            }}
                          >
                            {ent.label} <ExternalLink size={10} style={{ marginLeft: 4 }} />
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Supporting Regulatory Evidence Boxes */}
                    {msg.data.supporting_evidence && msg.data.supporting_evidence.length > 0 && (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700, textTransform: 'uppercase' }}>
                          Supporting Regulatory Evidence (Knowledge Base)
                        </div>
                        {msg.data.supporting_evidence.map((ev, i) => (
                          <div key={i} className="evidence-box">
                            <div className="evidence-title">
                              <BookOpen size={14} />
                              <span>{ev.title}</span>
                              {ev.doc_id && (
                                <span 
                                  style={{ marginLeft: 'auto', cursor: 'pointer', textDecoration: 'underline', fontSize: '0.75rem' }}
                                  onClick={() => onOpenRegulatoryRule(ev.doc_id)}
                                >
                                  Open Clause
                                </span>
                              )}
                            </div>
                            <div className="evidence-excerpt">"{ev.excerpt}"</div>
                            {ev.authority && (
                              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4 }}>
                                Authority: {ev.authority}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Suggested Next Actions */}
                    {msg.data.suggested_actions && msg.data.suggested_actions.length > 0 && (
                      <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: 12, borderRadius: 6, border: '1px solid var(--border-color)' }}>
                        <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#facc15', textTransform: 'uppercase', marginBottom: 6 }}>
                          Recommended Compliance Actions
                        </div>
                        <ul style={{ paddingLeft: 18, fontSize: '0.82rem', color: '#cbd5e1' }}>
                          {msg.data.suggested_actions.map((act, i) => (
                            <li key={i} style={{ marginBottom: 4 }}>{act}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message-bubble message-copilot" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <Sparkles size={16} className="animate-spin" color="#38bdf8" />
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Correlating transactions, baseline deviation, and regulatory evidence...
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input Bar */}
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            style={{ 
              padding: '16px 20px', 
              borderTop: '1px solid var(--border-color)', 
              display: 'flex', 
              gap: 12,
              background: 'var(--bg-secondary)'
            }}
          >
            <input 
              type="text" 
              className="input-field" 
              placeholder="Ask Copilot (e.g. 'Why was transaction TXN-1024 flagged?')..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
              style={{ background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', padding: '10px 14px' }}
            />
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading || !input.trim()}
            >
              <Send size={16} /> Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
