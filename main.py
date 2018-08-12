from __future__ import print_function
from datetime import datetime, timedelta
from time import mktime

import click
from furl import furl
from requests import get

APIKEYFILE = 'darksky.key'

MM_TO_INCH = 0.0393701


def get_api_key():
    with open(APIKEYFILE) as f:
        line = f.readline()
        return line.strip()


def build_api_url(**kwargs):
    url = furl('https://api.darksky.net')
    url.path.add('forecast')
    url.path.add(kwargs.get('key'))

    lat = str(kwargs.get('lat'))
    long = str(kwargs.get('long'))

    # [lat,long,time]
    try_time = kwargs.get('time')
    args = [lat, long]
    if try_time:
        unix_time = str(try_time)
        args.append(unix_time)

    darksky_args = ','.join(args)
    url.path.add(darksky_args)

    try_excludes = kwargs.get('excludes')
    if try_excludes:
        url.args.add('exclude', ','.join(try_excludes))

    return url.tostr()


@click.command()
@click.option('--lat', default=0, help='latitude of weather location', type=click.FLOAT)
@click.option('--long', default=0, help='longitude of weather location', type=click.FLOAT)
@click.option('--days', default=3, help='days back to total rainfall for', type=click.INT)
def main(lat, long, days):
    key = get_api_key()

    total_precip_mmh = 0

    # If a date is not given, its a forecast. if date given, its historical,
    # Request last couple days. reason we do a few days, is the API cuts off at midnight utc for a 'day' -
    # not request time.
    for day_back in range(days, 0, -1):
        d = datetime.today() - timedelta(days=day_back)
        unix_time = int(mktime(d.timetuple()))

        # we only care about daily
        url = build_api_url(key=key, lat=lat, long=long, time=unix_time, excludes=['currently', 'flags', 'hourly'])
        req = get(url)
        resp = req.json()

        data = resp['daily']['data']

        for day in data:
            # precipIntensity is unconditional on daily. see if we got any for the day
            precipIntensity = day.get('precipIntensity')
            if precipIntensity:
                precipType = day.get('precipType')
                # ensure it was rain and not snow or sleet
                if precipType == 'rain':
                    total_precip_mmh += day.get('precipIntensityMax')

    total_precip_mmh = round(total_precip_mmh, 2)
    precip_inches = round(total_precip_mmh * MM_TO_INCH, 2)
    print('In the last {} days, there was {} total mm/h, ({} inch/h) of rain for location ({}:{})'
          .format(days, total_precip_mmh, precip_inches, lat, long))


if __name__ == "__main__":
    main()
