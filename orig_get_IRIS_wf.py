# Steven J. Gibbons
# NGI, Sognsveien 72, Oslo
# 2022/11/09
# Take in source coordinates and station coordinates and
# origintime
# writes out phase lists with relative times
#
try:
    import os
    import sys
    import argparse
    import numpy as np
    import geographiclib
    from geographiclib.geodesic import Geodesic
    import math
    import obspy
    from obspy.taup import TauPyModel
    from obspy import UTCDateTime
    from obspy.clients.fdsn import RoutingClient
except ImportError as ie:
    miss_mod = ie.args[0].split()[3]
    print("\nThe Python module '" + miss_mod + "' is required.")
    print("Please install it and run again.\n")
    exit(1)

#==========================================================================
class llLocation:
    def __init__( self, lat, lon ):
        self.lat = lat
        self.lon = lon

#==========================================================================
def dist_between_locs_km( loc1, loc2 ):
    geod = Geodesic.WGS84
    g = geod.Inverse( loc1.lat, loc1.lon, loc2.lat, loc2.lon )
    return 0.001 * g['s12']

#==========================================================================
def dist_between_locs_deg( loc1, loc2 ):
    geod = Geodesic.WGS84
    g = geod.Inverse( loc1.lat, loc1.lon, loc2.lat, loc2.lon )
    return g['a12']

#==========================================================================
def source_to_receiver_azimuth( rloc, sloc ):
    geod = Geodesic.WGS84
    g = geod.Inverse( sloc.lat, sloc.lon, rloc.lat, rloc.lon )
    azimuth = g['azi1']
    if ( azimuth < 0.0 ):
        azimuth = azimuth + 360.0
    return azimuth

#==========================================================================
def receiver_to_source_backazimuth( rloc, sloc ):
    geod = Geodesic.WGS84
    g = geod.Inverse( rloc.lat, rloc.lon, sloc.lat, sloc.lon )
    backazimuth = g['azi1']
    if ( backazimuth < 0.0 ):
        backazimuth = backazimuth + 360.0
    return backazimuth

#==========================================================================
def new_location_azi_distkm( loc1, azi, distkm ):
    geod = Geodesic.WGS84
    g = geod.Direct( loc1.lat, loc1.lon, azi, 1000.0 * distkm )
    return llLocation( g['lat2'], g['lon2'] )

#==========================================================================
def src_rec_phases( rloc, sloc, source_depth_in_km, origt, phase ):
    ddeg = dist_between_locs_deg( rloc, sloc )
    model = TauPyModel( model = "ak135" )
    print ("Dist in degrees is ", ddeg )
    arrivals = model.get_travel_times( source_depth_in_km = source_depth_in_km,
                                           distance_in_degree = ddeg )
    numarrivals = len( arrivals )
    for iarr in range( 0, numarrivals ):
        phasename  = arrivals[iarr].name
        ttime      = arrivals[iarr].time
        arrtime    = origt + ttime
        outstring  = phasename.ljust(8) + " "
        outstring += "{:.3f}".format( ttime ).rjust(12) + "   "
        outstring += str( arrtime )
        print ( outstring )
        # print ( arrivals[iarr].name, arrivals[iarr].time )

    ind = -1
    if ( phase == "P1" ):
        for iarr in range( 0, numarrivals ):
            if ( ind == -1 and arrivals[iarr].name[0] == 'P' ):
                ind = iarr
                ttime      = arrivals[iarr].time
                arrtime    = origt + ttime
                return arrtime
    elif ( phase == "S1" ):
        for iarr in range( 0, numarrivals ):
            if ( ind == -1 and arrivals[iarr].name[0] == 'S' ):
                ind = iarr
                ttime      = arrivals[iarr].time
                arrtime    = origt + ttime
                return arrtime
    else:
        for iarr in range( 0, numarrivals ):
            if ( ind == -1 and arrivals[iarr].name[0] == phase ):
                ind = iarr
                ttime      = arrivals[iarr].time
                arrtime    = origt + ttime
                return arrtime

