import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Lock, 
  User, 
  Mail, 
  KeyRound, 
  UserPlus, 
  LogIn, 
  Shield, 
  CheckCircle2, 
  AlertTriangle,
  Building2,
  Fingerprint
} from 'lucide-react';
import { api, setToken, setStoredUser } from '../services/api';
import ThemeToggle from '../components/ThemeToggle';

export default function AuthPage({ onLoginSuccess, theme, toggleTheme }) {
  // 'signin' or 'signup'
  const [authMode, setAuthMode] = useState('signin');

  // Sign In states
  const [loginIdentifier, setLoginIdentifier] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  // Sign Up states
  const [regFullName, setRegFullName] = useState('');
  const [regUsername, setRegUsername] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regRole, setRegRole] = useState('user');

  // Status & error states
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const switchMode = (mode) => {
    setAuthMode(mode);
    setErrorMsg('');
    setSuccessMsg('');
  };

  const handleLoginSubmit = async (e) => {
    if (e) e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const payload = {
        username_or_email: loginIdentifier.trim(),
        password: loginPassword
      };

      const res = await api.login(payload);
      if (res && res.access_token) {
        setToken(res.access_token);
        setStoredUser(res.user);
        setSuccessMsg(`Access Granted! Welcome ${res.user.full_name || res.user.username} (${res.user.role.toUpperCase()})`);
        setTimeout(() => {
          onLoginSuccess(res.user, res.access_token);
        }, 300);
      }
    } catch (err) {
      setErrorMsg(err.message || 'Login failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    if (e) e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const payload = {
        full_name: regFullName.trim(),
        username: regUsername.trim(),
        email: regEmail.trim(),
        password: regPassword,
        role: regRole
      };

      const res = await api.register(payload);
      if (res && res.access_token) {
        setToken(res.access_token);
        setStoredUser(res.user);
        setSuccessMsg(`Account created successfully! Logged in as ${res.user.full_name || res.user.username}`);
        setTimeout(() => {
          onLoginSuccess(res.user, res.access_token);
        }, 400);
      }
    } catch (err) {
      setErrorMsg(err.message || 'Registration failed. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      {/* Floating Theme Switch in top-right corner */}
      <div className="theme-toggle-floating">
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
      </div>

      <div className="auth-card">
        {/* Header Branding */}
        <div className="auth-header">
          <img 
            src={theme === 'light' ? '/assets/astra-logo-light.png' : '/assets/astra-logo-dark.png'} 
            alt="Astra AI Logo" 
            className="auth-header-logo" 
          />
          <h1 className="auth-app-title">Astra AI</h1>
        </div>

        {/* Auth Mode Tabs: Sign In / Sign Up */}
        <div className="auth-tabs">
          <button 
            type="button"
            className={`auth-tab-btn ${authMode === 'signin' ? 'active user-tab' : ''}`}
            onClick={() => switchMode('signin')}
          >
            <LogIn size={16} />
            <span>Sign In</span>
          </button>
          
          <button 
            type="button"
            className={`auth-tab-btn ${authMode === 'signup' ? 'active register-tab' : ''}`}
            onClick={() => switchMode('signup')}
          >
            <UserPlus size={16} />
            <span>Sign Up</span>
          </button>
        </div>

        {/* Status Alerts */}
        {errorMsg && (
          <div className="auth-alert error">
            <AlertTriangle size={18} />
            <span>{errorMsg}</span>
          </div>
        )}

        {successMsg && (
          <div className="auth-alert success">
            <CheckCircle2 size={18} />
            <span>{successMsg}</span>
          </div>
        )}

        {/* SIGN IN FORM (Both User & Admin) */}
        {authMode === 'signin' && (
          <form onSubmit={handleLoginSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="login-username">
                <User size={14} /> Username or Email Address
              </label>
              <input 
                id="login-username"
                type="text" 
                className="auth-input"
                placeholder="Enter username or email"
                value={loginIdentifier}
                onChange={(e) => setLoginIdentifier(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="login-password">
                <Lock size={14} /> Password
              </label>
              <input 
                id="login-password"
                type="password" 
                className="auth-input"
                placeholder="••••••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
              />
            </div>

            <button 
              type="submit" 
              className="auth-submit-btn user-theme"
              disabled={loading}
            >
              {loading ? (
                <span className="btn-spinner">Authenticating...</span>
              ) : (
                <>
                  <LogIn size={16} />
                  <span>Sign In</span>
                </>
              )}
            </button>
          </form>
        )}

        {/* SIGN UP / REGISTRATION FORM */}
        {authMode === 'signup' && (
          <form onSubmit={handleRegisterSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="reg-fullname">
                <Building2 size={14} /> Full Name
              </label>
              <input 
                id="reg-fullname"
                type="text" 
                className="auth-input"
                placeholder="e.g. Rachel Zane"
                value={regFullName}
                onChange={(e) => setRegFullName(e.target.value)}
                required
              />
            </div>

            <div className="form-row-2">
              <div className="form-group">
                <label htmlFor="reg-username">
                  <User size={14} /> Username
                </label>
                <input 
                  id="reg-username"
                  type="text" 
                  className="auth-input"
                  placeholder="rachel_z"
                  value={regUsername}
                  onChange={(e) => setRegUsername(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="reg-email">
                  <Mail size={14} /> Business Email
                </label>
                <input 
                  id="reg-email"
                  type="email" 
                  className="auth-input"
                  placeholder="rachel@financial.corp"
                  value={regEmail}
                  onChange={(e) => setRegEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-row-2">
              <div className="form-group">
                <label htmlFor="reg-password">
                  <KeyRound size={14} /> Password (min 6 chars)
                </label>
                <input 
                  id="reg-password"
                  type="password" 
                  className="auth-input"
                  placeholder="••••••••••••"
                  value={regPassword}
                  onChange={(e) => setRegPassword(e.target.value)}
                  required
                  minLength={6}
                />
              </div>

              <div className="form-group">
                <label htmlFor="reg-role">
                  <Shield size={14} /> Account Role
                </label>
                <select 
                  id="reg-role"
                  className="auth-input auth-select"
                  value={regRole}
                  onChange={(e) => setRegRole(e.target.value)}
                >
                  <option value="user">User (Standard Access)</option>
                  <option value="admin">Administrator (Admin Access)</option>
                </select>
              </div>
            </div>

            <button 
              type="submit" 
              className="auth-submit-btn register-theme"
              disabled={loading}
            >
              {loading ? (
                <span className="btn-spinner">Registering account...</span>
              ) : (
                <>
                  <UserPlus size={16} />
                  <span>Create Account & Sign In</span>
                </>
              )}
            </button>
          </form>
        )}

        {/* Security Badges */}
        <div className="auth-footer">
          <div className="security-badges">
            <span className="sec-chip"><ShieldCheck size={12} /> PBKDF2 Password Hashing</span>
            <span className="sec-chip"><Lock size={12} /> HMAC-SHA256 Bearer Token</span>
            <span className="sec-chip"><Fingerprint size={12} /> Zero Unauthorized Access</span>
          </div>
        </div>
      </div>
    </div>
  );
}
