from craigslist import CraigslistHousing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import post_listing_to_slack, find_points_of_interest, desirable
from slackclient import SlackClient
import time
import settings


Base = declarative_base()


class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    neighborhood = Column(String)
    transit_stop = Column(String)
    shuttle_stop = Column(String)

engine = create_engine('sqlite:///listings.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def scrape(site, area, category, min_price, max_price):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest 
    listings.
    :param site:
    :param area:
    :param category:
    :param min_price:
    :param max_price:
    :return: A list of results.
    """

    results = []

    cl_h = CraigslistHousing(
        site=site,
        area=area,
        category=category,
        filters={'min_price': min_price, 'max_price': max_price}
    )

    gen = cl_h.get_results(
        sort_by='newest',
        geotagged=True,
        limit=20
    )

    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue

        listing = session.query(Listing).filter_by(cl_id=result['id']).first()

        # Don't store the listing if it already exists.
        if listing is None:
            if result['where'] is None:
                # If there is no string identifying which neighborhood the
                # result is from, skip it.
                continue

            # Annotate the result with information about the area it's in and
            # points of interest near it.
            result.update(
                find_points_of_interest(result['geotag'], result['where'])
            )

            lat = 0
            lon = 0
            if result['geotag'] is not None:
                # Assign the coordinates.
                lat = result['geotag'][0]
                lon = result['geotag'][1]

            # Try parsing the price.
            price = 0
            try:
                price = float(result['price'].replace('$', ''))
            except (TypeError, ValueError):
                pass

            # Create the listing object.
            listing = Listing(
                link=result['url'],
                created=parse(result['datetime']),
                geotag=str(result['geotag']),
                lat=lat,
                lon=lon,
                name=result['name'],
                price=price,
                location=result['where'],
                cl_id=result['id'],
                neighborhood=result['neighborhood'],
                transit_stop=result['transit_stop'],
                shuttle_stop=result['shuttle_stop']
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the result if it's near a shuttle stop and in a
            # desired neighborhood. Adjust requirements to your liking.
            if (result['shuttle_walk_time'] < settings.MAX_SHUTTLE_WALK_TIME
                    and len(result['neighborhood']) > 0
                    and result['has_image']
                    and desirable(result['url'])):
                results.append(result)

    return results


def scrape_and_post():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    for section in settings.CRAIGSLIST_HOUSING_SECTION:

        all_results = []

        for area in settings.AREAS:
            results = scrape(
                settings.CRAIGSLIST_SITE,
                area,
                section,
                settings.MIN_PRICE[section],
                settings.MAX_PRICE[section],
            )

            all_results += results

        print('{}: Got {} results for {}'.format(time.ctime(),
                                                 len(all_results),
                                                 section))

        # Post each result to slack.
        channel = settings.SLACK_CHANNEL[section]

        for result in all_results:
            post_listing_to_slack(sc, channel, result)
