'''
A top level test file to illustrate the use of the 'geodesy','Ephemerus','WaypointTarget_IO' and
     'RouteGenerator' modules in one program.
An example UTM waypoint file is read, the values are converted to Lat, Long and used to calculate
    the solar ephermerus for a current time (GMT) for each site.

 Lawrence Gray 2005

 Comment: I am amazed at the simplicity of writing a piece of code to do this, I like Python
'''

import Geodesy.geodesy as geodesy
import Ephemerus.Ephemerus as Ephemerus
import math
import time
import Map_db_IO.WaypointTarget_IO as wpio
import Map_db_IO.RouteGenerator as RG

mytestfile=r'c:\Documents and Settings\Owner\My Documents\Python\pyMap\test_sites_1.txt'
mytestfile=r"c:\Documents and Settings\Owner\My Documents\Python\pyMap\L'Acadie_sites.txt"

temp_db = wpio.ReadDatabase(mytestfile)
site_utm_db = wpio.generic2site_db(temp_db)

# iterate over all keys in the site database
# use the first tuple [0] in the list and use the first four items [0...4] in the tuple
# subsequent tuples for a given key, must be tested for their existence if they are to be used

gmt_current = time.gmtime()   # the current gmt based on the computers system time and timezone

for key in site_utm_db.keys():  
    lat_long = geodesy.UTM2LL(site_utm_db[key][0][0],    # datum
                              site_utm_db[key][0][1],    # northing
                              site_utm_db[key][0][2],    # easting
                              site_utm_db[key][0][3]     # UTMZone
                              )
    solar_dat = Ephemerus.Solar(math.radians(lat_long[0]),      # latitude
                                 -math.radians(lat_long[1]),    # longitude, Note the sign change
                                 gmt_current[0],                # current year
                                 gmt_current[1],                # current month
                                 gmt_current[2],                # current day
                                 gmt_current[3],                # current hour
                                 gmt_current[4],                # current minutes
                                 gmt_current[5],                # current seconds
                                 00                             # hundredths of seconds
                                 )
                               
                                            
    print key, lat_long, solar_dat

# demonstrates recognition of the database value as a single point, line or block site

for key in site_utm_db.keys():
    sitetype = RG.SiteType(site_utm_db[key])
    for x in range(0, len(site_utm_db[key]), 1):
                   if x==0:
                       print key, x, site_utm_db[key][0],
                       if sitetype == 0:
                           print "Point Target"
                       elif sitetype == 1:
                           print 'Line Target'
                       else:
                           print 'Block Target'
                   else:
                       print key, x, site_utm_db[key][x]

# we need a demonstration of doing something with a picked site                    

