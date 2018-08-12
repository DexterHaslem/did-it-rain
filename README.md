## did it rain

This is a simple script to see how much it rained in the the past few days if you are too lazy to 
go put a cup outside or something.

## setup

runs on Python 2.7+. Install python deps with
> pip install -r requirements.txt

 Get a darksky API key for free [here](https://darksky.net/dev/register) and place the key in a file called `darksky.key`

## Running
```commandline
$ python main.py --lat 39.601 --long -105.092 --days 5
in the last 5 days, there was 0.02 total mm/h, (0.0 inch/h) of rain for location (39.601:-105.092)
$
```

- `lat`: latitude of location to pull weather for
- `long`: longitude of location to pull weather for
- `days`: number of days back to sum rainfall for