from furl import furl
from requests import get
from time import time

APIKEYFILE = 'darksky.key'


def get_api_key():
    with open(APIKEYFILE) as f:
        l = f.readline()
        return l.strip()


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
    # url.args.add('exclude', 'currently,flags,hourly')
    return url.tostr()


def main():
    key = get_api_key()
    lat = 39.559319
    long = -105.099653
    unix_time = int(time())

    url = build_api_url(key=key, lat=lat, long=long)  # , time=unix_time)
    req = get(url)
    resp = req.json()

    print resp


if __name__ == "__main__":
    main()
