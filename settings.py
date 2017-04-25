import os

## Price

# The minimum rent you want to pay per month.
MIN_PRICE = {'roo': 1200, 'apa': 2000}

# The maximum rent you want to pay per month.
MAX_PRICE = {'roo': 2500, 'apa': 5200}


## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'sfbay'

# What Craigslist subdirectories to search on. For instance,
# https://sfbay.craigslist.org/eby/ is the East Bay,
# and https://sfbay.craigslist.org/sfc/ is San Francisco. You only need the
# last three letters of the URLs.
AREAS = ['sfc']

# A list of neighborhoods and coordinates that you want to look for
# apartments in.  Any listing that has coordinates attached will be checked
# to see which area it is in.  If there's a match, it will be annotated with
# the area name.  If no match, the neighborhood field, which is a string,
# will be checked to see if it matches anything in NEIGHBORHOODS.
BOXES = {
    # 'adams_point': [
    #     [37.80789, -122.25000],
    #     [37.81589, -122.26081],
    # ],
    # 'piedmont': [
    #     [37.82240, -122.24768],
    #     [37.83237, -122.25386],
    # ],
    # 'rockridge': [
    #     [37.83826, -122.24073],
    #     [37.84680, -122.25944],
    # ],
    # 'berkeley': [
    #     [37.86226, -122.25043],
    #     [37.86781, -122.26502],
    # ],
    # 'north_berkeley': [
    #     [37.86425, -122.26330],
    #     [37.87655, -122.28974],
    # ],
    'pac_heights': [
        [37.79124, -122.42381],
        [37.79850, -122.44784],
    ],
    'lower_pac_heights': [
        [37.78554, -122.42878],
        [37.78873, -122.44544],
    ],
    'haight': [
        [37.77059, -122.42688],
        [37.77086, -122.45401],
    ],
    'sunset': [
        [37.75451, -122.46422],
        [37.76258, -122.50825],
    ],
    # 'richmond': [
    #     [37.77188, -122.47263],
    #     [37.78029, -122.51005],
    # ],
    # 'presidio': [
    #     [37.77805, -122.43959],
    #     [37.78829, -122.47151],
    # ]
}

# A list of neighborhood names to look for in the Craigslist neighborhood
# name field. If a listing doesn't fall into one of the boxes you defined,
# it will be checked to see if the neighborhood name it was listed under
# matches one of these.  This is less accurate than the boxes, because it
# relies on the owner to set the right neighborhood, but it also catches
# listings that don't have coordinates (many listings are missing this info).
NEIGHBORHOODS = [
    'alamo square / nopa',
    'castro / upper market',
    'cole valley / ashbury hts',
    'downtown / civic / van ness',
    'financial district',
    'haight ashbury',
    'hayes valley',
    # 'inner richmond',
    # 'inner sunset / UCSF',
    'lower haight',
    # 'lower nob hill',
    'lower pac hts',
    'marina / cow hollow',
    'mission district',
    'nob hill',
    'noe valley',
    'north beach / telegraph hill',
    'pacific heights',
    'potrero hill',
    'russian hill',
    'SOMA / south beach',
    'USF / panhandle',
]


## Transit preferences

# The farthest you want to live from a transit stop.
MAX_TRANSIT_DIST = 1.5  # miles
MAX_SHUTTLE_DIST = 0.75  # miles
MAX_SHUTTLE_WALK_TIME = 15.0  # minutes


# Transit stations you want to check against.  Every coordinate here will be
# checked against each listing, and the closest station name will be added to
# the result and posted into Slack.

BART_STATIONS = {
    '12th St. Oakland City Center': (37.803664, -122.271604),
    '16th St. Mission': (37.765062, -122.419694),
    '19th St. Oakland': (37.80787, -122.269029),
    '24th St. Mission': (37.752254, -122.418466),
    'Ashby': (37.853024, -122.26978),
    'Balboa Park': (37.72198087, -122.4474142),
    'Bay Fair': (37.697185, -122.126871),
    'Castro Valley': (37.690754, -122.075567),
    'Civic Center/UN Plaza': (37.779528, -122.413756),
    'Coliseum': (37.754006, -122.197273),
    'Colma': (37.684638, -122.466233),
    'Concord': (37.973737, -122.029095),
    'Daly City': (37.70612055, -122.4690807),
    'Downtown Berkeley': (37.869867, -122.268045),
    'Dublin/Pleasanton': (37.701695, -121.900367),
    'El Cerrito del Norte': (37.925655, -122.317269),
    'El Cerrito Plaza': (37.9030588, -122.2992715),
    'Embarcadero': (37.792976, -122.396742),
    'Fremont': (37.557355, -121.9764),
    'Fruitvale': (37.774963, -122.224274),
    'Glen Park': (37.732921, -122.434092),
    'Hayward': (37.670399, -122.087967),
    'Lafayette': (37.893394, -122.123801),
    'Lake Merritt': (37.797484, -122.265609),
    'MacArthur': (37.828415, -122.267227),
    'Millbrae': (37.599787, -122.38666),
    'Montgomery St.': (37.789256, -122.401407),
    'North Berkeley': (37.87404, -122.283451),
    'North Concord/Martinez': (38.003275, -122.024597),
    "Oakland Int'l Airport": (37.71297174, -122.21244024),
    'Orinda': (37.87836087, -122.1837911),
    'Pittsburg/Bay Point': (38.018914, -121.945154),
    'Pleasant Hill/Contra Costa Centre': (37.928403, -122.056013),
    'Powell St.': (37.784991, -122.406857),
    'Richmond': (37.936887, -122.353165),
    'Rockridge': (37.844601, -122.251793),
    'San Bruno': (37.637753, -122.416038),
    "San Francisco Int'l Airport": (37.616035, -122.392612),
    'San Leandro': (37.72261921, -122.1613112),
    'South Hayward': (37.63479954, -122.0575506),
    'South San Francisco': (37.664174, -122.444116),
    'Union City': (37.591208, -122.017867),
    'Walnut Creek': (37.905628, -122.067423),
    'West Dublin/Pleasanton': (37.699759, -121.928099),
    'West Oakland': (37.80467476, -122.2945822),
    'Warm Springs/South Fremont': (37.502583, -121.93642),
}

SHUTTLE_STOPS = None  # load from private.py


## Search type preferences

# The Craigslist section underneath housing that you want to search in. For
# instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets. You only need the
# last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = ['roo', 'apa']

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 20 * 60  # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = {'roo': '#rooms', 'apa': '#apartments'}

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', '')

# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

