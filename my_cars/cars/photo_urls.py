"""Генерация URL фото автомобиля по марке, модели и году."""

import re
from urllib.parse import quote

IMAGIN_MAKE = {
    'Audi': 'audi',
    'BAIC': 'baic',
    'BMW': 'bmw',
    'Changan': 'changan',
    'Cadillac': 'cadillac',
    'Citroen': 'citroen',
    'Chery': 'chery',
    'Chevrolet': 'chevrolet',
    'Dodge': 'dodge',
    'Exeed': 'exeed',
    'Fiat': 'fiat',
    'Ford': 'ford',
    'GAC': 'gac',
    'Gelly': 'geely',
    'Haval': 'haval',
    'Honda': 'honda',
    'Hyundai': 'hyundai',
    'Infinity': 'infiniti',
    'Jac': 'jac',
    'Jaecoo': 'jaecoo',
    'Jaguar': 'jaguar',
    'Jetta': 'volkswagen',
    'KIA': 'kia',
    'Lexus': 'lexus',
    'Lifan': 'lifan',
    'Land Rover': 'land-rover',
    'Mercedes': 'mercedes-benz',
    'Mini': 'mini',
    'Mazda': 'mazda',
    'Mitsubishi': 'mitsubishi',
    'Nissan': 'nissan',
    'Omoda': 'omoda',
    'Opel': 'opel',
    'Peugeot': 'peugeot',
    'Ravon': 'ravon',
    'Renault': 'renault',
    'Smart': 'smart',
    'Skoda': 'skoda',
    'Suzuki': 'suzuki',
    'Tesla': 'tesla',
    'Toyota': 'toyota',
    'Volkswagen': 'volkswagen',
    'Volvo': 'volvo',
    'Лада': 'lada',
    'ВАЗ': 'lada',
    'Москвич': 'moskvich',
    'УАЗ': 'uaz',
    'Sollers': 'ford',
}


def _bmw_family(model: str) -> str:
    ml = model.lower().replace('-', '')
    if ml.startswith('x'):
        digits = ''.join(c for c in ml if c.isdigit())
        return f'x{digits}' if digits else 'x5'
    if ml and ml[0].isdigit():
        return f'{ml[0]}-series'
    return model.lower()


def _mercedes_family(model: str) -> str:
    ml = model.lower().replace(' ', '')
    if ml.startswith('glc'):
        return 'glc'
    if ml.startswith('gle'):
        return 'gle'
    if ml.startswith('gla'):
        return 'gla'
    if ml.startswith('gl') and not ml.startswith('glc'):
        return 'gl-class'
    if ml.startswith('slk') or ml.startswith('slc'):
        return 'slk-class'
    if ml.startswith('cls'):
        return 'cls-class'
    if re.match(r'^c\d', ml):
        return 'c-class'
    if re.match(r'^e\d', ml):
        return 'e-class'
    if re.match(r'^s\d', ml):
        return 's-class'
    return ml


