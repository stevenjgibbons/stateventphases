#!/bin/sh
evlat=-26.044
evlon=178.381
evdep=600.0
stlat=-20.08765
stlon=146.24998
origt=2022-11-09T09:51:04
python stateventabstimes.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon --origt $origt
