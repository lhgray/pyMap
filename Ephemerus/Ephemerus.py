#-----------------------------------------------------------------------------
# Name:        Ephemerus.py
# Purpose:     Calculate the Solar Elevation and Solar Azimuth for a specified
#               (latitude, longitude) at a specified time
#
# Author:      <Lawrence Gray>
#
# Created:     2005/25/02
# RCS-ID:      $Id: Ephemerus.py $
# Copyright:   (c) 2004
# Licence:     <your licence>
# New field:   Whatever
#-----------------------------------------------------------------------------
import math

#===============================================================================
# Function Definitions
#===============================================================================

def Julian(
    year,   # int, 'yyyy' format
    month,  # int, 'mm' format
    day     # int, 'dd' format
    ):

    temp=math.modf((month-14.0)/12.0)[1]
    jd= math.modf(day - 32075 + 1461*(year + 4800 + temp)/4)[1]
    jd= math.modf(jd + 367*(month - 2 - temp*12)/12)[1]
    jd= math.modf(jd - 3*math.modf((year+4900+temp)/100)[1] /4)[1]

    return(jd)
                
    
def Solar(  # Computes the Solar Ephemerus
    lat,    # real, latitude expressed in radians
    long,   # real, longitude expressed in radians
    year,   # int, year
    month,  # int, month
    day,    # int, day
    hour,   # int, hour (UTC)
    min,    # int, minute
    sec,    # int, seconds
    hun     # int, hundreths of secon
    ):

    c= math.pi/180
    c1= 279.4574*c
    c2= 0.985647*c
    c3= -120.5
    c4= -0.142
    c5= -429.8
    c6= 0.033
    c7= 596.5
    c8= -2
    c9= 4.2
    cc= 17.3
    cb= -12.8
    q0= 65536
    t0= 60*60*60*24
    
    ND = Julian(year, month, day) - Julian(year, 1, 1) +1

    TE = (3600*hour + 60*min + sec + 0.01*hun) * 60

    X = (year-1965)*365 +5 + ND +TE/t0

    L = c1 + (c2*X)

    X = X/365.2422

    EqnTime = ((c3+c4*X)*math.sin(L) + (c5+c6*X)*math.cos(L) +
               c7*math.sin(L*2) + c8*math.cos(L*2) + c9*math.sin(L*3) +
               cc*math.cos(L*3) + cb*math.sin(L*4))

    EqnTimeJif = EqnTime * 60

    Decln = math.atan(0.4336*math.sin(L-c*EqnTime/240))

    HourAng = (TE/t0) + (EqnTimeJif/t0)
    HourAng = HourAng*2*math.pi - long

    SinElev = (math.sin(lat)*math.sin(Decln) -
               math.cos(HourAng)*math.cos(lat)*math.cos(Decln))

    CosElev = 1 - SinElev*SinElev
    if (CosElev > 0):
        CosElev = math.sqrt(CosElev)

    SolarElev = math.atan(SinElev/CosElev)
    SolarElev = math.degrees(SolarElev)

    SinAzm = math.sin(HourAng)*math.cos(Decln)/CosElev

    CosAzm = 1 - SinAzm*SinAzm
    if (CosAzm > 0):
        CosAzm = math.sqrt(CosAzm)
        TZ = math.fabs(math.atan(SinAzm/CosAzm))
    else:
        TZ = math.pi/2

    if (math.sin(Decln) < math.sin(lat)*SinElev):
        TZ = math.pi - TZ
    if (SinAzm < 0):
        TZ = math.pi*2 - TZ

    SolarAzm = TZ
    SolarAzm = math.degrees(TZ)

    return(SolarElev, SolarAzm)

# ==============================================================================
# test stuff

if __name__ == "__main__":

    lat = 45
    long = 45
    year = 2005
    month = 2
    day = 25
    hour = 18
    min = 0
    sec = 0
    hun = 0

#test for a sequence of longitudes
    print ('%s%4i%s%02i%s%02i%s%02i%s%02i%s%02i%s%02i%s%5.1f%s'
           %("On ",year,"/",month,"/",day,
             " at ",hour,":",min,":",sec,".",hun,
             " at ",lat, " degrees of latitude"))
    print '%18s%18s%18s' %('Longitude(deg)','Elevation(deg)','Azimuth(deg)')
    for x in range(40,50,1):
        Result = Solar(math.radians(lat),
                                math.radians(x),year,month,day,hour,min,sec,hun)
        print '%13.1f%18.2f%18.2f' %(x,Result[0],Result[1])
    print "\n"

#test for a sequence of latitudes
    print ('%s%4i%s%02i%s%02i%s%02i%s%02i%s%02i%s%02i%s%5.1f%s'
           %("On ",year,"/",month,"/",day," at ",
            hour,":",min,":",sec,".",hun," at ",
            long," degrees of longitude"))
    print '%18s%18s%18s' %('Latitude(deg)','Elevation(deg)','Azimuth(deg)')
    for x in range(40,50,1):   
        Result = Solar(math.radians(x),math.radians(long), 
            year,month,day,hour,min,sec,hun)
        print '%13.1f%18.2f%18.2f' %(x, Result[0],Result[1])
    print "\n"

# test for a sequence of hours
    print ('%s%4i%s%02i%s%02i%s%5.1f%s%5.1f%s'
           %("On ", year,"/",month,"/",day," at ",
             lat, " degrees of latitude at ",
             long, " degrees of longitude"))
    print '%20s%18s%18s' %('Time(UTC)','Elevation(deg)','Azimuth(deg)')
    for x in range(00,25,1):
        Result = Solar(math.radians(lat),
                                math.radians(long),year,month,day,x,min,sec,hun)
        print ('%s%2i%s%02i%s%02i%s%02i%18.2f%18.2f' 
                %("\t",x,":",min,":",sec,".",hun,Result[0], Result[1]))
