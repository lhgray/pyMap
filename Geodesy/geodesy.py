# LatLong- UTM conversion.cpp
# Lat Long - UTM, UTM - Lat Long conversions

"""
Reference ellipsoids derived from Peter H. Dana's website- 
http://www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
Department of Geography, University of Texas at Austin
Internet: pdana@mail.utexas.edu
3/22/95

Source
Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to Department of Defense World Geodetic System
1984 Technical Report. Part I and II. Washington, DC: Defense Mapping Agency
"""

import math

#=====================================================================
#   Constants
#=====================================================================
ellipsoid = (( -1, "Placeholder", 0, 0),     # placeholder only, To allow array indices to match id numbers
             ( 1, "Airy", 6377563, 0.00667054),
             ( 2, "Australian National", 6378160, 0.006694542),
             ( 3, "Bessel 1841", 6377397, 0.006674372),
             ( 4, "Bessel 1841 (Nambia) ", 6377484, 0.006674372),
             ( 5, "Clarke 1866", 6378206, 0.006768658),
             ( 6, "Clarke 1880", 6378249, 0.006803511),
             ( 7, "Everest", 6377276, 0.006637847),
             ( 8, "Fischer 1960 (Mercury) ",6378166, 0.006693422),
             ( 9, "Fischer 1968", 6378150, 0.006693422),
             ( 10, "GRS 1967", 6378160, 0.006694605),
             ( 11, "GRS 1980", 6378137,0.00669438),
             ( 12, "Helmert 1906", 6378200, 0.006693422),
             ( 13, "Hough", 6378270, 0.00672267),
             ( 14, "International", 6378388, 0.00672267),
             ( 15, "Krassovsky", 6378245, 0.006693422),
             ( 16, "Modified Airy", 6377340, 0.00667054),
             ( 17, "Modified Everest", 6377304, 0.006637847),
             ( 18, "Modified Fischer 1960", 6378155, 0.006693422),
             ( 19, "South American 1969", 6378160, 0.006694542),
             ( 20, "WGS 60", 6378165, 0.006693422),
             ( 21, "WGS 66", 6378145, 0.006694542),
             ( 22, "WGS-72", 6378135, 0.006694318),
             ( 23, "WGS-84", 6378137, 0.00669438)
             )  # end of ellipsoid definitions

EquatorialRadius = 2        # predefined index number
eccentricitySquared = 3     # predefined index number
	
#=====================================================================
#
#   Function Definitions
#
#=====================================================================