def _audi_family(model: str) -> str:
    token = model.lower().split()[0]
    if token in {'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'q3', 'q5', 'q7', 'q8', 'tt'}:
        return token
    if token.startswith('a') or token.startswith('q'):
        return token[:2]
    return token


def _toyota_family(model: str) -> str:
    ml = model.lower()
    if 'camry' in ml:
        return 'camry'
    if 'corolla' in ml or 'fielder' in ml:
        return 'corolla'
    if 'rav' in ml:
        return 'rav4'
    if 'land cruiser' in ml:
        return 'land-cruiser'
    if 'gt86' in ml or 'gr86' in ml:
        return 'gr86'
    if 'harrier' in ml:
        return 'harrier'
    if 'town ace' in ml:
        return 'hiace'
    if 'spacio' in ml:
        return 'spacio'
    return ml.split()[0]


def _lexus_family(model: str) -> str:
    ml = model.lower().replace(' ', '')
    if ml.startswith('es'):
        return 'es'
    if ml.startswith('ls'):
        return 'ls'
    if ml.startswith('lx'):
        return 'lx'
    if ml.startswith('nx'):
        return 'nx'
    if ml.startswith('rx'):
        return 'rx'
    return ml


def _vw_family(model: str) -> str:
    ml = model.lower()
    if 'id.4' in ml or 'id4' in ml:
        return 'id4'
    if 'polo' in ml:
        return 'polo'
    if 'tiguan' in ml:
        return 'tiguan'
    if 'touareg' in ml:
        return 'touareg'
    if 'touran' in ml:
        return 'touran'
    if 'vs5' in ml:
        return 'tiguan'
    return ml.split()[0]


def _land_rover_family(model: str) -> str:
    ml = model.lower()
    if 'range rover sport' in ml:
        return 'range-rover-sport'
    if 'discovery' in ml:
        return 'discovery-sport'
    if 'evoque' in ml:
        return 'range-rover-evoque'
    return ml.replace(' ', '-')


def _lada_family(model: str) -> str:
    ml = model.lower()
    if 'granta' in ml:
        return 'granta'
    if '110' in ml or '2110' in ml:
        return 'vesta'
    if '2105' in ml or '2106' in ml or '2107' in ml:
        return 'vesta'
    return ml.split()[0]


def model_family(mark: str, model: str, complect: str = '') -> str:
    ml = model.lower().strip()
    comp = complect.lower()

    if mark == 'Audi':
        return _audi_family(model)
    if mark == 'BMW':
        return _bmw_family(model)
    if mark == 'Mercedes':
        return _mercedes_family(model)
    if mark == 'Toyota':
        return _toyota_family(model)
    if mark == 'Lexus':
        return _lexus_family(model)
    if mark in ('Volkswagen', 'Jetta'):
        return _vw_family(model)
    if mark == 'Land Rover':
        return _land_rover_family(model)
    if mark in ('Лада', 'ВАЗ'):
        return _lada_family(model)

    known = {
        'kia': {
            'rio': 'rio', 'seltos': 'seltos', 'soul': 'soul',
            'stinger': 'stinger', 'sportage': 'sportage',
        },
        'hyundai': {
            'solaris': 'accent', 'creta': 'creta', 'grand starex': 'staria',
        },
        'nissan': {
            'juke': 'juke', 'qashqai': 'qashqai', 'almera': 'almera',
            'patrol': 'patrol', 'pressage': 'presage',
        },
        'haval': {
            'dargo': 'h6', 'jolion': 'jolion', 'h3': 'h6', 'fx7': 'f7',
        },
        'chery': {
            'arizo 8': 'arrizo-8', 'tiggo 4 pro max': 'tiggo-4',
            'tiggo 7 pro max': 'tiggo-7',
        },
        'renault': {
            'arkana': 'arkana', 'kaptur': 'captur', 'logan': 'logan',
            'megane': 'megane', 'stepway': 'sandero',
        },
        'skoda': {
            'octavia': 'octavia', 'rapid': 'rapid', 'karoq': 'karoq', 'kodiaq': 'kodiaq',
        },
        'mazda': {'3': '3', 'mx-5': 'mx-5'},
        'ford': {'mustang': 'mustang'},
        'chevrolet': {'camaro': 'camaro'},
        'dodge': {'challenger': 'challenger'},
        'honda': {'accord': 'accord'},
        'mitsubishi': {'pajero': 'pajero'},
        'suzuki': {'swift': 'swift'},
        'tesla': {'model 3': 'model-3'},
        'volvo': {'xc60': 'xc60'},
        'jaguar': {'f-pace': 'f-pace', 'xf': 'xf'},
        'cadillac': {'ats': 'ats', 'escalade': 'escalade', 'srx': 'xt5'},
        'mini': {'cooper': 'cooper'},
        'fiat': {'500': '500', 'egea': 'tipo', 'spider 124': '124-spider'},
        'peugeot': {'5008': '5008'},
        'opel': {'insignia': 'insignia', 'grandland': 'grandland'},
        'citroen': {'c4': 'c4'},
        'smart': {'fortwo': 'fortwo', 'forfour': 'forfour'},
        'geely': {
            'atlas pro': 'atlas', 'coolray': 'coolray', 'emgrand': 'emgrand',
        },
        'exeed': {'lx': 'lx', 'rx': 'rx', 'txl': 'txl'},
        'omoda': {'c5': 'c5', 's5': 's5'},
        'gac': {'gs3': 'gs3'},
        'baic': {'x55': 'x55'},
        'jac': {'js4': 'js4', 'js6': 'js6'},
        'jaecoo': {'j7': 'j7'},
        'changan': {'uni-v': 'uni-v'},
        'ravon': {'r2': 'r2'},
        'moskvich': {'3': '3'},
        'uaz': {'3151': 'patriot'},
        'infiniti': {'qx70': 'qx70'},
        'lifan': {'x50': 'x50'},
    }

    make_key = IMAGIN_MAKE.get(mark, mark.lower())
    brand_map = known.get(make_key, {})
    full = f'{ml} {comp}'.strip()
    for key, family in sorted(brand_map.items(), key=lambda x: -len(x[0])):
        if key in full:
            return family

    token = re.sub(r'[^a-z0-9]', '', ml.split()[0])
    return token or 'sedan'


def photo_url(car_id, mark, model, year=2020, complect=''):
    make = IMAGIN_MAKE.get(mark)
    if not make:
        make = mark.lower().replace(' ', '-')

    family = model_family(mark, model, complect)
    year_clamped = max(1990, min(int(year), 2025))

    params = (
        f'customer=img&make={quote(make)}'
        f'&modelFamily={quote(family)}'
        f'&modelYear={year_clamped}'
        f'&width=800&angle=23&zoomType=fullscreen'
    )
    return f'https://cdn.imagin.studio/getimage?{params}'
