Earthquake analysis
=============
An application that calls the USGS API and store the result in a relational database
In this project I used these technologies:

* `python` version: `3.6.0`
* `PostgreSQL` (to store the JSON data)
* `Postgis` latest

 
Run
-----------
Run the project with docker

```bash
docker-compose up 
```


After this, you can test the `visuals.py` program to see same visuals in my screen shot folder. 

Finding max mag query
-----------
```bash 
select * from earthquakes where mag is not null order by mag desc limit 1;
```

First query (second question)
-----------
```bash
 select tbl.hour,tbl.mag, tbl.probability from tbl join (select max(probability) as probability, hour from tbl group by hour) as tb22 on tbl.probability=tb22.probability and tbl.hour = tb22.hour
```

Second query (second question)
-----------
```bash
CREATE TEMP TABLE tbl AS
select per_hour_per_mag.hour as hour, per_hour_per_mag.mag as mag, per_hour_per_mag.cnt1 as cnt1, total_per_hour.cnt2 as cnt2, per_hour_per_mag.cnt1::numeric / total_per_hour.cnt2::numeric as probability from 
    (select extract(hour from time) as hour, mag::int as mag, count(*) as cnt1 from earthquakes where mag > 0 group by extract(hour from time), mag::int) as per_hour_per_mag,
    (select extract(hour from time) as hour, count(*) as cnt2 from earthquakes where mag > 0 group by extract(hour from time) order by hour desc) as total_per_hour
where per_hour_per_mag.hour = total_per_hour.hour
``` 




Other Information
-------------
In the zip file that I have sent, there is a `report.csv` which consists of some valuable information out of the dataset. With this report we can querry a lot more valuable information, which if I had time I could give more examples.

As Im writing this file, I saw that my second querry is finding the most probable magnitude per hour of the day. The answer you needed was the other way around, which means a matter of changing my group by. 



**Architecture**

```bash
create table earthquakes (
        id          BIGSERIAL PRIMARY KEY,
	mag         numeric,
        mag_type    varchar,
        place       varchar(500),
        time        timestamp without time zone,
        title       varchar
);
create extension postgis;
SELECT AddGeometryColumn ('earthquakes', 'geom', 4326, 'POINT', 3);
```


**Data [references](https://nam11.safelinks.protection.outlook.com/?url=https%3A%2F%2Fprotect-us.mimecast.com%2Fs%2FE79HCXDXOQtJVLqrcVGZo1%3Fdomain%3Dearthquake.usgs.gov&data=04%7C01%7Cfaykhan%40tesla.com%7C1a94fcb3c1034f0106d408d9924ff167%7C9026c5f486d04b9fbd39b7d4d0fb4674%7C0%7C0%7C637701694364091144%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C1000&sdata=YRLoKqRYig%2BZqj3dvzq2A0dE%2BXB7pbD2BiWuU%2FZvLO8%3D&reserved=0)**
