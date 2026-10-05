import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Users, 
  ShieldAlert, 
  Activity, 
  UserCheck, 
  UserX, 
  Key, 
  RefreshCw, 
  Lock, 
  Clock, 
  Terminal,
  Shield,
  AlertCircle
} from 'lucide-react';
import { api } from '../services/api';

export default function AdminConsole({ currentUser }) {
  const [users, setUsers] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [bannerMsg, setBannerMsg] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const [usersData, auditData] = await Promise.all([
        api.getAdminUsers(),
        api.getAdminAuditLogs(30)
      ]);
      setUsers(usersData || []);
      setAuditLogs(auditData || []);
    } catch (err) {
      setBannerMsg({ type: 'error', text: err.message || 'Failed to load administrative data.' });
    } finally {
      setLoading(false);
    }
  };

  const handleRoleToggle = async (user) => {
    const newRole = user.role === 'admin' ? 'user' : 'admin';
    const confirmText = `Are you sure you want to change '${user.username}' from ${user.role.toUpperCase()} to ${newRole.toUpperCase()}?`;
    if (!window.confirm(confirmText)) return;

    setActionLoading(user.id);
    try {
      const updated = await api.updateUserRole(user.id, newRole);
      setUsers(users.map(u => u.id === user.id ? updated : u));
      setBannerMsg({ type: 'success', text: `Updated role of '${user.username}' to ${newRole.toUpperCase()}` });
      // Refresh audit logs
      const auditData = await api.getAdminAuditLogs(30);
      setAuditLogs(auditData || []);
    } catch (err) {
      setBannerMsg({ type: 'error', text: err.message || 'Failed to update user role.' });
    } finally {
      setActionLoading(null);
    }
  };

  const handleStatusToggle = async (user) => {
    const newStatus = !user.is_active;
    const actionName = newStatus ? 'activate' : 'deactivate';
    if (!window.confirm(`Are you sure you want to ${actionName} user '${user.username}'?`)) return;

    setActionLoading(user.id);
    try {
      const updated = await api.updateUserStatus(user.id, newStatus);
      setUsers(users.map(u => u.id === user.id ? updated : u));
      setBannerMsg({ type: 'success', text: `Successfully ${actionName}d user '${user.username}'.` });
      // Refresh audit logs
      const auditData = await api.getAdminAuditLogs(30);
      setAuditLogs(auditData || []);
    } catch (err) {
      setBannerMsg({ type: 'error', text: err.message || `Failed to ${actionName} user.` });
    } finally {
      setActionLoading(null);
    }
  };

  const adminCount = users.filter(u => u.role === 'admin' && u.is_active).length;
  const userCount = users.filter(u => u.role === 'user' && u.is_active).length;

  return (
    <div className="admin-console-page">
      {/* Top Banner */}
      <div className="admin-header-banner">
        <div className="admin-header-left">
          <div className="admin-shield-icon">
            <Shield size={28} />
          </div>
          <div>
            <h1 className="page-title">Compliance Security & Administrator Console</h1>
            <p className="page-subtitle">
              Role-Based Access Control (RBAC), Identity Governance & Security Audit Trail
            </p>
          </div>
        </div>

        <button 
          className="refresh-btn"
          onClick={fetchAdminData}
          disabled={loading}
          title="Refresh Administrator Data"
        >
          <RefreshCw size={15} className={loading ? 'spin' : ''} />
          <span>Sync Security Logs</span>
        </button>
      </div>

      {bannerMsg.text && (
        <div className={`auth-alert ${bannerMsg.type === 'error' ? 'error' : 'success'}`} style={{ marginBottom: '1.5rem' }}>
          {bannerMsg.type === 'error' ? <AlertCircle size={18} /> : <ShieldCheck size={18} />}
          <span>{bannerMsg.text}</span>
        </div>
      )}

      {/* Security Metrics Overview */}
      <div className="admin-stats-grid">
        <div className="stat-card">
          <div className="stat-icon-wrapper purple">
            <Shield size={22} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Security Role</span>
            <span className="stat-value">{currentUser?.role?.toUpperCase() || 'ADMIN'}</span>
            <span className="stat-sub">Authenticated as {currentUser?.username}</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon-wrapper indigo">
            <Users size={22} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Total Accounts</span>
            <span className="stat-value">{users.length}</span>
            <span className="stat-sub">{adminCount} Admins &bull; {userCount} Users</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon-wrapper emerald">
            <ShieldCheck size={22} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Authentication Mode</span>
            <span className="stat-value">PBKDF2 + JWT</span>
            <span className="stat-sub">Strict RBAC & Dual Portals</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon-wrapper blue">
            <Activity size={22} />
          </div>
          <div className="stat-content">
            <span className="stat-label">Security Audit Logs</span>
            <span className="stat-value">{auditLogs.length}</span>
            <span className="stat-sub">Live monitoring active</span>
          </div>
        </div>
      </div>

      {/* Platform Users Directory */}
      <div className="admin-section-card">
        <div className="section-card-header">
          <div className="section-card-title">
            <Users size={18} />
            <span>Authorized System Users ({users.length})</span>
          </div>
          <span className="section-badge">Live RBAC Enforcement</span>
        </div>

        <div className="table-responsive">
          <table className="admin-table">
            <thead>
              <tr>
                <th>User / Name</th>
                <th>Email Address</th>
                <th>Role</th>
                <th>Account Status</th>
                <th>Created</th>
                <th>Last Login</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const isSelf = u.id === currentUser?.id;
                const isAdmin = u.role === 'admin';
                return (
                  <tr key={u.id} className={!u.is_active ? 'row-deactivated' : ''}>
                    <td>
                      <div className="user-cell">
                        <div className={`user-avatar ${isAdmin ? 'admin-avatar' : 'user-avatar'}`}>
                          {u.full_name ? u.full_name.charAt(0).toUpperCase() : u.username.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <div className="user-cell-name">
                            {u.full_name} {isSelf && <span className="self-tag">(You)</span>}
                          </div>
                          <div className="user-cell-username">@{u.username}</div>
                        </div>
                      </div>
                    </td>
                    <td className="mono-cell">{u.email}</td>
                    <td>
                      <span className={`role-badge ${isAdmin ? 'role-admin' : 'role-user'}`}>
                        {isAdmin ? <Shield size={12} /> : <UserCheck size={12} />}
                        <span>{isAdmin ? 'ADMIN' : 'USER'}</span>
                      </span>
                    </td>
                    <td>
                      <span className={`status-pill ${u.is_active ? 'status-active' : 'status-disabled'}`}>
                        {u.is_active ? 'Active' : 'Deactivated'}
                      </span>
                    </td>
                    <td className="date-cell">
                      {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="date-cell">
                      {u.last_login ? new Date(u.last_login).toLocaleString() : 'Never'}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <div className="action-buttons-group">
                        <button
                          type="button"
                          className={`action-btn-sm ${isAdmin ? 'btn-demote' : 'btn-promote'}`}
                          onClick={() => handleRoleToggle(u)}
                          disabled={actionLoading === u.id || (isSelf && isAdmin && adminCount <= 1)}
                          title={isAdmin ? 'Demote to User' : 'Promote to Admin'}
                        >
                          <Key size={13} />
                          <span>{isAdmin ? 'Demote' : 'Make Admin'}</span>
                        </button>

                        <button
                          type="button"
                          className={`action-btn-sm ${u.is_active ? 'btn-deactivate' : 'btn-activate'}`}
                          onClick={() => handleStatusToggle(u)}
                          disabled={actionLoading === u.id || isSelf}
                          title={u.is_active ? 'Deactivate Account' : 'Activate Account'}
                        >
                          {u.is_active ? <UserX size={13} /> : <UserCheck size={13} />}
                          <span>{u.is_active ? 'Deactivate' : 'Activate'}</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Security Audit Trail */}
      <div className="admin-section-card" style={{ marginTop: '2rem' }}>
        <div className="section-card-header">
          <div className="section-card-title">
            <Terminal size={18} />
            <span>Security & Authentication Audit Trail (Chronological)</span>
          </div>
          <span className="section-badge audit-badge">Tamper-Evident Logs</span>
        </div>

        <div className="table-responsive">
          <table className="admin-table audit-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Actor / User</th>
                <th>Action</th>
                <th>Role</th>
                <th>Status</th>
                <th>Details</th>
                <th>IP Address</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
                    No audit records registered yet.
                  </td>
                </tr>
              ) : (
                auditLogs.map((log) => {
                  const isSuccess = log.status === 'SUCCESS';
                  const isBlocked = log.status === 'BLOCKED' || log.status === 'FAILED';
                  return (
                    <tr key={log.id}>
                      <td className="date-cell mono-cell">
                        <Clock size={12} style={{ display: 'inline', marginRight: '4px' }} />
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td className="mono-cell font-bold">{log.username}</td>
                      <td>
                        <span className="action-tag">{log.action}</span>
                      </td>
                      <td>
                        <span className={`role-badge-sm ${log.role === 'admin' ? 'role-admin' : 'role-user'}`}>
                          {log.role.toUpperCase()}
                        </span>
                      </td>
                      <td>
                        <span className={`status-pill ${isSuccess ? 'status-active' : 'status-blocked'}`}>
                          {log.status}
                        </span>
                      </td>
                      <td className="log-details-cell">{log.details || '—'}</td>
                      <td className="mono-cell">{log.ip_address || '127.0.0.1'}</td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
