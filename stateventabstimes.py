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
def src_rec_phases( rloc, sloc, source_depth_in_km, origt ):
    ddeg = dist_between_locs_deg( rloc, sloc )
    model = TauPyModel( model = "ak135" )
    arrivals = model.get_travel_times( source_depth_in_km = 0.0,
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

#==========================================================================
scriptname = sys.argv[0]
numarg     = len(sys.argv) - 1
text       = 'Specify '
text      += '--stlat [stlat] '
text      += '--stlon [stlon] '
text      += '--evlat [evlat] '
text      += '--evlon [evlon] '
text      += '--evdep [evdep] '
parser     = argparse.ArgumentParser( description = text )
parser.add_argument("--evlat", help="event latitude", default=None, required=True )
parser.add_argument("--evlon", help="event longitude", default=None, required=True )
parser.add_argument("--evdep", help="event depth (km)", default=0.0, required=False )
parser.add_argument("--stlat", help="station latitude", default=None, required=True )
parser.add_argument("--stlon", help="station longitude", default=None, required=True )
parser.add_argument("--origt", help="origintime", default=None, required=True )

args = parser.parse_args()

evlat        = float( args.evlat )
evlon        = float( args.evlon )
evdep        = float( args.evdep )
stlat        = float( args.stlat )
stlon        = float( args.stlon )
origt        = UTCDateTime( args.origt )

evloc = llLocation( evlat, evlon )
stloc = llLocation( stlat, stlon )
src_rec_phases( stloc, evloc, evdep, origt )


