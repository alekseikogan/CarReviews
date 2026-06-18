const PLACEHOLDER_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450">
  <rect fill="#e8eaed" width="800" height="450"/>
  <g fill="none" stroke="#9aa0a6" stroke-width="4">
    <rect x="220" y="150" width="360" height="150" rx="12"/>
    <circle cx="290" cy="300" r="28"/>
    <circle cx="510" cy="300" r="28"/>
  </g>
</svg>`;

export const carPlaceholder = `data:image/svg+xml,${encodeURIComponent(PLACEHOLDER_SVG)}`;

export function fallbackPhoto() {
  return carPlaceholder;
}

export function tileFallbackPhoto() {
  return carPlaceholder;
}
