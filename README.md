# stateventphases
Two little python programs for listing the phase arrivals for an event and station location

Very crude!

#!/bin/sh
evlat=-26.044
evlon=178.381
evdep=600.0
stlat=-20.08765
stlon=146.24998
origt=2022-11-09T09:51:04
python stateventabstimes.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon --origt $origt

P             371.768   2022-11-09T09:57:15.768373Z
PP            428.772   2022-11-09T09:58:12.771872Z
PP            428.772   2022-11-09T09:58:12.772194Z
PP            429.122   2022-11-09T09:58:13.122114Z
PP            439.697   2022-11-09T09:58:23.697225Z
PP            439.828   2022-11-09T09:58:23.827595Z
PcP           553.006   2022-11-09T10:00:17.005815Z
S             671.794   2022-11-09T10:02:15.793627Z
PS            677.519   2022-11-09T10:02:21.519067Z
SP            677.519   2022-11-09T10:02:21.519067Z
PS            696.017   2022-11-09T10:02:40.017319Z
SP            696.017   2022-11-09T10:02:40.017319Z
PS            696.049   2022-11-09T10:02:40.048516Z
SP            696.049   2022-11-09T10:02:40.048516Z
SS            764.297   2022-11-09T10:03:48.296596Z
PcS           776.472   2022-11-09T10:04:00.472446Z
