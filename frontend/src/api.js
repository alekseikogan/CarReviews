const API_URL = import.meta.env.VITE_API_URL || '/api';

function getAccessToken() {
  return localStorage.getItem('access_token');
}

async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh_token');
  if (!refresh) return null;
  const response = await fetch(`${API_URL}/auth/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });
  if (!response.ok) return null;
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  return data.access;
}

async function fetchApi(endpoint, { method = 'GET', body, auth = false, retry = true } = {}) {
  const url = new URL(`${API_URL}${endpoint}`, window.location.origin);
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const token = getAccessToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url.toString(), {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (response.status === 401 && auth && retry) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      return fetchApi(endpoint, { method, body, auth, retry: false });
    }
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data.detail || Object.values(data).flat().join(' ') || `API error: ${response.status}`;
    throw new Error(message);
  }
  return data;
}

export function getCars({ page = 1, mark, body, search } = {}) {
  const params = new URLSearchParams();
  params.set('page', page);
  if (mark) params.set('mark', mark);
  if (body) params.set('body', body);
  if (search) params.set('search', search);
  return fetchApi(`/cars/?${params.toString()}`);
}

export function getBodies() {
  return fetchApi('/bodies/');
}

export function getCar(slug) {
  return fetchApi(`/cars/${slug}/`);
}

export function getMarks() {
  return fetchApi('/marks/');
}

export function getStats() {
  return fetchApi('/cars/stats/');
}

export function login(credentials) {
  return fetchApi('/auth/login/', { method: 'POST', body: credentials });
}

export function register(payload) {
  return fetchApi('/auth/register/', { method: 'POST', body: payload });
}

export function getMe() {
  return fetchApi('/auth/me/', { auth: true });
}

export function updateMe(payload) {
  return fetchApi('/auth/me/', { method: 'PATCH', body: payload, auth: true });
}

export function requestPasswordReset(email) {
  return fetchApi('/auth/password-reset/', { method: 'POST', body: { email } });
}

export function confirmPasswordReset(payload) {
  return fetchApi('/auth/password-reset/confirm/', { method: 'POST', body: payload });
}

export function getCarComments(slug) {
  return fetchApi(`/cars/${slug}/comments/`);
}

export function postCarComment(slug, text) {
  return fetchApi(`/cars/${slug}/comments/`, { method: 'POST', body: { text }, auth: true });
}

export function deleteComment(id) {
  return fetchApi(`/comments/${id}/`, { method: 'DELETE', auth: true });
}
