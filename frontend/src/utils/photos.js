export function buildCarPhotoUrl(mark, model, year, complect = '') {
  const makeMap = {
    Mercedes: 'mercedes-benz',
    'Land Rover': 'land-rover',
    Gelly: 'geely',
    Infinity: 'infiniti',
    Лада: 'lada',
    ВАЗ: 'lada',
    Москвич: 'moskvich',
    УАЗ: 'uaz',
    Jetta: 'volkswagen',
    Sollers: 'ford',
  };

  const make = makeMap[mark] || mark.toLowerCase().replace(/\s+/g, '-');
  let family = model.toLowerCase().split(/[\s-]/)[0];

  if (mark === 'Audi') {
    const t = model.toLowerCase().split(' ')[0];
    family = ['a3', 'a4', 'a6', 'q3', 'tt'].includes(t) ? t : t;
  } else if (mark === 'BMW') {
    const ml = model.toLowerCase();
    if (ml.startsWith('x')) {
      family = `x${ml.replace(/\D/g, '') || '5'}`;
    } else if (/^\d/.test(ml)) {
      family = `${ml[0]}-series`;
    }
  } else if (mark === 'Mercedes') {
    const ml = model.toLowerCase();
    if (ml.startsWith('glc')) family = 'glc';
    else if (ml.startsWith('c')) family = 'c-class';
    else if (ml.startsWith('e')) family = 'e-class';
    else if (ml.startsWith('s')) family = 's-class';
    else if (ml.startsWith('cls')) family = 'cls-class';
  } else if (mark === 'Toyota' && model.toLowerCase().includes('camry')) {
    family = 'camry';
  } else if (mark === 'Chevrolet' && model.toLowerCase().includes('camaro')) {
    family = 'camaro';
  }

  const y = Math.max(1990, Math.min(Number(year) || 2020, 2025));
  const params = new URLSearchParams({
    customer: 'img',
    make,
    modelFamily: family,
    modelYear: String(y),
    width: '800',
    angle: '23',
    zoomType: 'fullscreen',
  });
  return `https://cdn.imagin.studio/getimage?${params.toString()}`;
}

export function fallbackPhoto(car) {
  if (car?.mark?.name && car?.model) {
    return buildCarPhotoUrl(
      car.mark.name,
      car.model,
      car.year,
      car.complect,
    );
  }
  return buildCarPhotoUrl('Audi', 'A4', 2018);
}

export function tileFallbackPhoto(seed = 0) {
  return buildCarPhotoUrl('Audi', 'A4', 2014 + (Number(seed) % 5));
}
