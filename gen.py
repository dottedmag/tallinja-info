"""
Stuff to gen stuff
"""

import requests
import datetime
import json
import concurrent.futures as cf

ZONES = {
    'ai': 'Airport',
    'ar': 'Armier%20bay',
    'at': 'Attard',
    'bh': 'Bahar%20ic%20Caghaq',
    'bi': 'Bahrija',
    'bl': 'Balzan',
    'bd': 'Bidnija',
    'br': 'Bpirgu',
    'bk': 'Birkirkara',
    'bz': 'Birzebbuga',
    'bt': 'Blata%20L-Bajda',
    'bo': 'Bormla',
    'bu': 'Bugibba',
    'bm': 'Burmarrad',
    'bs': 'Buskett',
    'ci': 'Cirkewwa',
    'di': 'Dingli',
    'dw': 'Dwejra',
    'fg': 'Fgura',
    'gl': 'Floriana',
    'gt': 'Ghajn%20Tuffieha',
    'gg': 'Gharghur',
    'gx': 'Ghaxaq',
    'gn': 'Gnejna',
    'gb': 'Golden%20Bay',
    'gu': 'Gudja',
    'gw': 'Gwardamangia',
    'gz': 'Gzira',
    'hf': 'Hal%20Far',
    'hm': 'Hamrun',
    'ib': 'Ibrag',
    'ik': 'Iklin',
    'im': 'Imtarfa',
    'is': 'Isla',
    'kk': 'Kalkara',
    'kp': 'Kappara',
    'kr': 'Kirkop',
    'li': 'Lija',
    'lu': 'Luqa',
    'ml': 'Madliena',
    'mt': 'Maghtab',
    'mk': 'Manikata',
    'mf': 'Marfa',
    'ma': 'Marsa',
    'mr': 'Marsaskala',
    'mx': 'Marsaxlokk',
    'md': 'Mdina',
    'me': 'Mellieha',
    'mg': 'Mgarr',
    'mo': 'Mosta',
    'mq': 'Mqabba',
    'mh': 'Mriehel',
    'ms': 'Msida',
    'nx': 'Naxxar',
    'pc': 'Paceville',
    'pa': 'Paola',
    'pe': 'Pembroke',
    'pi': 'Pieta',
    'qa': 'Qawra',
    'qo': 'Qormi',
    'qr': 'Qrendi',
    'ra': 'Rabat',
    'sf': 'Safi',
    'sn': 'Salina',
    'sg': 'San%20Giljan',
    'sw': 'San%20Gwann',
    'sp': 'San%20Pawl%20il-Bahar',
    'su': 'Santa%20Lucija',
    'sm': 'Santa%20Marija%20Estate',
    'sv': 'Santa%20Venera',
    'si': 'Siggiewi',
    'sl': 'Sliema',
    'sa': 'St%20Andrews',
    'st': 'Swatar',
    'sq': 'Swieqi',
    'tq': 'Ta%20Qali',
    'tx': 'Ta\'%20Xbiex',
    'tr': 'Tarxien',
    'un': 'University',
    'vl': 'Valletta',
    'wr': 'Wardija',
    'xm': 'Xemxija',
    'xg': 'Xghajra',
    'zb': 'Zabbar',
    'zu': 'Zebbug',
    'zj': 'Zejtun',
    'zr': 'Zurrieq',
}

CAR_TYPES = {
    'std': '1',
    'exec': 'Executive',
    'van': '5',
    'execvan': 'Executive Van',
}

HOUR_TYPES = {
    'day': '12',
    'night': '00'
}

PRICE_URL = \
    "http://g8way2.ecabsonline.com/eCabsRESTService.svc/RetrieveTotalPrice/"

NOW = datetime.datetime.now()

PRICES = {}

def get_price(f, t, c, h):
    print('?', f, t, c, h)
    fz = ZONES[f]
    tz = ZONES[t]
    ct = CAR_TYPES[c]
    ht = HOUR_TYPES[h]
    url = "{0}{1},{2},{3},{4},{5},{6},{7},00".format(
        PRICE_URL, fz, tz, ct,
        NOW.year, NOW.month, NOW.day, ht)
    res = requests.get(url)
    if res.status_code != 200:
        raise res.status_code
    body = res.json()
    result = body.get('RetrieveTotalPriceResult', {})
    if result.get('failed', True):
        raise body
    price = int(result['guid'])
    print(f, t, c, h, '->', price)
    PRICES[(f, t, c, h)] = price

EXEC = cf.ThreadPoolExecutor(max_workers=128)

fs = []

for f in ZONES:
    for t in ZONES:
        for c in CAR_TYPES:
            for h in HOUR_TYPES:
                fs.append(EXEC.submit(get_price, f, t, c, h))

cf.wait(fs)

print(PRICES)