def LL2UTM(
    ReferenceEllipsoid, # int, see defined constant ellipsoid
    Lat,                # float
    Long                # float
    ):

    # converts lat/long to UTM coords.  Equations from USGS Bulletin 1532 
    # East Longitudes are positive, West longitudes are negative. 
    # North latitudes are positive, South latitudes are negative
    # Lat and Long are in decimal degrees
	# Written by Chuck Gantz- chuck.gantz@globalstar.com

	# adapted to Python by Lawrence Gray 

    global EquatorialRadius
    global eccentricitySquared
    
    a = ellipsoid[ReferenceEllipsoid][EquatorialRadius] # the EquatorialRadius 
    eccSquared = ellipsoid[ReferenceEllipsoid][eccentricitySquared] # the eccentricitySquared
    k0 = 0.9996

    # Make sure the longitude is between -180.00 .. 179.9
    LongTemp = (Long+180)-math.modf((Long+180)/360)[1]*360-180 #  -180.00 .. 179.9

    LatRad = math.radians(Lat)
    LongRad = math.radians(LongTemp)

    ZoneNumber = int(math.modf((LongTemp+180)/6)[1]) + 1
  
    if((Lat >= 56.0) and (Lat < 64.0) and (LongTemp >= 3.0) and (LongTemp < 12.0 )):
        ZoneNumber = 32

    # Special zones for Svalbard
    if( Lat >= 72.0 and Lat < 84.0 ):
      if(LongTemp >= 0.0  and LongTemp <  9.0 ):
          ZoneNumber = 31
      elif( LongTemp >= 9.0  and LongTemp < 21.0 ):
              ZoneNumber = 33
      elif( LongTemp >= 21.0 and LongTemp < 33.0 ):
          ZoneNumber = 35
      elif( LongTemp >= 33.0 and LongTemp < 42.0 ):
              ZoneNumber = 37
    LongOrigin = (ZoneNumber - 1)*6 - 180 + 3  # +3 puts origin in middle of zone
    LongOriginRad = math.radians(LongOrigin)

    # compute the UTM Zone from the latitude and longitude
    #    print '%s%d%c' %(UTMZone, ZoneNumber, UTMLetterDesignator(Lat))

    eccPrimeSquared = (eccSquared)/(1-eccSquared)
    N = a/math.sqrt(1-eccSquared*math.sin(LatRad)*math.sin(LatRad))
    T = math.tan(LatRad)*math.tan(LatRad)
    C = eccPrimeSquared*math.cos(LatRad)*math.cos(LatRad)
    A = math.cos(LatRad)*(LongRad-LongOriginRad)

    M = (a*((1- eccSquared/4-3*eccSquared*eccSquared/64-5*eccSquared*eccSquared*eccSquared/256)*LatRad
            -(3*eccSquared/8 + 3*eccSquared*eccSquared/32 + 45*eccSquared*eccSquared*eccSquared/1024)*math.sin(2*LatRad)
            +(15*eccSquared*eccSquared/256 + 45*eccSquared*eccSquared*eccSquared/1024)*math.sin(4*LatRad) 
            -(35*eccSquared*eccSquared*eccSquared/3072)*math.sin(6*LatRad)))
    
    UTMEasting = ((k0*N*(A+(1-T+C)*A*A*A/6 + (5-18*T+T*T+72*C-58*eccPrimeSquared)*A*A*A*A*A/120)
                    + 500000.0))

    UTMNorthing = ((k0*(M+N*math.tan(LatRad)*(A*A/2+(5-T+9*C+4*C*C)*A*A*A*A/24
                                         +(61-58*T+T*T+600*C-330*eccPrimeSquared)*A*A*A*A*A*A/720))))
    if(Lat < 0):
        UTMNorthing += 10000000.0   # 10000000 meter offset for southern hemisphere

    '''
    if(Lat <0):
        UTMZone = str(ZoneNumber)+"S"
    else:
        UTMZone = str(ZoneNumber)+"N"
    '''
    UTMZone = str(ZoneNumber)+UTMLetterDesignator(Lat)

    return(UTMNorthing, UTMEasting, UTMZone, UTMLetterDesignator(Lat))

#============================================================================================
def UTMLetterDesignator(Lat):

    # This routine determines the correct UTM letter designator for the given latitude
    # returns 'Z' if latitude is outside the UTM limits of 84N to 80S
	# Written by Chuck Gantz- chuck.gantz@globalstar.com

    if((84 >= Lat) and (Lat >= 72)):
        LetterDesignator = 'X'
    elif((72 > Lat) and (Lat >= 64)):
        LetterDesignator = 'W'
    elif((64 > Lat) and (Lat >= 56)):
        LetterDesignator = 'V'
    elif((56 > Lat) and (Lat >= 48)):
        LetterDesignator = 'U'
    elif((48 > Lat) and (Lat >= 40)):
        LetterDesignator = 'T'
    elif((40 > Lat) and (Lat >= 32)):
        LetterDesignator = 'S'
    elif((32 > Lat) and (Lat >= 24)):
        LetterDesignator = 'R'
    elif((24 > Lat) and (Lat >= 16)):
        LetterDesignator = 'Q'
    elif((16 > Lat) and (Lat >= 8)):
        LetterDesignator = 'P'
    elif(( 8 > Lat) and (Lat >= 0)):
        LetterDesignator = 'N'
    elif(( 0 > Lat) and (Lat >= -8)):
        LetterDesignator = 'M'
    elif((-8 > Lat) and (Lat >= -16)):
        LetterDesignator = 'L'
    elif((-16 > Lat) and (Lat >= -24)):
        LetterDesignator = 'K'
    elif((-24 > Lat) and (Lat >= -32)):
        LetterDesignator = 'J'
    elif((-32 > Lat) and (Lat >= -40)):
        LetterDesignator = 'H'
    elif((-40 > Lat) and (Lat >= -48)):
        LetterDesignator = 'G'
    elif((-48 > Lat) and (Lat >= -56)):
        LetterDesignator = 'F'
    elif((-56 > Lat) and (Lat >= -64)):
        LetterDesignator = 'E'
    elif((-64 > Lat) and (Lat >= -72)):
        LetterDesignator = 'D'
    elif((-72 > Lat) and (Lat >= -80)):
        LetterDesignator = 'C'
    else: LetterDesignator = 'Z' # This is here as an error flag to show that the Latitude is outside the UTM limits

    return(LetterDesignator)



