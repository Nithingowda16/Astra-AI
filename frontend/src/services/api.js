/**
 * Centralized API client for Risk, Fraud & Regulatory Intelligence Copilot
 */

const BASE_URL = import.meta.env.VITE_API_URL || '';

export const getToken = () => localStorage.getItem('compliance_auth_token');
export const setToken = (token) => localStorage.setItem('compliance_auth_token', token);
export const removeToken = () => localStorage.removeItem('compliance_auth_token');

export const getStoredUser = () => {
  try {
    const raw = localStorage.getItem('compliance_auth_user');
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
};
export const setStoredUser = (user) => localStorage.setItem('compliance_auth_user', JSON.stringify(user));
export const removeStoredUser = () => localStorage.removeItem('compliance_auth_user');

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}/api${endpoint}`;
  const token = getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      if (res.status === 401 && !url.includes('/auth/login') && !url.includes('/auth/register')) {
        // Clear invalid token on session expiry
        removeToken();
        removeStoredUser();
        window.dispatchEvent(new CustomEvent('auth:expired'));
      }
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Request failed with status ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`API Error on ${url}:`, err);
    throw err;
  }
}

export const api = {
  // Authentication & RBAC
  login: (credentials) => request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials)
  }),
  register: (userData) => request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  }),
  getMe: () => request('/auth/me'),
  getAdminUsers: () => request('/auth/admin/users'),
  updateUserRole: (userId, role) => request(`/auth/admin/users/${userId}/role`, {
    method: 'PATCH',
    body: JSON.stringify({ role })
  }),
  updateUserStatus: (userId, isActive) => request(`/auth/admin/users/${userId}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ is_active: isActive })
  }),
  getAdminAuditLogs: (limit = 50) => request(`/auth/admin/audit?limit=${limit}`),

  // Dashboard
  getDashboardStats: () => request('/dashboard/stats'),


  // Transactions
  getTransactions: (params = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        searchParams.append(k, v);
      }
    });
    const qs = searchParams.toString();
    return request(`/transactions${qs ? `?${qs}` : ''}`);
  },
  getTransactionDetail: (id) => request(`/transactions/${id}`),
  evaluateTransaction: (txnData) => request('/transactions/evaluate', {
    method: 'POST',
    body: JSON.stringify(txnData)
  }),

  // Customers
  getCustomers: (params = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        searchParams.append(k, v);
      }
    });
    const qs = searchParams.toString();
    return request(`/customers${qs ? `?${qs}` : ''}`);
  },
  getCustomerDetail: (id) => request(`/customers/${id}`),

  // Alerts
  getAlerts: (params = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        searchParams.append(k, v);
      }
    });
    const qs = searchParams.toString();
    return request(`/alerts${qs ? `?${qs}` : ''}`);
  },
  updateAlertStatus: (id, status) => request(`/alerts/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status })
  }),

  // Investigations
  getInvestigations: (params = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        searchParams.append(k, v);
      }
    });
    const qs = searchParams.toString();
    return request(`/investigations${qs ? `?${qs}` : ''}`);
  },
  getInvestigationDetail: (id) => request(`/investigations/${id}`),
  createInvestigation: (data) => request('/investigations', {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateInvestigation: (id, data) => request(`/investigations/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data)
  }),
  getInvestigationReport: (id) => request(`/investigations/${id}/report`),

  // Regulatory Knowledge Base
  getRegulatoryRules: (params = {}) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        searchParams.append(k, v);
      }
    });
    const qs = searchParams.toString();
    return request(`/regulatory/rules${qs ? `?${qs}` : ''}`);
  },
  getRegulatoryRuleDetail: (id) => request(`/regulatory/rules/${id}`),

  // Copilot
  queryCopilot: (query, context = {}) => request('/copilot/query', {
    method: 'POST',
    body: JSON.stringify({
      query,
      context_customer_id: context.customerId || null,
      context_transaction_id: context.transactionId || null
    })
  })
};
