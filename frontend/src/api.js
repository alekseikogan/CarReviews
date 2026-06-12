const API_URL = import.meta.env.VITE_API_URL || '/api';

async function fetchApi(endpoint, params = {}) {
  const url = new URL(`${API_URL}${endpoint}`, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      url.searchParams.set(key, value);
    }
  });

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function getCars({ page = 1, mark, body, search } = {}) {
  return fetchApi('/cars/', { page, mark, body, search });
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