def UTM2LL(
    ReferenceEllipsoid, # int
    UTMNorthing,        # float
    UTMEasting,         # float
    UTMZone             # char
    ):

# converts UTM coords to lat/long.  Equations from USGS Bulletin 1532 
# East Longitudes are positive, West longitudes are negative. 
# North latitudes are positive, South latitudes are negative
# Lat and Long are in decimal degrees. 
	# Written by Chuck Gantz- chuck.gantz@globalstar.com
	# adapted to Python by Lawrence Gay

    global ellipsoid
    global EquatorialRadius
    global eccentricitySquared
    
    k0 = 0.9996
    a = ellipsoid[ReferenceEllipsoid][EquatorialRadius] # the EquatorialRadius 
    eccSquared = ellipsoid[ReferenceEllipsoid][eccentricitySquared] # the eccentricitySquared
    e1 = (1-math.sqrt(1-eccSquared))/(1+math.sqrt(1-eccSquared))

    x = UTMEasting - 500000.0   # remove 500,000 meter offset for longitude
    y = UTMNorthing

    # ZoneNumber = strtoul(UTMZone, &ZoneLetter, 10)  # this line extarcts a string to long integer, base 10
    ZoneNumber = int(UTMZone[:-1])                   # everything except the last character eg. '17N', first 2 characters
    ZoneLetter = UTMZone[len(UTMZone)-1].upper()    # last character, must be set to upper case
    
    if(ZoneLetter >= 'N'):
        NorthernHemisphere = 1  # point is in northern hemisphere
    else:
        NorthernHemisphere = 0  # point is in southern hemisphere
        y -= 10000000.0 # remove 10,000,000 meter offset used for southern hemisphere

    LongOrigin = (ZoneNumber - 1)*6 - 180 + 3  # +3 puts origin in middle of zone

    eccPrimeSquared = (eccSquared)/(1-eccSquared)

    M = y / k0
    mu = M/(a*(1-eccSquared/4-3*eccSquared*eccSquared/64-5*eccSquared*eccSquared*eccSquared/256))

    phi1Rad = (mu+(3*e1/2-27*e1*e1*e1/32)*math.sin(2*mu)
               + (21*e1*e1/16-55*e1*e1*e1*e1/32)*math.sin(4*mu)
               + (151*e1*e1*e1/96)*math.sin(6*mu))
    phi1 = math.degrees(phi1Rad)

    N1 = a/math.sqrt(1-eccSquared*math.sin(phi1Rad)*math.sin(phi1Rad))
    T1 = math.tan(phi1Rad)*math.tan(phi1Rad)
    C1 = eccPrimeSquared*math.cos(phi1Rad)*math.cos(phi1Rad)
    R1 = a*(1-eccSquared)/pow(1-eccSquared*math.sin(phi1Rad)*math.sin(phi1Rad), 1.5)
    D = x/(N1*k0)

    Lat = phi1Rad - (N1*math.tan(phi1Rad)/R1)*(D*D/2-(5+3*T1+10*C1-4*C1*C1-9*eccPrimeSquared)*D*D*D*D/24
					+(61+90*T1+298*C1+45*T1*T1-252*eccPrimeSquared-3*C1*C1)*D*D*D*D*D*D/720)
    Latitude = math.degrees(Lat)

    Long = (D-(1+2*T1+C1)*D*D*D/6+(5-2*C1+28*T1-3*C1*C1+8*eccPrimeSquared+24*T1*T1)
					*D*D*D*D*D/120)/math.cos(phi1Rad)
    Longitude = LongOrigin + math.degrees(Long)

    return(Latitude, Longitude)

#============================================================================================
#   test stuff
#============================================================================================

if __name__ == "__main__":
    
    Lat = 47.37816667  # degrees
    Long = 8.23250000  # degrees
    RefEllipsoid = 23  # WGS-84

    print Lat, Long,
    UTMresult = LL2UTM(RefEllipsoid, Lat, Long)
    print UTMresult
    LLresult = UTM2LL(RefEllipsoid, UTMresult[0], UTMresult[1], UTMresult[2])
    print LLresult, '\n'

    for Long in range(-177,180,18):  # Each long should be in the centre of a zone
        print Lat, Long,
        print LL2UTM(RefEllipsoid, Lat, Long)

    print '\n'
    Long = 8.2325000

    for Lat in range(-76,90,8):  # Each lat should be in the centre of a zone
        print Lat, Long,
        print LL2UTM(RefEllipsoid, Lat, Long)


