import React from 'react';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  ArrowLeftRight, 
  Users, 
  Bell, 
  FileSearch, 
  BookOpen, 
  BotMessageSquare, 
  Shield, 
  LogOut,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';

export default function Navbar({ 
  activeTab, 
  setActiveTab, 
  alertCount = 0, 
  openCaseCount = 0,
  currentUser,
  onLogout,
  theme,
  toggleTheme,
  sidebarCollapsed = false,
  setSidebarCollapsed
}) {
  const isAdmin = currentUser?.role === 'admin';

  const navSections = [
    {
      title: 'OPERATIONS',
      items: [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { id: 'transactions', label: 'Transactions', icon: ArrowLeftRight },
        { id: 'customers', label: 'Customers', icon: Users },
        { id: 'alerts', label: 'Alerts', icon: Bell, badge: alertCount },
        { id: 'investigations', label: 'Investigations', icon: FileSearch, badge: openCaseCount },
      ]
    },
    {
      title: 'AI & INTELLIGENCE',
      items: [
        { id: 'regulatory', label: 'Regulatory Rules', icon: BookOpen },
        { id: 'copilot', label: 'Copilot Assistant', icon: BotMessageSquare, isSpecial: true },
      ]
    }
  ];

  if (isAdmin) {
    navSections.push({
      title: 'GOVERNANCE',
      items: [
        { id: 'admin', label: 'Admin Console', icon: Shield, isAdminTab: true }
      ]
    });
  }

  return (
    <aside className={`sidebar-nav ${sidebarCollapsed ? 'collapsed' : ''}`}>
      {/* Sidebar Header / Brand with Smooth Collapse Toggle */}
      <div className="sidebar-header">
        <div className="sidebar-header-main" onClick={() => setActiveTab('dashboard')} title="Astra AI Dashboard">
          <div className="sidebar-brand-icon">
            <img 
              src={theme === 'light' ? '/assets/astra-logo-light.png' : '/assets/astra-logo-dark.png'} 
              alt="Astra AI" 
              className="sidebar-brand-logo-img" 
            />
          </div>
          {!sidebarCollapsed && (
            <div className="sidebar-brand-text">
              <div className="sidebar-brand-title">Astra AI</div>
              <div className="sidebar-brand-subtitle">Risk & Regulatory Intelligence</div>
            </div>
          )}
        </div>
        
        {setSidebarCollapsed && (
          <button 
            type="button" 
            className="sidebar-collapse-btn" 
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title={sidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
            aria-label={sidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {sidebarCollapsed ? <PanelLeftOpen size={16} /> : <PanelLeftClose size={16} />}
          </button>
        )}
      </div>

      {/* Navigation Sections */}
      <div className="sidebar-menu-scroll">
        {navSections.map((section) => (
          <div key={section.title} className="sidebar-section">
            {!sidebarCollapsed && (
              <div className="sidebar-section-title">{section.title}</div>
            )}
            <nav className="sidebar-links">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    className={`sidebar-nav-btn ${isActive ? 'active' : ''} ${item.isAdminTab ? 'is-admin-btn' : ''} ${sidebarCollapsed ? 'btn-collapsed' : ''}`}
                    onClick={() => setActiveTab(item.id)}
                    title={item.label}
                    aria-label={item.label}
                  >
                    <Icon size={18} className="sidebar-item-icon" />
                    {!sidebarCollapsed && (
                      <span className="sidebar-item-label">{item.label}</span>
                    )}
                    {item.badge > 0 && (
                      <span className={`sidebar-badge ${sidebarCollapsed ? 'badge-collapsed' : ''}`}>
                        {item.badge}
                      </span>
                    )}
                    {!sidebarCollapsed && item.isSpecial && (
                      <span className="sidebar-special-tag">AI</span>
                    )}
                    {!sidebarCollapsed && item.isAdminTab && (
                      <span className="sidebar-badge admin-badge-tag">ADMIN</span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* Sidebar Footer: Theme Toggle & User Identity */}
      <div className="sidebar-footer">
        <div className={`sidebar-theme-row ${sidebarCollapsed ? 'theme-collapsed' : ''}`}>
          {!sidebarCollapsed && <span className="sidebar-theme-label">Appearance</span>}
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        </div>

        {currentUser && (
          <div className={`sidebar-user-card ${sidebarCollapsed ? 'user-card-collapsed' : ''}`}>
            <div className={`user-avatar-sm ${isAdmin ? 'admin-avatar' : 'user-avatar'}`} title={currentUser.full_name || currentUser.username}>
              {currentUser.full_name ? currentUser.full_name.charAt(0).toUpperCase() : currentUser.username.charAt(0).toUpperCase()}
            </div>
            {!sidebarCollapsed && (
              <div className="sidebar-user-info">
                <span className="sidebar-user-name" title={currentUser.full_name || currentUser.username}>
                  {currentUser.full_name || currentUser.username}
                </span>
                <span className={`sidebar-role-badge ${isAdmin ? 'role-admin' : 'role-user'}`}>
                  {isAdmin ? 'ADMIN' : 'USER'}
                </span>
              </div>
            )}
            <button 
              type="button" 
              className="sidebar-logout-btn" 
              onClick={onLogout}
              title="Sign Out"
              aria-label="Sign Out"
            >
              <LogOut size={16} />
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}
