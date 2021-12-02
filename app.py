import datetime
from calendar import monthrange
from datetime import datetime, timedelta, timezone
from pprint import pprint

import matplotlib.pyplot as plt
import psycopg2
import requests
from psycopg2.extras import execute_values
from shapely.geometry import shape

API_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
start_year = 2017
start_month = 1

end_year = 2018
end_month = 8

host="db"
db_name = "earthquake_db"
user = "saeed"
password = "123"
table_name = "earthquakes"

connection = psycopg2.connect(f"host={host} dbname={db_name} user={user} password={password}")
cursor = connection.cursor()


def last_day_of_month(year: int, month: int) -> int:
    return monthrange(year, month)[1]


def get_datetime(ts, tz=None):
    tz = timezone(timedelta(minutes=tz)) if tz else timezone.utc
    return datetime.fromtimestamp(ts / 1000, tz=tz).astimezone(timezone.utc)


def get_data(record):
    if record["properties"]["type"] != "earthquake":
        return
    return {
        "mag": record["properties"]["mag"],
        "mag_type": record["properties"]["magType"],
        "place": record["properties"]["place"],
        "time": get_datetime(
            record["properties"]["time"], tz=record["properties"]["tz"] or None
        ),
        "title": record["properties"]["title"],
        "geom": shape(record["geometry"]).wkt,
    }


def prepare_to_insert(records):
    return [
        (
            record["mag"],
            record["mag_type"],
            record["place"],
            record["time"],
            record["title"],
            record["geom"],
        )
        for record in records
    ]


for current_year in range(start_year, end_year + 1):
    _start_month = start_month if current_year == start_year else 1
    for current_month in range(_start_month, 12 + 1):
        if (current_year == end_year) and (current_month > end_month):
            break
        try:
            result = requests.get(
                API_ENDPOINT.format(
                    start_date=f"{current_year}-{current_month}-01",
                    end_date=f"{current_year}-{current_month}-{last_day_of_month(current_year, current_month)}",
                )
            ).json()["features"]
        except Exception:
            # TODO: handle network/memory/... exceptions here
            pass
        finally:
            earthquake_set = filter(
                bool, [get_data(earthquake) for earthquake in result]
            )
            records = prepare_to_insert(earthquake_set)
            execute_values(
                cursor,
                "INSERT INTO earthquakes (mag, mag_type, place, time, title, geom) VALUES %s",
                records,
                template="(%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))",
            )


cursor.execute(
    """
CREATE TEMP TABLE tbl AS
select per_hour_per_mag.hour as hour, per_hour_per_mag.mag as mag, per_hour_per_mag.cnt1 as cnt1, total_per_hour.cnt2 as cnt2, per_hour_per_mag.cnt1::numeric / total_per_hour.cnt2::numeric as probability from 
    (select extract(hour from time) as hour, mag::int as mag, count(*) as cnt1 from earthquakes where mag > 0 group by extract(hour from time), mag::int) as per_hour_per_mag,
    (select extract(hour from time) as hour, count(*) as cnt2 from earthquakes where mag > 0 group by extract(hour from time) order by hour desc) as total_per_hour
where per_hour_per_mag.hour = total_per_hour.hour
"""
)

cursor.execute(
    "select tbl.hour,tbl.mag, tbl.probability from tbl join (select max(probability) as probability, hour from tbl group by hour) as tb22 on tbl.probability=tb22.probability and tbl.hour = tb22.hour"
)
records = list([row for row in cursor.fetchall()])

connection.commit()


# shape({'coordinates': [-155.27034, 19.4165001, 0.98], 'type': 'Point'})
# x = shape({'coordinates': [-155.2786713, 19.4190006, 1.44], 'type': 'Point'})
# create extension postgis;
