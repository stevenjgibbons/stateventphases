# stateventphases  

Release v1.0.0 is permanently stored on Zenodo with DOI 10.5281/zenodo.10629194  
[![DOI](https://zenodo.org/badge/564022209.svg)](https://zenodo.org/doi/10.5281/zenodo.10629194)  

https://doi.org/10.5281/zenodo.10629194    



Two little python programs for listing the phase arrivals for an event and station location

(1) **stateventphases.py** simply returns lines of ASCII text containing two columns: (1) the phase name and (2) the number of seconds after the origin time at which you would expect to observe the phase.  

The calling sequence is  

```
python stateventphases.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon
```

An example for the station IU.CTAO is given in the shell script *run_CTAO.sh*  

```
#!/bin/sh
# Set event latitude, longitude, event depth (in km), station latitude and longitude
evlat=-26.044
evlon=178.381
evdep=600.0
stlat=-20.08765
stlon=146.24998
python stateventphases.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon
```

The output from this particular run looks like  
```
P             371.768
PP            428.772
PP            428.772
PP            429.122
PP            439.697
PP            439.828
PcP           553.006
S             671.794
PS            677.519
...
PKPPKP       2524.304
SKIKSSKIKS     3262.895
```

(2) **stateventabstimes.py** is almost identical but takes an additional argument, *origt*  

```
python stateventabstimes.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon --origt $origt
```

so a complete call could look a little like:

```
#!/bin/sh  
evlat=-26.044  
evlon=178.381  
evdep=600.0  
stlat=-20.08765  
stlon=146.24998  
origt=2022-11-09T09:51:04  
python stateventabstimes.py --evlat $evlat --evlon $evlon --evdep $evdep --stlat $stlat --stlon $stlon --origt $origt
```

(as found in the shell script *run_CTAO_origt.sh*). This gives the output

```
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
```

Both programs are based upon the **obspy** software: *https://docs.obspy.org/* and *https://github.com/obspy/obspy*  

