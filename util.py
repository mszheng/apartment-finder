import settings
import math


def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Distance in miles.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    km = 2 * 6367 * math.asin(math.sqrt(a))
    mi = 0.621371 * km
    return mi


def in_box(coords, box):
    """
    Find if a coordinate tuple is inside a bounding box.
    :param coords: Tuple containing latitude and longitude.
    :param box: Two tuples, where first is the bottom left, and the second is 
    the top right of the box.
    :return: Boolean indicating if the coordinates are in the box.
    """
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False


def post_listing_to_slack(sc, channel, listing):
    """
    Posts the listing to slack.
    :param sc: A slack client.
    :param channel: Channel to post to.
    :param listing: A record of the listing.
    """
    desc1 = '{0} | {1} | {2}\n'.format(listing['neighborhood'],
                                       listing['price'],
                                       listing['name'])
    desc2 = '{0:2.2f} mi to {1} | {2:2.2f} mi to {3} shuttle\n'
    desc2 = desc2.format(listing['transit_dist'],
                         listing['transit_stop'],
                         listing['shuttle_dist'],
                         listing['shuttle_stop'])

    desc3 = '<{0}>'.format(listing['url'])

    sc.api_call(
        'chat.postMessage', channel=channel, text=desc1 + desc2 + desc3,
        username='cl_rooms', icon_emoji=':house:'
    )


def closest_stop(geotag, stops):
    """
    Find closest stop to a location.
    :param geotag: 
    :param stops: 
    :return: 
    """
    stop_name = ''
    closest_dist = float('inf')
    for stop, coords in stops.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
        if dist < closest_dist:
            stop_name = stop
            closest_dist = dist

    return stop_name, closest_dist


def find_points_of_interest(geotag, location):
    """
    Find points of interest, like transit, near a result.
    :param geotag: The geotag field of a Craigslist result.
    :param location: The where field of a Craigslist result.  Is a string 
    containing a description of where
    the listing was posted.
    :return: A dictionary containing annotations.
    """

    fields = ['neighborhood', 'transit_stop', 'transit_dist', 'shuttle_stop',
              'shuttle_dist']

    if geotag is not None:
        neighborhood = ''

        # Check to see if the string description of the neighborhood matches
        # anything in our list of neighborhoods.
        for hood in settings.NEIGHBORHOODS:
            if hood.lower() in location.lower():
                neighborhood = location

        # If neighborhood not labled, look to see if the listing is in any of
        # the manual neighborhood boxes we defined.
        if len(neighborhood) == 0:
            for hood, box_coords in settings.BOXES.items():
                if in_box(geotag, box_coords):
                    neighborhood = hood

        # Find the closest transit stations.
        transit_stop, transit_dist = closest_stop(geotag,
                                                  settings.BART_STATIONS)

        # Find the closest shuttle stop.
        shuttle_stop, shuttle_dist = closest_stop(geotag,
                                                  settings.SHUTTLE_STOPS)

        values = [neighborhood, transit_stop, transit_dist, shuttle_stop,
                  shuttle_dist]

    else:
        values = ['', '', float('inf'), '', float('inf')]

    return dict(zip(fields, values))
