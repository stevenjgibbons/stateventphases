#!/bin/sh
# https://earthquake.usgs.gov/earthquakes/eventpage/us6000mwnp/executive
# 2024-05-06 11:11:57 (UTC)68.007°N 177.618°W
network=$1
station=$2
location=$3
channel=$4
evlat=68.007
evlon=177.618
evdep=0.0
origt=2024-05-06T11:11:57
python orig_get_IRIS_wf.py --evlat $evlat --evlon $evlon --evdep $evdep --network $network --station $station --location $location --channel $channel --origt $origt
