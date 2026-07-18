"""
Country slug → ISO 4217 currency code, used by country_detail() in
apps/core/views.py to look up that country's currency in the shared rates
table from apps/core/exchange_rate.py and plot it against USD and Toman on
templates/core/country_detail.html.

A few countries share a currency with a neighbor (e.g. Palestine mostly
uses the Israeli Shekel / Jordanian Dinar day-to-day) — where that's the
case the code picked here is the one the rates API actually has data for.
"""

CURRENCY_CODES = {
    'afghanistan': 'AFN',
    'bahrain': 'BHD',
    'bangladesh': 'BDT',
    'bhutan': 'BTN',
    'brunei': 'BND',
    'cambodia': 'KHR',
    'china': 'CNY',
    'india': 'INR',
    'indonesia': 'IDR',
    'iran': 'IRR',
    'japan': 'JPY',
    'jordan': 'JOD',
    'kazakhstan': 'KZT',
    'kuwait': 'KWD',
    'kyrgyzstan': 'KGS',
    'laos': 'LAK',
    'malaysia': 'MYR',
    'mongolia': 'MNT',
    'myanmar': 'MMK',
    'nepal': 'NPR',
    'oman': 'OMR',
    'pakistan': 'PKR',
    'palestine': 'ILS',
    'philippines': 'PHP',
    'qatar': 'QAR',
    'russia': 'RUB',
    'saudi-arabia': 'SAR',
    'singapore': 'SGD',
    'south-korea': 'KRW',
    'sri-lanka': 'LKR',
    'tajikistan': 'TJS',
    'thailand': 'THB',
    'turkey': 'TRY',
    'united-arab-emirates': 'AED',
    'uzbekistan': 'UZS',
    'vietnam': 'VND',
    'armenia': 'AMD',
    'azerbaijan': 'AZN',
    'cyprus': 'EUR',
    'georgia': 'GEL',
    'iraq': 'IQD',
    'israel': 'ILS',
    'lebanon': 'LBP',
    'maldives': 'MVR',
    'north-korea': 'KPW',
    'syria': 'SYP',
    'taiwan': 'TWD',
    'timor-leste': 'USD',
    'turkmenistan': 'TMT',
    'yemen': 'YER',
}
