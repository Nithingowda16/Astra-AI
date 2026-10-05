import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Customers from './pages/Customers';
import Alerts from './pages/Alerts';
import Investigations from './pages/Investigations';
import Regulatory from './pages/Regulatory';
import Copilot from './pages/Copilot';
import AdminConsole from './pages/AdminConsole';
import AuthPage from './pages/AuthPage';
import { api, getToken, getStoredUser, removeToken, removeStoredUser } from './services/api';
import { ShieldAlert, LogIn, PanelLeft } from 'lucide-react';

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => getStoredUser());
  const [token, setAuthToken] = useState(() => getToken());
  const isAuthenticated = Boolean(token && currentUser);

  // Sidebar Collapsible State
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Visual Theme: 'dark' | 'light'
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('compliance_theme') || 'dark';
  });

  const toggleTheme = () => {
    setTheme(prev => {
      const nextTheme = prev === 'dark' ? 'light' : 'dark';
      localStorage.setItem('compliance_theme', nextTheme);
      return nextTheme;
    });
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedTxnId, setSelectedTxnId] = useState(null);
  const [selectedCustomerId, setSelectedCustomerId] = useState(null);
  const [copilotInitialQuery, setCopilotInitialQuery] = useState('');
  const [incomingCaseData, setIncomingCaseData] = useState(null);

  // Badge counts
  const [alertCount, setAlertCount] = useState(0);
  const [openCaseCount, setOpenCaseCount] = useState(0);

  useEffect(() => {
    const handleAuthExpired = () => {
      setCurrentUser(null);
      setAuthToken(null);
    };

    window.addEventListener('auth:expired', handleAuthExpired);
    return () => window.removeEventListener('auth:expired', handleAuthExpired);
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      loadBadgeCounts();
    }
  }, [activeTab, isAuthenticated]);


  const loadBadgeCounts = async () => {
    try {
      const stats = await api.getDashboardStats();
      if (stats) {
        setAlertCount(stats.recent_alerts?.length || 0);
        setOpenCaseCount(stats.open_investigations || 0);
      }
    } catch (err) {
      // quiet fail on badge counter
    }
  };

  const handleLoginSuccess = (user, tokenStr) => {
    setCurrentUser(user);
    setAuthToken(tokenStr);
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    removeToken();
    removeStoredUser();
    setCurrentUser(null);
    setAuthToken(null);
    setActiveTab('dashboard');
  };

  const handleSelectTransaction = (txnId) => {
    setSelectedTxnId(txnId);
    setActiveTab('transactions');
  };

  const handleSelectCustomer = (custId) => {
    setSelectedCustomerId(custId);
    setActiveTab('customers');
  };

  const handleOpenCopilot = (query = '') => {
    setCopilotInitialQuery(query);
    setActiveTab('copilot');
  };

  const handleCreateInvestigation = (caseData) => {
    setIncomingCaseData(caseData);
    setActiveTab('investigations');
  };

  const handleOpenRegulatoryRule = (docId) => {
    setActiveTab('regulatory');
  };

  // If not authenticated, enforce the Security Authentication Gatekeeper
  if (!isAuthenticated) {
    return (
      <AuthPage 
        onLoginSuccess={handleLoginSuccess} 
        theme={theme}
        toggleTheme={toggleTheme}
      />
    );
  }

  const isAdmin = currentUser?.role === 'admin';

  return (
    <div className="app-layout">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        alertCount={alertCount}
        openCaseCount={openCaseCount}
        currentUser={currentUser}
        onLogout={handleLogout}
        theme={theme}
        toggleTheme={toggleTheme}
        sidebarCollapsed={sidebarCollapsed}
        setSidebarCollapsed={setSidebarCollapsed}
      />

      <div className="app-main-viewport">
        <header className="topbar">
          <div className="topbar-left">
            <button 
              type="button" 
              className="topbar-sidebar-toggle"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              title={sidebarCollapsed ? "Expand Navigation Sidebar" : "Collapse Navigation Sidebar"}
              aria-label="Toggle Sidebar Navigation"
            >
              <PanelLeft size={18} />
            </button>
            <span className="topbar-crumb-prefix">Astra AI</span>
            <span className="topbar-divider">/</span>
            <span className="topbar-crumb-active">
              {activeTab === 'dashboard' && 'Operational Dashboard'}
              {activeTab === 'transactions' && 'Transaction Auditing & Monitoring'}
              {activeTab === 'customers' && 'Customer Risk Profiles'}
              {activeTab === 'alerts' && 'Critical Anomaly & Risk Alerts'}
              {activeTab === 'investigations' && 'SAR & Regulatory Case Dossiers'}
              {activeTab === 'regulatory' && 'Regulatory Knowledge Base'}
              {activeTab === 'copilot' && 'AI Compliance Copilot Desk'}
              {activeTab === 'admin' && 'RBAC & Identity Governance'}
            </span>
          </div>
          <div className="topbar-right">
            <div className="topbar-live-chip">
              <span className="live-pulse-dot"></span>
              <span>Live Engine Connected</span>
            </div>
          </div>
        </header>

        <main className="main-content">
          {activeTab === 'dashboard' && (
            <Dashboard 
              onSelectTransaction={handleSelectTransaction}
              onSelectCustomer={handleSelectCustomer}
              onOpenCopilot={handleOpenCopilot}
            />
          )}

          {activeTab === 'transactions' && (
            <Transactions 
              selectedTxnId={selectedTxnId}
              onSelectCustomer={handleSelectCustomer}
              onOpenCopilot={handleOpenCopilot}
              onOpenRegulatoryRule={handleOpenRegulatoryRule}
            />
          )}

          {activeTab === 'customers' && (
            <Customers 
              selectedCustomerId={selectedCustomerId}
              onSelectCustomer={handleSelectCustomer}
              onSelectTransaction={handleSelectTransaction}
              onOpenCopilot={handleOpenCopilot}
              onCreateInvestigation={handleCreateInvestigation}
            />
          )}

          {activeTab === 'alerts' && (
            <Alerts 
              onSelectTransaction={handleSelectTransaction}
              onSelectCustomer={handleSelectCustomer}
              onCreateInvestigation={handleCreateInvestigation}
            />
          )}

          {activeTab === 'investigations' && (
            <Investigations 
              onSelectCustomer={handleSelectCustomer}
              onSelectTransaction={handleSelectTransaction}
              incomingCaseData={incomingCaseData}
            />
          )}

          {activeTab === 'regulatory' && (
            <Regulatory 
              onOpenCopilot={handleOpenCopilot}
            />
          )}

          {activeTab === 'copilot' && (
            <Copilot 
              initialQuery={copilotInitialQuery}
              onSelectTransaction={handleSelectTransaction}
              onSelectCustomer={handleSelectCustomer}
              onOpenRegulatoryRule={handleOpenRegulatoryRule}
            />
          )}

          {activeTab === 'admin' && (
            isAdmin ? (
              <AdminConsole currentUser={currentUser} />
            ) : (
              <div className="unauthorized-card">
                <ShieldAlert size={48} className="unauthorized-icon" />
                <h2>Administrative Access Required</h2>
                <p>Your current session is authenticated as <strong>User ({currentUser?.username})</strong>. Administrative and governance controls require elevated credentials.</p>
                <button className="auth-submit-btn user-theme" onClick={() => setActiveTab('dashboard')} style={{ maxWidth: '250px', margin: '1rem auto 0' }}>
                  Return to Operational Dashboard
                </button>
              </div>
            )
          )}
        </main>
      </div>
    </div>
  );
}

