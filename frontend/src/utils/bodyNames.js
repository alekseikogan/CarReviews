export const bodyNamesEn = {
  sedan: 'Sedan',
  hatchback: 'Hatchback',
  suv: 'SUV',
  crossover: 'Crossover',
  coupe: 'Coupe',
  cabrio: 'Convertible',
  wagon: 'Wagon',
  minivan: 'Minivan',
  liftback: 'Liftback',
  pickup: 'Pickup',
};

export function getBodyName(body, lang) {
  if (!body) return '';
  if (lang === 'en') {
    return bodyNamesEn[body.slug] || body.name;
  }
  return body.name;
}
