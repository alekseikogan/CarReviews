const FALLBACK_PHOTOS = [
  '1542362563207-aeb566b25d3f',
  '1503376780353-7f669ff66a09',
  '1552519507-da3b142c6e3d',
  '1494976388534-d1058498ceb2',
  '1580273916550-4061e76ee7ed',
  '1618843479313-40f8afb5110d',
  '1502877338535-766e1452684a',
  '1617531653524-bd46e24dcc71',
];

export function fallbackPhoto(seed = 0) {
  const idx = Math.abs(Number(seed) || 0) % FALLBACK_PHOTOS.length;
  return `https://images.unsplash.com/photo-${FALLBACK_PHOTOS[idx]}?w=800&h=500&fit=crop&auto=format&q=85`;
}