#==========================================================================
scriptname = sys.argv[0]
numarg     = len(sys.argv) - 1
text       = 'Specify '
text      += '--network [network] '
text      += '--station [station] '
text      += '--location [location] '
text      += '--channel [channel] '
text      += '--evlon [evlon] '
text      += '--evlat [evlat] '
text      += '--evdep [evdep] '
text      += '--origt [origt] '
parser     = argparse.ArgumentParser( description = text )
parser.add_argument("--evlat", help="event latitude", default=None, required=True )
parser.add_argument("--evlon", help="event longitude", default=None, required=True )
parser.add_argument("--evdep", help="event depth (km)", default=0.0, required=False )
parser.add_argument("--network", help="network", default=None, required=True )
parser.add_argument("--station", help="station", default=None, required=True )
parser.add_argument("--location", help="location", default=None, required=True )
parser.add_argument("--channel", help="channel", default=None, required=True )
parser.add_argument("--origt", help="origintime", default=None, required=True )
parser.add_argument("--phase", help="phase", default="P1", required=False )

args = parser.parse_args()

evlat        = float( args.evlat )
evlon        = float( args.evlon )
evdep        = float( args.evdep )
phase        = args.phase
network      = args.network
station      = args.station
location     = args.location
if ( location == "X" ):
    location = ""
channel      = args.channel
origt        = UTCDateTime( args.origt )
endtime      = origt + 900.0

evloc = llLocation( evlat, evlon )
#
# Now need to find station lat and lon
#
client = RoutingClient("iris-federator")
inv = client.get_stations(
    channel=channel, starttime=origt, endtime=endtime,
    station=station, network=network, location=location )
print(inv)  
st =  client.get_waveforms(
    channel=channel, starttime=origt, endtime=endtime,
    station=station, network=network, location=location )
# st.plot()
for y, tr in enumerate(st):
    networkID, stationID, locationID, channelID = tr.get_id().split(".")
    for net in inv:
        for stat in net:
            if networkID == net.code:
                if stationID == stat.code:
                    tr.stats["coordinates"] = {} # add the coordinates to the dictionary, needed for the section plot
                    tr.stats["coordinates"]["latitude"] = stat.latitude
                    tr.stats["coordinates"]["longitude"] = stat.longitude
                    stlat                               = stat.latitude
                    stlon                               = stat.longitude
                    stelev                              = stat.elevation

print ("Station ", stlat, stlon, stelev )
print ("Event ",   evlat, evlon )
stloc = llLocation( stlat, stlon )
arrtime = src_rec_phases( stloc, evloc, evdep, origt, phase )
print ( arrtime )
time1 = UTCDateTime( arrtime ) - 60.0
time2 = UTCDateTime( arrtime ) + 60.0
print ( "time1", time1 )
print ( "time2", time2 )
print ( "channel", channel )
print ( "station", station )
print ( "network", network )
print ( "location", location )
evlatstring  = "{:.4f}".format( stlat ).rjust(8)
evlonstring  = "{:.4f}".format( stlon ).rjust(9)
evdepstring  = "{:.3f}".format( stlon ).rjust(8)
stlatstring  = "{:.6f}".format( stlat ).rjust(10)
stlonstring  = "{:.6f}".format( stlon ).rjust(11)
stelevstring = "{:.3f}".format( stelev ).rjust(9)
string  = network + "." + station + " "
string += stlatstring   + " "
string += stlonstring   + " "
string += stelevstring   + " "
string += phase   + " "
string += str( arrtime )   + " "
string += evlatstring   + " "
string += evlonstring   + " "
string += evdepstring   + "\n"
outfile = "predicted_times.txt"
file1   = open( outfile, "a" )
file1.write( string )
file1.close()

st =  client.get_waveforms(
    channel=channel, starttime=time1, endtime=time2,
    station=station, network=network, location=location )
st.plot()


