from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

my_map = Basemap(
    projection="robin", lat_0=0, lon_0=-100, resolution="l", area_thresh=1000.0
)

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color="coral")
my_map.drawmapboundary()

my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

x, y = my_map(-93.8993, 15.0222)
my_map.plot(x, y, "bo", markersize=12)

plt.show()

from decimal import Decimal

data = [
    (0.0, 1, Decimal("0.41996035909991838638")),
    (1.0, 1, Decimal("0.42011111111111111111")),
    (12.0, 1, Decimal("0.44932046892831206557")),
    (18.0, 1, Decimal("0.42388863942523574315")),
    (14.0, 1, Decimal("0.43132154006243496358")),
    (15.0, 1, Decimal("0.43504209741020995417")),
    (20.0, 1, Decimal("0.43132502308402585411")),
    (5.0, 1, Decimal("0.42489711934156378601")),
    (8.0, 1, Decimal("0.43036809815950920245")),
    (9.0, 1, Decimal("0.44700837247294261793")),
    (10.0, 1, Decimal("0.44085466556564822461")),
    (11.0, 1, Decimal("0.43556231003039513678")),
    (21.0, 1, Decimal("0.43332958253628896140")),
    (2.0, 1, Decimal("0.42227352682497801231")),
    (4.0, 1, Decimal("0.43225394120153387303")),
    (22.0, 1, Decimal("0.42967872388227364637")),
    (7.0, 1, Decimal("0.44572333685322069694")),
    (13.0, 1, Decimal("0.43868363862154610369")),
    (19.0, 1, Decimal("0.43984306887532693984")),
    (3.0, 1, Decimal("0.43033889187735341581")),
    (6.0, 1, Decimal("0.43875936280198333158")),
    (16.0, 1, Decimal("0.42900107411385606874")),
    (17.0, 1, Decimal("0.42489410231345715217")),
    (23.0, 1, Decimal("0.42497376705141657922")),
]


# Line Graph Example

import matplotlib.pyplot as plt

magnitudes = [i[1] for i in data]

# Compute average magnitude
avMagnitude = sum(magnitudes) / len(magnitudes)

# Plot magnitudes as a line graph
plt.plot(magnitudes)

# Add line for average magnitude: a line from (0,avMagnitude)
#                                       to (len(magnitudes), avMagnitude)
plt.plot([0, len(magnitudes)], [avMagnitude, avMagnitude])

# Label Axes and figure
plt.xlabel("Time")
plt.ylabel("Magnitude")
plt.title("Most probable magnitues per hour")

# Display histogram
plt.show()

# Clear before the next graph
plt.clf()


"""
Biggest Magnitude out of the data base

  id   | mag | mag_type |               place               |          time          |            st_astext             
-------+-----+----------+-----------------------------------+------------------------+----------------------------------
 95903 | 8.2 | mww      | near the coast of Chiapas, Mexico | 2017-09-08 06:49:19.18 | POINT Z (-93.8993 15.0222 47.39)
"""


# select id, mag, mag_type, place, time, st_astext(geom) from earthquakes where mag is not null order by mag desc limit 1;
