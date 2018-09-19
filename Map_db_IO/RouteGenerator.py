<<<<<<< .mine
#        
# Module to Generate Routing Waypoints based on the 'Site' selected 
#   from a site database and a plan selected from a planning database 
#
#  RouteGenerator Module - import as <RG> to abbreviate
#

import math
import Ephemerus.Ephemerus as Ephemerus
import Geodesy.geodesy as geodesy
import time
import Numeric as N
import LinearAlgebra as LA

debug = 0

#==============================================================================
#
#   function SiteType
#
def SiteType(WPt_List):    # a list of waypoints defined for the selected site
    '''
    A function to determine the type of target by assessing the number of
    waypoints in Wpt_List. Returns an integer 'sitetype'
    
    1 waypoint indicates a point target, SiteType = 0
        
    2 waypoints indicate a line target, SiteType = 1
    
    2 or more waypoints indicate an extended target area, SiteType = 2
    '''
    if len(WPt_List)==2:
        sitetype=1
    elif len(WPt_List)>2:
        sitetype=2
    else:
        sitetype=0

    return(sitetype)

#==============================================================================
#
#   function UTM2Solar
#
# XXX Update UTM2Solar to accept an input time to override the current time
#
def UTM2Solar(Input_Pt):    # a function to determine the current solar ephemerus
                            # for the selected Waypoint
    
    lat_long = geodesy.UTM2LL(Input_Pt[0],    # datum
                              Input_Pt[1],    # northing
                              Input_Pt[2],    # easting
                              Input_Pt[3]     # UTMZone
                              )

    # the current gmt based on the computers system time and timezone
    gmt_current = time.gmtime()

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
    return(solar_dat)

#==============================================================================
#
#   function GridRangeBearing
#
#   function that returns the range and grid bearing between two points
#       maybe this should made general by inputting utm tuples

def GridRangeBearing(from_wpt,  # list, utm coordinates for the waypoint flying from
                     to_wpt     # list, utm coordinates for the waypoint flying to
                     ):
    
    n2=to_wpt[1]    # to northing
    e2=to_wpt[2]    # to easting
    n1=from_wpt[1]  # from northing
    e1=from_wpt[2]  # from easting
    
    # slopeangle is the angle defined by two points accounting for the
    #   order if the points as the direction

    try:
        theta = math.degrees(math.atan((n2-n1)/(e2-e1)))
    except ZeroDivisionError:
        if n2 > n1:
            theta = 90.0
        elif n2 < n1:
            theta = 270.0
        else:
            print 'Coincident Points entered in function GridRangeBearing'
            Range = 0
            Bearing = 0
            return(Range, Bearing)
        slopeangle = theta
        
    if e2>e1:  
        if n2<>n1: slopeangle=theta 
        else: slopeangle=0.0
    if e2<e1:
        if n2<>n1: slopeangle=180.0+theta
        else: slopeangle=180.0
    # note the condition of e2=e1 has been handled in the try/exception
    #   above
            
    Bearing = math.fmod(450.0-slopeangle, 360.0)
    Range = math.sqrt((n2-n1)*(n2-n1)+(e2-e1)*(e2-e1))

    return(Range, Bearing)
#==============================================================================
#
#   function Offset
#
#   a simple function to return the utm offset if the distance(range)
#       and bearing between two points is known
#

def Offset(Range,
           Bearing
           ):
    Northing = math.sin(math.radians(math.fmod(450-Bearing, 360)))*Range
    Easting = math.cos(math.radians(math.fmod(450-Bearing, 360)))*Range        
    return(Northing, Easting)

#==============================================================================
#
#   function NERBsIntersect
#
#       a function to compute the intersection point of two NERB's 
#          ie. Lines defined as (Northing, Easting, Range, Bearing)
#

def NERBsIntersect(nerb1,
                   nerb2
                   ):
    '''
    nerb1 - type list, a line defined by a northing, easting, range & bearing
    
    nerb2 - type list, a line defined by a northing, easting, range & bearing

    returns a northing, easting and flag

    flag indicates that the intersection point lies within the range & bearing
    of nerb1
    '''
    theta1 = math.fmod(450-nerb1[3], 360)   # convert bearing to math angle
    theta2 = math.fmod(450-nerb2[3], 360)   # yes, it's the same formula for
                                            #   math to bearing angle
##    if theta1 == 90 or theta1 == 270:
##        a1 = 0
##        b1 = -1
##        c1 = nerb1[1]
##    else:
##        a1 = 1
##        b1 = -math.tan(math.radians(theta1))
##        c1 = nerb1[0]-nerb1[1]*math.tan(math.radians(theta1))
##
##    if theta2 == 90 or theta2 == 270:
##        a2 = 0
##        b2 = -1
##        c2 = nerb2[1]
##    else:
##        a2 = 1
##        b2 = -math.tan(math.radians(theta2))
##        c2 = nerb2[0]-nerb2[1]*math.tan(math.radians(theta2))
##
##    a = N.array([(a1,b1),(a2,b2)])
##    b = N.array([(c1),(c2)])
##    try:
##        c = LA.solve_linear_equations(a,b)
##    except LA.LinAlgError:
##        # print'Singular matrix'
##        return (0,0,0)  # return zero's, the flag is zero so the
##                        #   data is ignored anyway
    # New Section
    if theta1 == 90 or theta1 == 270:
        c = [nerb2[0]-math.tan(math.radians(theta2))*(nerb2[1]-nerb1[1]), nerb1[1]]
    elif theta2 == 90 or theta2 == 270:
        c = [nerb1[0]-math.tan(math.radians(theta1))*(nerb1[1]-nerb2[1]), nerb2[1]]
    else:
        a1 = 1
        b1 = -math.tan(math.radians(theta1))
        c1 = nerb1[0]-nerb1[1]*math.tan(math.radians(theta1))
        a2 = 1
        b2 = -math.tan(math.radians(theta2))
        c2 = nerb2[0]-nerb2[1]*math.tan(math.radians(theta2))

        a = N.array([(a1,b1),(a2,b2)])
        b = N.array([(c1),(c2)])
        try:
            c = LA.solve_linear_equations(a,b)
        except LA.LinAlgError:
            # print'Singular matrix'
            return (0,0,0)  # return zero's, the flag is zero so the
                            #   result is ignored anyway
    # End of New Section
                    
    temp = GridRangeBearing((0, nerb1[0], nerb1[1], ''),
                            (0, c[0], c[1], '')
                            )

    flag=0
    if temp[0] < nerb1[2]:
        if abs(nerb1[3]-temp[1])<15 or abs(abs(nerb1[3]-temp[1])-360)<15:
            flag = 1

##    if temp[0] < nerb1[2] and abs(nerb1[3]-temp[1])<15 :
##        flag = 1
##    else:
##        flag=0

    return (c[0], c[1], flag)

#==============================================================================
#
#   function SortbyAttr
#
#       this function sorts a data list using the nth attribute as the sort key
#       the function uses the DSU, (dress sort, undress) technique
#       the sort can be reversed
def SortbyAttr(input,   # list, the name of the list to be sorted
               attr,    # int, the number of the attribute to use as the key (0 index)
               reverse  # int, 0 if reverse is false, 1 if true
               ):

    output = []
    # create a temporary list dressed up with the value for sorting
    tmplist = []
    tmplist = [(x[attr], x) for x in input]
    # sort the temporary list
    tmplist.sort()
    if reverse: tmplist.reverse()
    # recreate the original list, now sorted, by undressing the temporary list
    output = [tmplist[x][1] for x in range(len(tmplist))]
    tmplist = []
    
    return(output)

#==============================================================================
#
#   function PointSite2Route
#
#       this function currently works but needs to be upgraded to include
#           parallel offset
#           line reversal
def PointSite2Route(Wpt_List, Plan):
    '''
    Wpt_List - a waypoint list defined for the selected site
    
    Plan     - a plan selected for the selected site
    
    returns the route waypoints and the solar data at the time of calculation
    
    A function generate UTM and Geodetic Coordinates for a point site and uses the
    data in the site plan to generate all necessary targetting waypoints.
    
    The function handles multiview angles form the plan and generates an ordered list of waypoints
    '''
# XXX Override of database parameters
##    At some point in the development of this progran we must implement a means to
##    override some of the parameters in the site plan or configuration plan. All
##    contingencies cannot be accounted for, therefore the user may be required to
##    alter the approach on the 'fly'. For instance, the altitude or approach vector
##    might be changed.
##    
##    Some variables, not in a database, may be altered. For instance, in the
##    'BlockSite2Route' function, it assumes that if the camera is pitched forward
##    then it remains so for all lines. There is no database parameter for pitch
##    reversal for opposing tracks.
##    
##    Any parameter that is not preplanned in a database should be part of an
##    override schema. The necessity for a parallel offset or a line reversal
##    cannot typically be planned in advance.

    KeyNum = 0
    Nav_UTM={}
    Nav_LL={}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data

    FlightAltitude = Plan[0]
    Leadin = Plan[3]
    Leadout = Plan[4]
    SiteDiameter = Wpt_List[0][7]
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7]
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8+x])
    print NumViewAngles, ViewAngles
    TrackOffset=Plan[8+NumViewAngles]   # the angular offset of the track from the solar plane 
    RouteOffset=Plan[9+NumViewAngles]   # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate

    solar_track = math.fmod(Solar_Dat[1]+180, 360)
    track = solar_track + TrackOffset # adjusts for requested deviation from the solar plane
    
    # UTM navigation start waypoint 
    view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    offset = Offset(NavLeadin + Leadin + SiteDiameter/2 + view_angle_offset, track)    
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],              
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM line start waypoint    
    offset = Offset(Leadin + SiteDiameter/2 + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],          
                    Wpt_List[0][1] - offset[0],
                    Wpt_List[0][2] - offset[1],
                    Wpt_List[0][3])

    # sequencing for multiangle targeting                                            
    for x in range(0, NumViewAngles, 1):       
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[x]))
        
        
        # UTM start of site
        offset = Offset(SiteDiameter/2 + view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3])
        
        # UTM line centre waypoint
        offset = Offset(view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3]) 

        # UTM end of site
        offset = Offset(-SiteDiameter/2 + view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3])
                                                    
    # UTM line end waypoint
    offset = Offset(-(Leadout + SiteDiameter/2) + view_angle_offset, track)  
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],               
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM navigation end waypoint
    offset = Offset(-(NavLeadout + Leadout + SiteDiameter/2) + view_angle_offset, track)  
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],               
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])
    
    Nav_LL = utm2ll_route(Nav_UTM)  # create a lat/long route from the utm route
    
    return(Nav_UTM, Nav_LL, Solar_Dat)  # returns the line navigation coordinates in UTM space as a
                                #   dictionary and the solar data as a list

#==============================================================================
#
#   function LineSite2Route
#
#       this function currently works but needs to be upgraded to include
#           parallel offset
#           line reversal
#
def LineSite2Route(Wpt_List,    
                   Plan):
    
    Wpt_List.sort()
    KeyNum = 0
    Nav_UTM={}
    Nav_LL={}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data, not necessry to have in this case
                                         #  but nice to have updated information

    FlightAltitude = Plan[0]
    Leadin = Plan[3]
    Leadout = Plan[4]
    SiteDiameter = Wpt_List[0][7]       # not particularly useful for a line site.
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7]             # there should only be one, but it may be non zero
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8+x])
    print NumViewAngles, ViewAngles
    TrackOffset=Plan[8+NumViewAngles]   # the angular offset of the track from the solar plane, not used
                                        #   in the case of a line taret
    RouteOffset=Plan[9+NumViewAngles]   # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate

    SiteRangeBearing = GridRangeBearing(Wpt_List[0], Wpt_List[1])
    SiteLength = SiteRangeBearing[0]
    track = SiteRangeBearing[1]
    print 'SiteRangeBearing =', SiteRangeBearing
    
    if NumViewAngles==1:    # check that only one view angle has been specified for the target
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    else:
        view_angle_offset = 0   

    # UTM navigation start waypoint 
    offset = Offset(NavLeadin + Leadin + view_angle_offset, track)    
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],              
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM line start waypoint    
    offset = Offset(Leadin + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM site start waypoint    
    offset = Offset(view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM site end waypoint    
    offset = Offset(view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    # UTM line end waypoint    
    offset = Offset(-Leadout + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    # UTM navigation end waypoint 
    offset = Offset(-(NavLeadout + Leadout) + view_angle_offset, track)    
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],              
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    Nav_LL = utm2ll_route(Nav_UTM)  # create a lat/long route from the utm route
    
    return(Nav_UTM, Nav_LL, Solar_Dat)  # returns the line navigation coordinates in UTM space as a
                                #   dictionary and the solar data as a list

#==============================================================================
#
#   function BlockSite2Route
#
#       this function is in development
#           parallel offset
#           line reversal
#
def BlockSite2Route(Wpt_List,
                    Plan,
                    Config):
    '''
        I expect that this function will operate by determining a centre point
    for the block, creating a list of parallel offset lines on either side of
    the centre point at the grid deviation angle specified.
        Then the function will determine the intersection points of the offset
    lines with each of the boudary lines and select the appropriate intersections
    to determine the site start and site end waypoints of the line. Knowledge of
    the sensor swath is required for this. Once the 'unique' intersection points
    are determined for each offset line a list of utm linepoint pairs is created.
        A route is generated for each of the 'utm linepoint pairs' using the
    function 'LineSite2Route' and appending the result into the 'Nav_UTM' output.
    As each route is generated one could undertake the conversion of the utm
    route coordinates to geodetic coordinates and return the result along with the
    others as:
    
        return(Nav_UTM, Nav_LL, Solar_Dat)
    
        In fact, I think this is a better way to do it for the 'PointSite2Route'
    and 'LineSite2Route functions. It generates a nice object to pass around.
    
        Determine Point at COG
        Determine Range and Bearing to each vertex from centre
        Sort the vertices according to bearing relative to centre and create an
            ordered list of relative offsets
        Create s list of boundary lines
        Create the list of offsets from the centre point along the Northing
            through the centre point until they fall outside the maximum &
            minimum eastings
        Compute the intersections for each line 
        
    '''
    global debug
    
    WptKeyNum = 0
    LineKeyNum = 0
    Nav_UTM = {}
    Block_Nav_UTM = {}
    Nav_LL = {}
    Block_Nav_LL = {}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data, not necessry to have in this case
                                         #  but nice to have updated information
    Datum = Wpt_List[0][0]               # use the datum for the 1st waypoint as a nominal value
    UTMZone = Wpt_List[0][3]             # use the utmzone for the 1st waypoint as a nominal value
    GridDeviation = Wpt_List[0][5]      # use as a nominal value
    MagDeviation = Wpt_List[0][6]       # use as a nominal value
    SiteDiameter = Wpt_List[0][7]       # not particularly useful for a line site.
    
    FlightAltitude = Plan[0]
    Resolution = Plan[1]
    Gnd_Spd = Plan[2]
    Leadin = Plan[3]
    Leadout = Plan[4]
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7] # there should only be one, but it may be non zero
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8+x])
    # print NumViewAngles, ViewAngles
    TrackOffset = Plan[8+NumViewAngles] # the angular offset of the track from the solar plane, not used
                                        #   in the case of a line target
    casiMode = Plan[9+NumViewAngles]    # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate
    Overlap = Plan[10+NumViewAngles]
    RouteOffset = Plan[11+NumViewAngles]
    Block_Pattern = Plan[12+NumViewAngles]
    Comment = Plan[13+NumViewAngles]
    Tau = Plan[14+NumViewAngles]
    Bandset = Plan[15+NumViewAngles]
    Priority = Plan[16+NumViewAngles]
    Status = Plan[17+NumViewAngles]
               
    
    # compute the effective altitude due to camera pitch
    EffAlt = FlightAltitude / math.cos(math.radians(ViewAngles[0]))
                                         
    tFOV = math.radians(Config[7])  # total field of view in radians
    pFOV = math.radians(Config[8])  # port field of view in radians
    sFOV = math.radians(Config[9])  # starboard field of view in radians
    if debug ==1:
        print tFOV, pFOV, sFOV          # for debug
    
    port_swath = EffAlt * math.tan(pFOV)    # camera swath to the port(left) side
    stbd_swath = EffAlt * math.tan(sFOV)    # camera swath to the starboard(right) side.
    total_swath = port_swath + stbd_swath
    if debug ==1:
        print total_swath, port_swath, stbd_swath   # for debug

    port_swath_g = port_swath*(100-Overlap)/100   # swath less overlap
    stbd_swath_g = stbd_swath*(100-Overlap)/100
    total_swath_g = total_swath*(100-Overlap)/100
    if debug == 1:
        print total_swath_g, port_swath_g, stbd_swath_g   # for debug
    
    # create an array with the UTM coordinates
    # array of vertices as type float
    Vertices=N.zeros((len(Wpt_List),2),'f') 
    # populate the array with the vertex coordinates
    for x in range(0, len(Wpt_List),1):
                   Vertices[x][0] = Wpt_List[x][1]
                   Vertices[x][1] = Wpt_List[x][2]

    # determine the mean centre point
    Centre_Wpt = N.average(Vertices,0)

    # create an array copy for the Relative Vertices
    RelativeVertices = Vertices.copy()

    # populate the RelativeVertices array
    for x in range(0, len(Wpt_List),1):
                   RelativeVertices[x][0] = Vertices[x][0]-Centre_Wpt[0]
                   RelativeVertices[x][1] = Vertices[x][1]-Centre_Wpt[1]
    # determine the maximum values
    max_Easting = max(RelativeVertices[:,1])
    min_Easting = min(RelativeVertices[:,1])
    max_Northing = max(RelativeVertices[:,0])
    min_Northing = min(RelativeVertices[:,0])
    max_coordinate = max(max_Easting, max_Northing)
    min_coordinate = min(min_Easting, min_Northing)

    '''
    # increases the size by one row and copies data from the first
    #   row into the last. I'm not sure that this is necessary.
    RelativeVertices = N.resize(RelativeVertices, (len(Wpt_List)+1, 2))
    '''

    # create an array of range/bearing data from centre point to vertices
    CentreRangeBearing = Vertices.copy()

    # populate the RangeBearing array
    for x in range(0, len(Wpt_List),1):
        Temp = GridRangeBearing((0, Centre_Wpt[0], Centre_Wpt[1],''),
                                Wpt_List[x]
                                )
        CentreRangeBearing[x][0] = Temp[0]
        CentreRangeBearing[x][1] = Temp[1]
    

    # we may need some code here to sort the waypoints on the basis of
    #  the data in the CentreRangeBearing array. Not so for the test data.

    # concatenate two arrays
    temp = N.concatenate((RelativeVertices, CentreRangeBearing), 1)
    # convert the array to a list for sorting
    temp = temp.tolist()
    # sort the list
    # attribute 3 is the Bearing
    CentreRangeBearingList = SortbyAttr(temp, 3, 0)
    if debug==1:
        print 'Sorted Result\n', CentreRangeBearingList, '\n\n'
    if debug==1:
        print 'CentreRangeBearingList'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
    # create the VerticesRangeBearing List
    '''
    VerticesRangeBearing = list(CentreRangeBearingList)
    CentreRangeBearingList = tuple(CentreRangeBearingList)
    
    This was tried as an alternative to the above assignment
    but it made no difference
    '''
    VerticesRangeBearing = []
    for x in range(len(CentreRangeBearingList)):
        VerticesRangeBearing.append(CentreRangeBearingList[x])
    
    # update the range bearing data in VerticesRangeBearing
    if debug==1:
        print 'CentreRangeBearingList after creating VerticesRangeBearing'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
        print 'VerticesRangeBearing before updating the range & bearing'
        for x in range(len(VerticesRangeBearing)):
            print VerticesRangeBearing[x]
        print ''
    for x in range(len(VerticesRangeBearing)):
        y = int(math.fmod(x+1,len(VerticesRangeBearing)))
        temp = GridRangeBearing((0,
                                 VerticesRangeBearing[x][0],
                                 VerticesRangeBearing[x][1],
                                 ''
                                 ),
                                (0,
                                 VerticesRangeBearing[y][0],
                                 VerticesRangeBearing[y][1],
                                 ''
                                 )
                                )
        VerticesRangeBearing[x][2] = temp[0]
        VerticesRangeBearing[x][3] = temp[1]
        
    if debug==1:
        print 'CentreRangeBearingList'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
        print 'VerticesRangeBearing before expanding the target area'
        for x in range(len(VerticesRangeBearing)):
            print VerticesRangeBearing[x]
        print ''

    # expand the target area defined by the 'VerticesRangeBearing' data
    # to ensure complete coverage by the camera. The offset is based on
    # the intersection angle between the track and the bearing of the
    # boundary segment
    #
    # THIS WORKS - Don't change
    expandedRangeBearing = []
    '''
    Note: for the future, do not use a simple assigment to create a copy of an
            existing object. For example, doing this
                expandedRangeBearing = VerticesRangeBearing'
            caused a whole lot of trouble since the two variables are merely
            different names for the same object, so when an item is updated in
            one it is updated in the other.
            
            For safety, create a new list of items and append them to the new
            empty object as done below.
    '''
    for x in range(len(VerticesRangeBearing)):
        IntersectionAngle = VerticesRangeBearing[x][3] - TrackOffset
        # ensure that the intersection angle is from 0 to 90 degrees
        #   otherwise strange errors result
        # IntersectionAngle = math.fmod(IntersectionAngle + 180, 90)
        IntersectionAngle = math.fmod(IntersectionAngle + 180, 180)
        if IntersectionAngle > 90:
            IntersectionAngle = 180 - IntersectionAngle
        boundary_offset = abs(total_swath_g * math.cos(math.radians(IntersectionAngle)))
        BearingCCW90 = math.fmod(VerticesRangeBearing[x][3]+270,360)
        OffsetAngle = math.fmod(450-BearingCCW90, 360)
        dNorthing = math.sin(math.radians(OffsetAngle))*boundary_offset
        dEasting = math.cos(math.radians(OffsetAngle))*boundary_offset
        if debug == 1:
            print (VerticesRangeBearing[x][3],
                   IntersectionAngle,
                   boundary_offset,
                   OffsetAngle,
                   dNorthing,
                   dEasting)
            
        expandedRangeBearing.append([VerticesRangeBearing[x][0] + dNorthing, \
                                     VerticesRangeBearing[x][1] + dEasting, \
                                     VerticesRangeBearing[x][2], \
                                     VerticesRangeBearing[x][3]])
    if debug ==1:
        print 'expandedRangeBearing', len(expandedRangeBearing), 'Items\n', expandedRangeBearing, '\n\n'
    
    # at this point the coordinates in the expandedRangeBearing list
    # are not the vertices. The intersections for the NERB's must be
    # calculated and the range/bearings updated.
    # THIS WORKS - Don't change
    ExpandedVerticesRangeBearing = []
    # calculate the intersection points
    for x in range(len(expandedRangeBearing)):
        y = int(math.fmod(x+len(expandedRangeBearing)-1,len(expandedRangeBearing)))
        # y is the decrement by one in the range
        temp = NERBsIntersect(expandedRangeBearing[x],
                              expandedRangeBearing[y])
        ExpandedVerticesRangeBearing.append([temp[0], temp[1]])
    if debug ==1:
        print 'expandedRangeBearing', len(expandedRangeBearing), 'Items\n', expandedRangeBearing, '\n\n'
        print 'ExpandedVerticesRangeBearing\n', ExpandedVerticesRangeBearing, '\n\n'
    #calulate the range and bearing between the new intersection points
    for x in range(len(ExpandedVerticesRangeBearing)):
        y = int(math.fmod(x+1,len(ExpandedVerticesRangeBearing)))
        # y is the increment by one in the range
        if debug ==1:
            print ExpandedVerticesRangeBearing[x]
            print ExpandedVerticesRangeBearing[y]
        temp = GridRangeBearing((0,
                                ExpandedVerticesRangeBearing[x][0],
                                ExpandedVerticesRangeBearing[x][1],
                                ''),
                                (0,
                                ExpandedVerticesRangeBearing[y][0],
                                ExpandedVerticesRangeBearing[y][1],
                                '')                                 
                                )
        ExpandedVerticesRangeBearing[x].append(temp[0]) # append the range
        ExpandedVerticesRangeBearing[x].append(temp[1]) # append the bearing
        
    if debug==1:
        print 'ExpandedVerticesRangeBearing, Final Update before determining \
        line pattern spacing'
        for x in range(len(ExpandedVerticesRangeBearing)):
            print ExpandedVerticesRangeBearing[x]
        print ''

    # now that the vertices of the target block are appropriately defined it
    # is now possible to determine the flight line tracks once the
    # flight pattern and track spacing are determined       

    # This lengthy section of logic code is based on my spreadsheet model to 
    # create a list of centre track points along the E/W axis throught the
    #   relative centre point (0,0). One needs to know the necessary flight
    #   pattern from the plan and the camera swath for the camera mode and
    #   flight altitude. Also correct for the track offset as this affects
    #   line spacing.

    intercepts = []
    intercepts_Northing = []
    intercepts_Easting = []
    intercept = 0
    direction = 0   # a variable that specifies whether the line's track through
                    #   the intercept point will be at the value of the
                    #   TrackOffset given (relative to gridNorth) or in the
                    #   opposing direction.
                    #   direction = 1, means use the given track
                    #   direction = -1, means use the opposite track
                    
    if Block_Pattern == 0:  # this works, DON'T TOUCH
        # Pattern of OmniDirectional Parallel Lines
        x=0
        # determine the eastings for zero and positive offsets
        while (intercept < max_coordinate):
            intercept = x * total_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x+=1
        x=-1
        # determine the eastings for negative offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    
            intercept = x * total_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
        # Note that this will crash if TrackOffset=90
        
    elif Block_Pattern == 1:    # this works, DON'T TOUCH
        # Pattern of Alternating Parallel Lines
        x=0
        # determine the eastings for zero and positive even offsets
        while (intercept < max_coordinate):   
            intercept = x*port_swath_g + x*stbd_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x+=2           
        x=1
        # determine the eastings for positive odd offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept < max_coordinate):    # for odd values of x
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x+=2
        x=-1
        # determine the eastings for negative odd offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x-=2            
        x=-2
        # determine the eastings for negative even offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    # for even values of x
            intercept = (x*port_swath_g) + (x*stbd_swath_g)
            direction = 1
            intercepts.append([intercept, direction])
            x-=2
        intercepts.sort()
                        
    elif Block_Pattern == 2:
        # Centred Racetrack pattern of Parallel Lines
        # Since all of the intercept values are divided by the TrackOffset
        # correction factor and there will be a RouteOffset correction as well
        # which is the same in all cases, why not do it at the end. Apply it to the
        # easting_intercepts object at the end. For that matter call variable
        # intercepts and place in easting_intercepts or northing_intercepts as
        # required. Decide at the beginning, which one is required.
        x=0
        while intercept < max_coordinate:
            intercept = x*(port_swath_g + stbd_swath_g)
            direction = 1
            intercepts.append(intercept)
            x+=1
        x=-1
        while intercept > min_coordinate:
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
        
    else:
        # Centred Racetrack pattern of Parallel Lines Alternating
        #  Direction every R'th Line. Use the pattern number if>2
        x=0
        R=Block_Pattern-1    # the pattern reversal number, every 'R' lines
        while intercept < max_coordinate:
            isodd = int(math.modf(math.floor(x/R))[1]%2)            
            # isodd = 1 (if x/R is odd) = 0 (if x/R is even)
            intercept = (x-isodd)*port_swath_g + (x+isodd)*stbd_swath_g
            if not isodd:
                direction = 1
            else:
                direction = -1
            intercepts.append([intercept, direction])
            x+=1
        x=-1
        while intercept > min_coordinate:
            isodd = int(math.modf(math.floor(x/R))[1]%2)
            intercept = (x-isodd)*port_swath_g + (x+isodd)*stbd_swath_g
            if isodd:
                direction = -1
            else:
                direction = 1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
    #==========================================================================
    #   the pattern has now been generated. It is time to turn it into numbers
    #   along the N-S or E-W axes, which ever is most appropriate.
    #
    easting_spacing_factor = math.cos(math.radians(TrackOffset))
    northing_spacing_factor = math.sin(math.radians(TrackOffset))
    
    route_offset = RouteOffset*total_swath_g/100
    # Note: In future, watch out for implicit int. (RouteOffset/100) is an integer =0 because
    #       RouteOffset and 100 are integer and the result was rounded down to 0

    # a displacement of the spacing equivalent to a % of the total
    #   guaranteed swath. 
    for x in range(len(intercepts)):
        intercepts[x][0] += route_offset
    # a correction of the spacing for the grid deviation
    #   if the Track Offset is less than 45 degrees off the N-S grid line create a list
    #       of intercepts along the E-W grid line through the block centre point. Otherwise
    #       create a list of intercepts along the N-S grid line
    #
    if math.fmod(360+TrackOffset,180)<=45 or math.fmod(360+TrackOffset,180)>=135:
        spacing_factor = easting_spacing_factor
        for x in range(len(intercepts)):
            intercepts[x][0] /= spacing_factor
            if intercepts[x][1] > 0:
                intercepts[x][1] = TrackOffset
            else:
                intercepts[x][1] = TrackOffset+180
            intercepts[x].insert(0,0.0) #   insert '0.0' as an Northing in the list
            intercepts[x].insert(2,100.0) # insert '100.0' as a dummy Range value in the list
    else:
        spacing_factor = northing_spacing_factor
        for x in range(len(intercepts)):
            intercepts[x][0] /= spacing_factor
            if intercepts[x][1] > 0:
                intercepts[x][1] = TrackOffset
            else:
                intercepts[x][1] = TrackOffset+180
            intercepts[x].insert(1,0.0) #   insert '0.0' as an Easting in the list
            intercepts[x].insert(2,100.0) # insert '100.0' as a dummy Range value in the list

    # now that the factoring has been completed the elements in the intercepts
    #   object should be immuteable, so change each top-level list item to a tuple
    for x in range(len(intercepts)): intercepts[x]=tuple(intercepts[x])

    # now use the RelativeVertices Data and expand the boundary sufficiently to
    # ensure complete coverage at the terminus of every line.
    # use the pattern spacing list 'intercepts' and the expanded boudary values
    #   in ExpandedVerticesRangeBearing to determine the intersections of the
    #   pattern lines with the boundary.
    # use the function NERBsIntersect to find the intersection points of each
    #   pattern line with all of the boundary segments. The function returns a
    #   flag that indicates whether the intersecion point is within the confines
    #   of the boudary segment. Save only the intersecion points that are within
    #   the segments
    #
    #   This WORKS Do not revise
    #
    # this currently does not retain information about the required track of the
    #   route. The order of the points in the should reflect the intended track, the
    #   first point being the start, and the second point being the end.
    TargetBlockIntercepts = []  # the storage location for the intercepts
    for x in range(len(intercepts)):
        LineIntersections = [] # a temporary container for intersectiion points
        for y in range(len(ExpandedVerticesRangeBearing)):
            temp = NERBsIntersect(ExpandedVerticesRangeBearing[y],
                                  intercepts[x]
                                  )
            if temp[2]==1:   # is the intercept flag '1'
                LineIntersections.append([Datum, temp[0], temp[1], UTMZone])
        # check the orientation
        # note, that there should only be two tuples in the LineIntersections object
        if len(LineIntersections)==2:   # a test
            #if LineIntersections != []:
            LineIntersections.append(math.fmod(360+intercepts[x][3],360))
            # append the bearing of the planned track
            temp = GridRangeBearing(LineIntersections[0],
                                    LineIntersections[1]
                                    )
            if abs(LineIntersections[2]-temp[1])>5 :
                # checks the Bearing agrees with the order of the points,
                # otherwise we need to swap the points so the 1st pt is the start
                # and the 2nd pt is the end and it agrees with the bearing.
                # need to swap, done by direct assignment
                LineIntersections[0], LineIntersections[1] = \
                                      LineIntersections[1], LineIntersections[0]
            TargetBlockIntercepts.append(LineIntersections)
    
    if debug == 1:
        print 'TargetBlockIntercepts'
        for x in range(len(TargetBlockIntercepts)):
            print x, TargetBlockIntercepts[x]
    
    # now that the lines have been determined by intercepts with the Expanded Block
    #   area, the waypoints for the routes can be generated using the LineSite2Route
    #   function. In calling this function the Waypoint entry will be constructed from the
    #   'TargetBlocksIntercepts' object and the plan will be reconstructed rather than
    #   read from the database.
    #
    #   This section also adds the centre offset that was removed from the coordinate
    #   values of the vertices of the target area. The numbers will correspond to real
    #   UTM space.

    if NumViewAngles==1:    # check that only one view angle has been specified for the target
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    else:
        view_angle_offset = 0

    for x in range(len(TargetBlockIntercepts)):
        Nav_UTM = {}
        Nav_LL = {}
        LineKeyNum = x
        KeyNum = 0
        
        # UTM navigation start waypoint
        offset = Offset(NavLeadin + Leadin + view_angle_offset, TargetBlockIntercepts[x][2])
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],              
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM line start waypoint    
        offset = Offset(Leadin + view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM site start waypoint    
        offset = Offset(view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM site end waypoint    
        offset = Offset(view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])

        # UTM line end waypoint    
        offset = Offset(-Leadout + view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])

        # UTM navigation end waypoint 
        offset = Offset(-(NavLeadout + Leadout) + view_angle_offset, TargetBlockIntercepts[x][2])    
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],              
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])
        Block_Nav_UTM[x] = Nav_UTM
        Nav_LL = utm2ll_route(Nav_UTM)
        Block_Nav_LL[x] = Nav_LL

    if debug == 1:
        #   another section of printouts for debugging
        #   for checking the parameters that are passed into the function
        #
        print 'route_offset(m)=', route_offset, 'track_offset_factor=',spacing_factor
        print 'FlightAltitude',FlightAltitude 
        print 'Leadin',Leadin, 'metres'
        print 'Leadout',Leadout, 'metres'
        print 'SiteDiameter',SiteDiameter, 'metres'     
        print 'NavLeadin',NavLeadin, 'metres'
        print 'NavLeadout',NavLeadout, 'metres'
        print 'NumViewAngles',NumViewAngles
        print 'ViewAngles',ViewAngles, 'degrees'
        print 'TrackOffset',TrackOffset, 'degrees'
        print 'casiMode',casiMode
        print 'GridDeviation',GridDeviation, 'degrees'
        print 'MagDeviation',MagDeviation, 'degrees'
        print 'Overlap',Overlap, 'percent'
        print 'RouteOffset',RouteOffset, 'percent'
        print 'Block_Pattern',Block_Pattern
        print 'Comment',Comment
        print 'Tau',Tau
        print 'Bandset',Bandset
        print 'Priority',Priority
        print 'Status',Status
        print 'Vertices\n', Vertices, Centre_Wpt
        print 'RelativeVertices\n', RelativeVertices
        print  '\tE_Min =', min_Easting, 'E_Max =', max_Easting
        print  '\tN_Min =', min_Northing, 'N_Max =', max_Northing
        print 'CentreRangeBearing\n', CentreRangeBearing
        print intercepts
        #   end of section for debugging

# XXX Revise the output of the vertices.
##    Output of the vertices is required for plotting of the target area on a
##    map display at some point. Correct the vertices so they are in real UTM
##    space, not in relative UTM space.
    
    return(Block_Nav_UTM, Block_Nav_LL, Solar_Dat,
           VerticesRangeBearing,
           ExpandedVerticesRangeBearing,
           Centre_Wpt)                              # added for test

    
#==============================================================================
#
#   function utm2ll_Route
#
#       this function currently works only if the dictionary passed to 'utm_route'
#               contains a utm waypoint value for each key.
#       for a block site it is expected that the muliple routes will be dictionaries nested within
#           the dictionary variable passed to this function.
#       the function will need to handle this situation.
#
def utm2ll_route(utm_route):

    route_LL = {}
    for key in utm_route.keys():
        route_LL[key] = geodesy.UTM2LL(utm_route[key][0],
                                       utm_route[key][1],
                                       utm_route[key][2],
                                       utm_route[key][3]
                                       )

    return(route_LL)    # returns a dictionary of the latitude/longitude coordinates
    
#===============================================================================
#   test stuff
#
if __name__ == "__main__":

    import WaypointTarget_IO as wpio

    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\test_sites_1.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    site_utm_db = wpio.generic2site_db(temp_db) # the target database
                  
    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\test_plan_1.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    plan_utm_db = wpio.generic2plan_db(temp_db) # the planning database
    
    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\casi302_config.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    sensor_db = wpio.generic2sensor_db(temp_db)   # the sensor configuration database
    
    
    #=========================================================================================
    #   test of a single point site
    #
    
    site = 'Sb-1'
    print '\n', site_utm_db[site], plan_utm_db[site][0],'\n'
       
    Result = PointSite2Route(site_utm_db[site], plan_utm_db[site][0])
    utm_route = Result[0]               # get the utm route from Result
    ll_route = Result[1]
    solar_dat = Result[2]               # get the solar data from Result

    # the 6 lines above show how to obtain a route for a point target, code below
    # is window dressing to display the results
    #
    print 'SiteID', site
    print 'Solar Data', solar_dat, '\n'
    print 'Routing Waypoints as UTM Coordinates\n'
    key = utm_route.keys()      # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()                  # sort the integers
    for x in (key):    
        print '\t', x, utm_route[str(x)] # integer converted to string for key

    print '\nRouting Waypoints as Latitude / Longitude Coordinates\n'
    key = ll_route.keys()       # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()
    # sort the integers
    for x in (key):
        print '\t', x, ll_route[str(x)]  # integer converted to string for key

    
    #=========================================================================================
    #   test of a two point site (a predefined line)
    #
    
    site='Pj-6'
    print '\n', site_utm_db[site], plan_utm_db[site][0],'\n'

    Result = LineSite2Route(site_utm_db[site], plan_utm_db[site][0])
    utm_route = Result[0]
    ll_route = Result[1]
    solar_dat = Result[2]
    
    print 'SiteID', site
    print 'Solar Data', solar_dat, '\n'
    print 'Routing Waypoints as UTM Coordinates\n'
    key = utm_route.keys()      # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()                  # sort the integers
    for x in (key):    
        print '\t', x, utm_route[str(x)] # integer converted to string for key

    print '\nRouting Waypoints as Latitude / Longitude Coordinates\n'
    key = ll_route.keys()       # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()
    # sort the integers
    for x in (key):
        print '\t', x, ll_route[str(x)]  # integer converted to string for key
    
    
    #=========================================================================================
    #   test of a block site
    #

    site = 'Pj-76'      # in a real program this value will be selected from a list
    config = 'mmeris'   # in a real program this value will be selected from a list
    # this is a spatial config read from the list of multiple plans (if any) for the site
    config = plan_utm_db[site][0][-3] # if the configuration name is 3rd from the end
    
    print 'Start of MAIN TEST Output for a Block Site\n'    
    print '\nSite Selected\n', site_utm_db[site], '\n'
    print '\nPlan Selected\n', plan_utm_db[site][0], '\n'
    print '\nSensor Configuration\n', sensor_db[config][0], '\n'
    
    debug = 0   # turn on debugging for the block site section
    Result = BlockSite2Route(site_utm_db[site],
                             plan_utm_db[site][0],
                             sensor_db[config][0])
    utm_route = Result[0]
    ll_route = Result[1]
    solar_dat = Result[2]
    vertices = Result[3]
    expanded_vertices = Result[4]
    centre = Result[5]
    
    # print 'UTM Routing Data\n', utm_route, '\n'
    # print 'Lat/Long Routing Data\n', ll_route, '\n'
    print 'Solar Ephemerus Data\n', solar_dat, '\n'
    # print '\nEND OF MAIN TEST OUTPUT for a Block Site\n'
    
    # Output of the Vertices and Routing data in a sensible fashion so the results can be copied and
    # checked as an ordered list of data
    #
    print 'Vertices'
    for x in range(len(vertices)):
        print x, vertices[x]
    print 0, vertices[0]
    print '\nExpanded_Vertices'
    for x in range(len(expanded_vertices)):
        print x, expanded_vertices[x]
    print 0, expanded_vertices[0]
    print '\nCentre_Waypoint'
    print '0', centre, '\n'
    
    key = utm_route.keys()          # get the keys as strings
    key.sort()                      # sort the integers
    print 'Block_Nav_UTM'
    for x in range(len(key)):
        key1 = utm_route[key[x]].keys()
        key1.sort()
        for y in range(len(key1)):
            print key[x], key1[y], utm_route[key[x]][key1[y]]
        print ''

    key = ll_route.keys()          # get the keys as strings
    key.sort()                      # sort the integers
    print 'Block_Nav_LL'
    for x in range(len(key)):
        key1 = ll_route[key[x]].keys()
        key1.sort()
        for y in range(len(key1)):
            print key[x], key1[y], ll_route[key[x]][key1[y]]
        print ''
    

=======
#        
# Module to Generate Routing Waypoints based on the 'Site' selected 
#   from a site database and a plan selected from a planning database 
#
#  RouteGenerator Module - import as <RG> to abbreviate
#

import math
import Ephemerus.Ephemerus as Ephemerus
import Geodesy.geodesy as geodesy
import time
import Numeric as N
import LinearAlgebra as LA

debug = 0

#==============================================================================
#
#   function SiteType
#
def SiteType(WPt_List):    # a list of waypoints defined for the selected site
    '''
    A function to determine the type of target by assessing the number of
    waypoints in Wpt_List. Returns an integer 'sitetype'
    
    1 waypoint indicates a point target, SiteType = 0
        
    2 waypoints indicate a line target, SiteType = 1
    
    2 or more waypoints indicate an extended target area, SiteType = 2
    '''
    if len(WPt_List)==2:
        sitetype=1
    elif len(WPt_List)>2:
        sitetype=2
    else:
        sitetype=0

    return(sitetype)

#==============================================================================
#
#   function UTM2Solar
#
# XXX Update UTM2Solar to accept an input time to override the current time
#
def UTM2Solar(Input_Pt):    # a function to determine the current solar ephemerus
                            # for the selected Waypoint
    
    lat_long = geodesy.UTM2LL(Input_Pt[0],    # datum
                              Input_Pt[1],    # northing
                              Input_Pt[2],    # easting
                              Input_Pt[3]     # UTMZone
                              )

    # the current gmt based on the computers system time and timezone
    gmt_current = time.gmtime()

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
    return(solar_dat)

#==============================================================================
#
#   function GridRangeBearing
#
#   function that returns the range and grid bearing between two points
#       maybe this should made general by inputting utm tuples

def GridRangeBearing(from_wpt,  # list, utm coordinates for the waypoint flying from
                     to_wpt     # list, utm coordinates for the waypoint flying to
                     ):
    
    n2=to_wpt[1]    # to northing
    e2=to_wpt[2]    # to easting
    n1=from_wpt[1]  # from northing
    e1=from_wpt[2]  # from easting
    
    # slopeangle is the angle defined by two points accounting for the
    #   order if the points as the direction

    try:
        theta = math.degrees(math.atan((n2-n1)/(e2-e1)))
    except ZeroDivisionError:
        if n2 > n1:
            theta = 90.0
        elif n2 < n1:
            theta = 270.0
        else:
            print 'Coincident Points entered in function GridRangeBearing'
            Range = 0
            Bearing = 0
            return(Range, Bearing)
        slopeangle = theta
        
    if e2>e1:  
        if n2<>n1: slopeangle=theta 
        else: slopeangle=0.0
    if e2<e1:
        if n2<>n1: slopeangle=180.0+theta
        else: slopeangle=180.0
    # note the condition of e2=e1 has been handled in the try/exception
    #   above
            
    Bearing = math.fmod(450.0-slopeangle, 360.0)
    Range = math.sqrt((n2-n1)*(n2-n1)+(e2-e1)*(e2-e1))

    return(Range, Bearing)
#==============================================================================
#
#   function Offset
#
#   a simple function to return the utm offset if the distance(range)
#       and bearing between two points is known
#

def Offset(Range,
           Bearing
           ):
    Northing = math.sin(math.radians(math.fmod(450-Bearing, 360)))*Range
    Easting = math.cos(math.radians(math.fmod(450-Bearing, 360)))*Range        
    return(Northing, Easting)

#==============================================================================
#
#   function NERBsIntersect
#
#       a function to compute the intersection point of two NERB's 
#          ie. Lines defined as (Northing, Easting, Range, Bearing)
#

def NERBsIntersect(nerb1,
                   nerb2
                   ):
    '''
    nerb1 - type list, a line defined by a northing, easting, range & bearing
    
    nerb2 - type list, a line defined by a northing, easting, range & bearing

    returns a northing, easting and flag

    flag indicates that the intersection point lies within the range & bearing
    of nerb1
    '''
    theta1 = math.fmod(450-nerb1[3], 360)   # convert bearing to math angle
    theta2 = math.fmod(450-nerb2[3], 360)   # yes, it's the same formula for
                                            #   math to bearing angle
##    if theta1 == 90 or theta1 == 270:
##        a1 = 0
##        b1 = -1
##        c1 = nerb1[1]
##    else:
##        a1 = 1
##        b1 = -math.tan(math.radians(theta1))
##        c1 = nerb1[0]-nerb1[1]*math.tan(math.radians(theta1))
##
##    if theta2 == 90 or theta2 == 270:
##        a2 = 0
##        b2 = -1
##        c2 = nerb2[1]
##    else:
##        a2 = 1
##        b2 = -math.tan(math.radians(theta2))
##        c2 = nerb2[0]-nerb2[1]*math.tan(math.radians(theta2))
##
##    a = N.array([(a1,b1),(a2,b2)])
##    b = N.array([(c1),(c2)])
##    try:
##        c = LA.solve_linear_equations(a,b)
##    except LA.LinAlgError:
##        # print'Singular matrix'
##        return (0,0,0)  # return zero's, the flag is zero so the
##                        #   data is ignored anyway
    # New Section
    if theta1 == 90 or theta1 == 270:
        c = [nerb2[0]-math.tan(math.radians(theta2))*(nerb2[1]-nerb1[1]), nerb1[1]]
    elif theta2 == 90 or theta2 == 270:
        c = [nerb1[0]-math.tan(math.radians(theta1))*(nerb1[1]-nerb2[1]), nerb2[1]]
    else:
        a1 = 1
        b1 = -math.tan(math.radians(theta1))
        c1 = nerb1[0]-nerb1[1]*math.tan(math.radians(theta1))
        a2 = 1
        b2 = -math.tan(math.radians(theta2))
        c2 = nerb2[0]-nerb2[1]*math.tan(math.radians(theta2))

        a = N.array([(a1,b1),(a2,b2)])
        b = N.array([(c1),(c2)])
        try:
            c = LA.solve_linear_equations(a,b)
        except LA.LinAlgError:
            # print'Singular matrix'
            return (0,0,0)  # return zero's, the flag is zero so the
                            #   result is ignored anyway
    # End of New Section
                    
    temp = GridRangeBearing((0, nerb1[0], nerb1[1], ''),
                            (0, c[0], c[1], '')
                            )

    flag=0
    if temp[0] < nerb1[2]:
        if abs(nerb1[3]-temp[1])<15 or abs(abs(nerb1[3]-temp[1])-360)<15:
            flag = 1

##    if temp[0] < nerb1[2] and abs(nerb1[3]-temp[1])<15 :
##        flag = 1
##    else:
##        flag=0

    return (c[0], c[1], flag)

#==============================================================================
#
#   function SortbyAttr
#
#       this function sorts a data list using the nth attribute as the sort key
#       the function uses the DSU, (dress sort, undress) technique
#       the sort can be reversed
def SortbyAttr(input,   # list, the name of the list to be sorted
               attr,    # int, the number of the attribute to use as the key (0 index)
               reverse  # int, 0 if reverse is false, 1 if true
               ):

    output = []
    # create a temporary list dressed up with the value for sorting
    tmplist = []
    tmplist = [(x[attr], x) for x in input]
    # sort the temporary list
    tmplist.sort()
    if reverse: tmplist.reverse()
    # recreate the original list, now sorted, by undressing the temporary list
    output = [tmplist[x][1] for x in range(len(tmplist))]
    tmplist = []
    
    return(output)

#==============================================================================
#
#   function PointSite2Route
#
#       this function currently works but needs to be upgraded to include
#           parallel offset
#           line reversal
def PointSite2Route(Wpt_List, Plan):
    '''
    Wpt_List - a waypoint list defined for the selected site
    
    Plan     - a plan selected for the selected site
    
    returns the route waypoints and the solar data at the time of calculation
    
    A function generate UTM and Geodetic Coordinates for a point site and uses the
    data in the site plan to generate all necessary targetting waypoints.
    
    The function handles multiview angles form the plan and generates an ordered list of waypoints
    '''
# XXX Override of database parameters
##    At some point in the development of this progran we must implement a means to
##    override some of the parameters in the site plan or configuration plan. All
##    contingencies cannot be accounted for, therefore the user may be required to
##    alter the approach on the 'fly'. For instance, the altitude or approach vector
##    might be changed.
##    
##    Some variables, not in a database, may be altered. For instance, in the
##    'BlockSite2Route' function, it assumes that if the camera is pitched forward
##    then it remains so for all lines. There is no database parameter for pitch
##    reversal for opposing tracks.
##    
##    Any parameter that is not preplanned in a database should be part of an
##    override schema. The necessity for a parallel offset or a line reversal
##    cannot typically be planned in advance.

    KeyNum = 0
    Nav_UTM={}
    Nav_LL={}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data

    FlightAltitude = Plan[0]
    Leadin = Plan[3]
    Leadout = Plan[4]
    SiteDiameter = Wpt_List[0][7]
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7]
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8][x])
    print NumViewAngles, ViewAngles
    TrackOffset=Plan[8+NumViewAngles]   # the angular offset of the track from the solar plane 
    RouteOffset=Plan[9+NumViewAngles]   # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate

    solar_track = math.fmod(Solar_Dat[1]+180, 360)
    track = solar_track + TrackOffset # adjusts for requested deviation from the solar plane
    
    # UTM navigation start waypoint
    view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    offset = Offset(NavLeadin + Leadin + SiteDiameter/2 + view_angle_offset, track)    
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],              
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM line start waypoint    
    offset = Offset(Leadin + SiteDiameter/2 + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],          
                    Wpt_List[0][1] - offset[0],
                    Wpt_List[0][2] - offset[1],
                    Wpt_List[0][3])

    # sequencing for multiangle targeting                                            
    for x in range(0, NumViewAngles, 1):       
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[x]))
        
        
        # UTM start of site
        offset = Offset(SiteDiameter/2 + view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3])
        
        # UTM line centre waypoint
        offset = Offset(view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3]) 

        # UTM end of site
        offset = Offset(-SiteDiameter/2 + view_angle_offset, track)
        KeyNum = KeyNum+1
        Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],             
                                Wpt_List[0][1] - offset[0],
                                Wpt_List[0][2] - offset[1],
                                Wpt_List[0][3])
                                                    
    # UTM line end waypoint
    offset = Offset(-(Leadout + SiteDiameter/2) + view_angle_offset, track)  
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],               
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM navigation end waypoint
    offset = Offset(-(NavLeadout + Leadout + SiteDiameter/2) + view_angle_offset, track)  
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],               
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])
    
    Nav_LL = utm2ll_route(Nav_UTM)  # create a lat/long route from the utm route
    
    return(Nav_UTM, Nav_LL, Solar_Dat)  # returns the line navigation coordinates in UTM space as a
                                #   dictionary and the solar data as a list

#==============================================================================
#
#   function LineSite2Route
#
#       this function currently works but needs to be upgraded to include
#           parallel offset
#           line reversal
#
def LineSite2Route(Wpt_List,    
                   Plan):
    
    Wpt_List.sort()
    KeyNum = 0
    Nav_UTM={}
    Nav_LL={}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data, not necessry to have in this case
                                         #  but nice to have updated information

    FlightAltitude = Plan[0]
    Leadin = Plan[3]
    Leadout = Plan[4]
    SiteDiameter = Wpt_List[0][7]       # not particularly useful for a line site.
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7]             # there should only be one, but it may be non zero
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8][x])
    print NumViewAngles, ViewAngles
    TrackOffset=Plan[8+NumViewAngles]   # the angular offset of the track from the solar plane, not used
                                        #   in the case of a line taret
    RouteOffset=Plan[9+NumViewAngles]   # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate

    SiteRangeBearing = GridRangeBearing(Wpt_List[0], Wpt_List[1])
    SiteLength = SiteRangeBearing[0]
    track = SiteRangeBearing[1]
    print 'SiteRangeBearing =', SiteRangeBearing
    
    if NumViewAngles==1:    # check that only one view angle has been specified for the target
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    else:
        view_angle_offset = 0   

    # UTM navigation start waypoint 
    offset = Offset(NavLeadin + Leadin + view_angle_offset, track)    
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],              
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM line start waypoint    
    offset = Offset(Leadin + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM site start waypoint    
    offset = Offset(view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[0][0],
                            Wpt_List[0][1] - offset[0],
                            Wpt_List[0][2] - offset[1],
                            Wpt_List[0][3])

    # UTM site end waypoint    
    offset = Offset(view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    # UTM line end waypoint    
    offset = Offset(-Leadout + view_angle_offset, track)
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    # UTM navigation end waypoint 
    offset = Offset(-(NavLeadout + Leadout) + view_angle_offset, track)    
    KeyNum = KeyNum+1
    Nav_UTM[str(KeyNum)] = (Wpt_List[1][0],              
                            Wpt_List[1][1] - offset[0],
                            Wpt_List[1][2] - offset[1],
                            Wpt_List[1][3])

    Nav_LL = utm2ll_route(Nav_UTM)  # create a lat/long route from the utm route
    
    return(Nav_UTM, Nav_LL, Solar_Dat)  # returns the line navigation coordinates in UTM space as a
                                #   dictionary and the solar data as a list

#==============================================================================
#
#   function BlockSite2Route
#
#       this function is in development
#           parallel offset
#           line reversal
#
def BlockSite2Route(Wpt_List,
                    Plan,
                    Config):
    '''
        I expect that this function will operate by determining a centre point
    for the block, creating a list of parallel offset lines on either side of
    the centre point at the grid deviation angle specified.
        Then the function will determine the intersection points of the offset
    lines with each of the boudary lines and select the appropriate intersections
    to determine the site start and site end waypoints of the line. Knowledge of
    the sensor swath is required for this. Once the 'unique' intersection points
    are determined for each offset line a list of utm linepoint pairs is created.
        A route is generated for each of the 'utm linepoint pairs' using the
    function 'LineSite2Route' and appending the result into the 'Nav_UTM' output.
    As each route is generated one could undertake the conversion of the utm
    route coordinates to geodetic coordinates and return the result along with the
    others as:
    
        return(Nav_UTM, Nav_LL, Solar_Dat)
    
        In fact, I think this is a better way to do it for the 'PointSite2Route'
    and 'LineSite2Route functions. It generates a nice object to pass around.
    
        Determine Point at COG
        Determine Range and Bearing to each vertex from centre
        Sort the vertices according to bearing relative to centre and create an
            ordered list of relative offsets
        Create s list of boundary lines
        Create the list of offsets from the centre point along the Northing
            through the centre point until they fall outside the maximum &
            minimum eastings
        Compute the intersections for each line 
        
    '''
    global debug
    
    WptKeyNum = 0
    LineKeyNum = 0
    Nav_UTM = {}
    Block_Nav_UTM = {}
    Nav_LL = {}
    Block_Nav_LL = {}
    Solar_Dat = UTM2Solar(Wpt_List[0])   # get the solar ephemerus data, not necessry to have in this case
                                         #  but nice to have updated information
    Datum = Wpt_List[0][0]               # use the datum for the 1st waypoint as a nominal value
    UTMZone = Wpt_List[0][3]             # use the utmzone for the 1st waypoint as a nominal value
    GridDeviation = Wpt_List[0][5]      # use as a nominal value
    MagDeviation = Wpt_List[0][6]       # use as a nominal value
    SiteDiameter = Wpt_List[0][7]       # not particularly useful for a line site.
    
    FlightAltitude = Plan[0]
    Resolution = Plan[1]
    Gnd_Spd = Plan[2]
    Leadin = Plan[3]
    Leadout = Plan[4]
    NavLeadin = Plan[5]
    NavLeadout = Plan[6]
    NumViewAngles = Plan[7] # there should only be one, but it may be non zero
    ViewAngles = []
    for x in range(0,Plan[7],1):        # pitch angles for the camera
        ViewAngles.append(Plan[8][x])
    # print NumViewAngles, ViewAngles
    TrackOffset = Plan[8+NumViewAngles] # the angular offset of the track from the solar plane, not used
                                        #   in the case of a line target
    casiMode = Plan[9+NumViewAngles]    # the percent parallel offset of the track from the centre line
                                        # needs knowledge of the camera swath in order to estimate
    Overlap = Plan[10+NumViewAngles]
    RouteOffset = Plan[11+NumViewAngles]
    Block_Pattern = Plan[12+NumViewAngles]
    Comment = Plan[13+NumViewAngles]
    Tau = Plan[14+NumViewAngles]
    Bandset = Plan[15+NumViewAngles]
    Priority = Plan[16+NumViewAngles]
    Status = Plan[17+NumViewAngles]
               
    
    # compute the effective altitude due to camera pitch
    EffAlt = FlightAltitude / math.cos(math.radians(ViewAngles[0]))
                                         
    tFOV = math.radians(Config[7])  # total field of view in radians
    pFOV = math.radians(Config[8])  # port field of view in radians
    sFOV = math.radians(Config[9])  # starboard field of view in radians
    if debug ==1:
        print tFOV, pFOV, sFOV          # for debug
    
    port_swath = EffAlt * math.tan(pFOV)    # camera swath to the port(left) side
    stbd_swath = EffAlt * math.tan(sFOV)    # camera swath to the starboard(right) side.
    total_swath = port_swath + stbd_swath
    if debug ==1:
        print total_swath, port_swath, stbd_swath   # for debug

    port_swath_g = port_swath*(100-Overlap)/100   # swath less overlap
    stbd_swath_g = stbd_swath*(100-Overlap)/100
    total_swath_g = total_swath*(100-Overlap)/100
    if debug == 1:
        print total_swath_g, port_swath_g, stbd_swath_g   # for debug
    
    # create an array with the UTM coordinates
    # array of vertices as type float
    Vertices=N.zeros((len(Wpt_List),2),'f') 
    # populate the array with the vertex coordinates
    for x in range(0, len(Wpt_List),1):
                   Vertices[x][0] = Wpt_List[x][1]
                   Vertices[x][1] = Wpt_List[x][2]

    # determine the mean centre point
    Centre_Wpt = N.average(Vertices,0)

    # create an array copy for the Relative Vertices
    RelativeVertices = Vertices.copy()

    # populate the RelativeVertices array
    for x in range(0, len(Wpt_List),1):
                   RelativeVertices[x][0] = Vertices[x][0]-Centre_Wpt[0]
                   RelativeVertices[x][1] = Vertices[x][1]-Centre_Wpt[1]
    # determine the maximum values
    max_Easting = max(RelativeVertices[:,1])
    min_Easting = min(RelativeVertices[:,1])
    max_Northing = max(RelativeVertices[:,0])
    min_Northing = min(RelativeVertices[:,0])
    max_coordinate = max(max_Easting, max_Northing)
    min_coordinate = min(min_Easting, min_Northing)

    '''
    # increases the size by one row and copies data from the first
    #   row into the last. I'm not sure that this is necessary.
    RelativeVertices = N.resize(RelativeVertices, (len(Wpt_List)+1, 2))
    '''

    # create an array of range/bearing data from centre point to vertices
    CentreRangeBearing = Vertices.copy()

    # populate the RangeBearing array
    for x in range(0, len(Wpt_List),1):
        Temp = GridRangeBearing((0, Centre_Wpt[0], Centre_Wpt[1],''),
                                Wpt_List[x]
                                )
        CentreRangeBearing[x][0] = Temp[0]
        CentreRangeBearing[x][1] = Temp[1]
    

    # we may need some code here to sort the waypoints on the basis of
    #  the data in the CentreRangeBearing array. Not so for the test data.

    # concatenate two arrays
    temp = N.concatenate((RelativeVertices, CentreRangeBearing), 1)
    # convert the array to a list for sorting
    temp = temp.tolist()
    # sort the list
    # attribute 3 is the Bearing
    CentreRangeBearingList = SortbyAttr(temp, 3, 0)
    if debug==1:
        print 'Sorted Result\n', CentreRangeBearingList, '\n\n'
    if debug==1:
        print 'CentreRangeBearingList'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
    # create the VerticesRangeBearing List
    '''
    VerticesRangeBearing = list(CentreRangeBearingList)
    CentreRangeBearingList = tuple(CentreRangeBearingList)
    
    This was tried as an alternative to the above assignment
    but it made no difference
    '''
    VerticesRangeBearing = []
    for x in range(len(CentreRangeBearingList)):
        VerticesRangeBearing.append(CentreRangeBearingList[x])
    
    # update the range bearing data in VerticesRangeBearing
    if debug==1:
        print 'CentreRangeBearingList after creating VerticesRangeBearing'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
        print 'VerticesRangeBearing before updating the range & bearing'
        for x in range(len(VerticesRangeBearing)):
            print VerticesRangeBearing[x]
        print ''
    for x in range(len(VerticesRangeBearing)):
        y = int(math.fmod(x+1,len(VerticesRangeBearing)))
        temp = GridRangeBearing((0,
                                 VerticesRangeBearing[x][0],
                                 VerticesRangeBearing[x][1],
                                 ''
                                 ),
                                (0,
                                 VerticesRangeBearing[y][0],
                                 VerticesRangeBearing[y][1],
                                 ''
                                 )
                                )
        VerticesRangeBearing[x][2] = temp[0]
        VerticesRangeBearing[x][3] = temp[1]
        
    if debug==1:
        print 'CentreRangeBearingList'
        for x in range(len(CentreRangeBearingList)):
            print CentreRangeBearingList[x]
        print ''
        print 'VerticesRangeBearing before expanding the target area'
        for x in range(len(VerticesRangeBearing)):
            print VerticesRangeBearing[x]
        print ''

    # expand the target area defined by the 'VerticesRangeBearing' data
    # to ensure complete coverage by the camera. The offset is based on
    # the intersection angle between the track and the bearing of the
    # boundary segment
    #
    # THIS WORKS - Don't change
    expandedRangeBearing = []
    '''
    Note: for the future, do not use a simple assigment to create a copy of an
            existing object. For example, doing this
                expandedRangeBearing = VerticesRangeBearing'
            caused a whole lot of trouble since the two variables are merely
            different names for the same object, so when an item is updated in
            one it is updated in the other.
            
            For safety, create a new list of items and append them to the new
            empty object as done below.
    '''
    for x in range(len(VerticesRangeBearing)):
        IntersectionAngle = VerticesRangeBearing[x][3] - TrackOffset
        # ensure that the intersection angle is from 0 to 90 degrees
        #   otherwise strange errors result
        # IntersectionAngle = math.fmod(IntersectionAngle + 180, 90)
        IntersectionAngle = math.fmod(IntersectionAngle + 180, 180)
        if IntersectionAngle > 90:
            IntersectionAngle = 180 - IntersectionAngle
        boundary_offset = abs(total_swath_g * math.cos(math.radians(IntersectionAngle)))
        BearingCCW90 = math.fmod(VerticesRangeBearing[x][3]+270,360)
        OffsetAngle = math.fmod(450-BearingCCW90, 360)
        dNorthing = math.sin(math.radians(OffsetAngle))*boundary_offset
        dEasting = math.cos(math.radians(OffsetAngle))*boundary_offset
        if debug == 1:
            print (VerticesRangeBearing[x][3],
                   IntersectionAngle,
                   boundary_offset,
                   OffsetAngle,
                   dNorthing,
                   dEasting)
            
        expandedRangeBearing.append([VerticesRangeBearing[x][0] + dNorthing, \
                                     VerticesRangeBearing[x][1] + dEasting, \
                                     VerticesRangeBearing[x][2], \
                                     VerticesRangeBearing[x][3]])
    if debug ==1:
        print 'expandedRangeBearing', len(expandedRangeBearing), 'Items\n', expandedRangeBearing, '\n\n'
    
    # at this point the coordinates in the expandedRangeBearing list
    # are not the vertices. The intersections for the NERB's must be
    # calculated and the range/bearings updated.
    # THIS WORKS - Don't change
    ExpandedVerticesRangeBearing = []
    # calculate the intersection points
    for x in range(len(expandedRangeBearing)):
        y = int(math.fmod(x+len(expandedRangeBearing)-1,len(expandedRangeBearing)))
        # y is the decrement by one in the range
        temp = NERBsIntersect(expandedRangeBearing[x],
                              expandedRangeBearing[y])
        ExpandedVerticesRangeBearing.append([temp[0], temp[1]])
    if debug ==1:
        print 'expandedRangeBearing', len(expandedRangeBearing), 'Items\n', expandedRangeBearing, '\n\n'
        print 'ExpandedVerticesRangeBearing\n', ExpandedVerticesRangeBearing, '\n\n'
    #calulate the range and bearing between the new intersection points
    for x in range(len(ExpandedVerticesRangeBearing)):
        y = int(math.fmod(x+1,len(ExpandedVerticesRangeBearing)))
        # y is the increment by one in the range
        if debug ==1:
            print ExpandedVerticesRangeBearing[x]
            print ExpandedVerticesRangeBearing[y]
        temp = GridRangeBearing((0,
                                ExpandedVerticesRangeBearing[x][0],
                                ExpandedVerticesRangeBearing[x][1],
                                ''),
                                (0,
                                ExpandedVerticesRangeBearing[y][0],
                                ExpandedVerticesRangeBearing[y][1],
                                '')                                 
                                )
        ExpandedVerticesRangeBearing[x].append(temp[0]) # append the range
        ExpandedVerticesRangeBearing[x].append(temp[1]) # append the bearing
        
    if debug==1:
        print 'ExpandedVerticesRangeBearing, Final Update before determining \
        line pattern spacing'
        for x in range(len(ExpandedVerticesRangeBearing)):
            print ExpandedVerticesRangeBearing[x]
        print ''

    # now that the vertices of the target block are appropriately defined it
    # is now possible to determine the flight line tracks once the
    # flight pattern and track spacing are determined       

    # This lengthy section of logic code is based on my spreadsheet model to 
    # create a list of centre track points along the E/W axis throught the
    #   relative centre point (0,0). One needs to know the necessary flight
    #   pattern from the plan and the camera swath for the camera mode and
    #   flight altitude. Also correct for the track offset as this affects
    #   line spacing.

    intercepts = []
    intercepts_Northing = []
    intercepts_Easting = []
    intercept = 0
    direction = 0   # a variable that specifies whether the line's track through
                    #   the intercept point will be at the value of the
                    #   TrackOffset given (relative to gridNorth) or in the
                    #   opposing direction.
                    #   direction = 1, means use the given track
                    #   direction = -1, means use the opposite track
                    
    if Block_Pattern == 0:  # this works, DON'T TOUCH
        # Pattern of OmniDirectional Parallel Lines
        x=0
        # determine the eastings for zero and positive offsets
        while (intercept < max_coordinate):
            intercept = x * total_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x+=1
        x=-1
        # determine the eastings for negative offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    
            intercept = x * total_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
        # Note that this will crash if TrackOffset=90
        
    elif Block_Pattern == 1:    # this works, DON'T TOUCH
        # Pattern of Alternating Parallel Lines
        x=0
        # determine the eastings for zero and positive even offsets
        while (intercept < max_coordinate):   
            intercept = x*port_swath_g + x*stbd_swath_g
            direction = 1
            intercepts.append([intercept, direction])
            x+=2           
        x=1
        # determine the eastings for positive odd offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept < max_coordinate):    # for odd values of x
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x+=2
        x=-1
        # determine the eastings for negative odd offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x-=2            
        x=-2
        # determine the eastings for negative even offsets
        # reset intercept so the last value does not trip up the logic
        intercept = 0
        while (intercept > min_coordinate):    # for even values of x
            intercept = (x*port_swath_g) + (x*stbd_swath_g)
            direction = 1
            intercepts.append([intercept, direction])
            x-=2
        intercepts.sort()
                        
    elif Block_Pattern == 2:
        # Centred Racetrack pattern of Parallel Lines
        # Since all of the intercept values are divided by the TrackOffset
        # correction factor and there will be a RouteOffset correction as well
        # which is the same in all cases, why not do it at the end. Apply it to the
        # easting_intercepts object at the end. For that matter call variable
        # intercepts and place in easting_intercepts or northing_intercepts as
        # required. Decide at the beginning, which one is required.
        x=0
        while intercept < max_coordinate:
            intercept = x*(port_swath_g + stbd_swath_g)
            direction = 1
            intercepts.append(intercept)
            x+=1
        x=-1
        while intercept > min_coordinate:
            intercept = (x-1)*port_swath_g + (x+1)*stbd_swath_g
            direction = -1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
        
    else:
        # Centred Racetrack pattern of Parallel Lines Alternating
        #  Direction every R'th Line. Use the pattern number if>2
        x=0
        R=Block_Pattern-1    # the pattern reversal number, every 'R' lines
        while intercept < max_coordinate:
            isodd = int(math.modf(math.floor(x/R))[1]%2)            
            # isodd = 1 (if x/R is odd) = 0 (if x/R is even)
            intercept = (x-isodd)*port_swath_g + (x+isodd)*stbd_swath_g
            if not isodd:
                direction = 1
            else:
                direction = -1
            intercepts.append([intercept, direction])
            x+=1
        x=-1
        while intercept > min_coordinate:
            isodd = int(math.modf(math.floor(x/R))[1]%2)
            intercept = (x-isodd)*port_swath_g + (x+isodd)*stbd_swath_g
            if isodd:
                direction = -1
            else:
                direction = 1
            intercepts.append([intercept, direction])
            x-=1
        intercepts.sort()
    #==========================================================================
    #   the pattern has now been generated. It is time to turn it into numbers
    #   along the N-S or E-W axes, which ever is most appropriate.
    #
    easting_spacing_factor = math.cos(math.radians(TrackOffset))
    northing_spacing_factor = math.sin(math.radians(TrackOffset))
    
    route_offset = RouteOffset*total_swath_g/100
    # Note: In future, watch out for implicit int. (RouteOffset/100) is an integer =0 because
    #       RouteOffset and 100 are integer and the result was rounded down to 0

    # a displacement of the spacing equivalent to a % of the total
    #   guaranteed swath. 
    for x in range(len(intercepts)):
        intercepts[x][0] += route_offset
    # a correction of the spacing for the grid deviation
    #   if the Track Offset is less than 45 degrees off the N-S grid line create a list
    #       of intercepts along the E-W grid line through the block centre point. Otherwise
    #       create a list of intercepts along the N-S grid line
    #
    if math.fmod(360+TrackOffset,180)<=45 or math.fmod(360+TrackOffset,180)>=135:
        spacing_factor = easting_spacing_factor
        for x in range(len(intercepts)):
            intercepts[x][0] /= spacing_factor
            if intercepts[x][1] > 0:
                intercepts[x][1] = TrackOffset
            else:
                intercepts[x][1] = TrackOffset+180
            intercepts[x].insert(0,0.0) #   insert '0.0' as an Northing in the list
            intercepts[x].insert(2,100.0) # insert '100.0' as a dummy Range value in the list
    else:
        spacing_factor = northing_spacing_factor
        for x in range(len(intercepts)):
            intercepts[x][0] /= spacing_factor
            if intercepts[x][1] > 0:
                intercepts[x][1] = TrackOffset
            else:
                intercepts[x][1] = TrackOffset+180
            intercepts[x].insert(1,0.0) #   insert '0.0' as an Easting in the list
            intercepts[x].insert(2,100.0) # insert '100.0' as a dummy Range value in the list

    # now that the factoring has been completed the elements in the intercepts
    #   object should be immuteable, so change each top-level list item to a tuple
    for x in range(len(intercepts)): intercepts[x]=tuple(intercepts[x])

    # now use the RelativeVertices Data and expand the boundary sufficiently to
    # ensure complete coverage at the terminus of every line.
    # use the pattern spacing list 'intercepts' and the expanded boudary values
    #   in ExpandedVerticesRangeBearing to determine the intersections of the
    #   pattern lines with the boundary.
    # use the function NERBsIntersect to find the intersection points of each
    #   pattern line with all of the boundary segments. The function returns a
    #   flag that indicates whether the intersecion point is within the confines
    #   of the boudary segment. Save only the intersecion points that are within
    #   the segments
    #
    #   This WORKS Do not revise
    #
    # this currently does not retain information about the required track of the
    #   route. The order of the points in the should reflect the intended track, the
    #   first point being the start, and the second point being the end.
    TargetBlockIntercepts = []  # the storage location for the intercepts
    for x in range(len(intercepts)):
        LineIntersections = [] # a temporary container for intersectiion points
        for y in range(len(ExpandedVerticesRangeBearing)):
            temp = NERBsIntersect(ExpandedVerticesRangeBearing[y],
                                  intercepts[x]
                                  )
            if temp[2]==1:   # is the intercept flag '1'
                LineIntersections.append([Datum, temp[0], temp[1], UTMZone])
        # check the orientation
        # note, that there should only be two tuples in the LineIntersections object
        if len(LineIntersections)==2:   # a test
            #if LineIntersections != []:
            LineIntersections.append(math.fmod(360+intercepts[x][3],360))
            # append the bearing of the planned track
            temp = GridRangeBearing(LineIntersections[0],
                                    LineIntersections[1]
                                    )
            if abs(LineIntersections[2]-temp[1])>5 :
                # checks the Bearing agrees with the order of the points,
                # otherwise we need to swap the points so the 1st pt is the start
                # and the 2nd pt is the end and it agrees with the bearing.
                # need to swap, done by direct assignment
                LineIntersections[0], LineIntersections[1] = \
                                      LineIntersections[1], LineIntersections[0]
            TargetBlockIntercepts.append(LineIntersections)
    
    if debug == 1:
        print 'TargetBlockIntercepts'
        for x in range(len(TargetBlockIntercepts)):
            print x, TargetBlockIntercepts[x]
    
    # now that the lines have been determined by intercepts with the Expanded Block
    #   area, the waypoints for the routes can be generated using the LineSite2Route
    #   function. In calling this function the Waypoint entry will be constructed from the
    #   'TargetBlocksIntercepts' object and the plan will be reconstructed rather than
    #   read from the database.
    #
    #   This section also adds the centre offset that was removed from the coordinate
    #   values of the vertices of the target area. The numbers will correspond to real
    #   UTM space.

    if NumViewAngles==1:    # check that only one view angle has been specified for the target
        view_angle_offset = FlightAltitude*math.tan(math.radians(ViewAngles[0]))
    else:
        view_angle_offset = 0

    for x in range(len(TargetBlockIntercepts)):
        Nav_UTM = {}
        Nav_LL = {}
        LineKeyNum = x
        KeyNum = 0
        
        # UTM navigation start waypoint
        offset = Offset(NavLeadin + Leadin + view_angle_offset, TargetBlockIntercepts[x][2])
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],              
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM line start waypoint    
        offset = Offset(Leadin + view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM site start waypoint    
        offset = Offset(view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][0][0],
                                TargetBlockIntercepts[x][0][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][0][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][0][3])

        # UTM site end waypoint    
        offset = Offset(view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])

        # UTM line end waypoint    
        offset = Offset(-Leadout + view_angle_offset, TargetBlockIntercepts[x][2])
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])

        # UTM navigation end waypoint 
        offset = Offset(-(NavLeadout + Leadout) + view_angle_offset, TargetBlockIntercepts[x][2])    
        KeyNum = KeyNum+1
        Nav_UTM[KeyNum] = (TargetBlockIntercepts[x][1][0],              
                                TargetBlockIntercepts[x][1][1] - offset[0] + Centre_Wpt[0],
                                TargetBlockIntercepts[x][1][2] - offset[1] + Centre_Wpt[1],
                                TargetBlockIntercepts[x][1][3])
        Block_Nav_UTM[x] = Nav_UTM
        Nav_LL = utm2ll_route(Nav_UTM)
        Block_Nav_LL[x] = Nav_LL

    if debug == 1:
        #   another section of printouts for debugging
        #   for checking the parameters that are passed into the function
        #
        print 'route_offset(m)=', route_offset, 'track_offset_factor=',spacing_factor
        print 'FlightAltitude',FlightAltitude 
        print 'Leadin',Leadin, 'metres'
        print 'Leadout',Leadout, 'metres'
        print 'SiteDiameter',SiteDiameter, 'metres'     
        print 'NavLeadin',NavLeadin, 'metres'
        print 'NavLeadout',NavLeadout, 'metres'
        print 'NumViewAngles',NumViewAngles
        print 'ViewAngles',ViewAngles, 'degrees'
        print 'TrackOffset',TrackOffset, 'degrees'
        print 'casiMode',casiMode
        print 'GridDeviation',GridDeviation, 'degrees'
        print 'MagDeviation',MagDeviation, 'degrees'
        print 'Overlap',Overlap, 'percent'
        print 'RouteOffset',RouteOffset, 'percent'
        print 'Block_Pattern',Block_Pattern
        print 'Comment',Comment
        print 'Tau',Tau
        print 'Bandset',Bandset
        print 'Priority',Priority
        print 'Status',Status
        print 'Vertices\n', Vertices, Centre_Wpt
        print 'RelativeVertices\n', RelativeVertices
        print  '\tE_Min =', min_Easting, 'E_Max =', max_Easting
        print  '\tN_Min =', min_Northing, 'N_Max =', max_Northing
        print 'CentreRangeBearing\n', CentreRangeBearing
        print intercepts
        #   end of section for debugging

# XXX Revise the output of the vertices.
##    Output of the vertices is required for plotting of the target area on a
##    map display at some point. Correct the vertices so they are in real UTM
##    space, not in relative UTM space.
    
    return(Block_Nav_UTM, Block_Nav_LL, Solar_Dat,
           VerticesRangeBearing,
           ExpandedVerticesRangeBearing,
           Centre_Wpt)                              # added for test

    
#==============================================================================
#
#   function utm2ll_Route
#
#       this function currently works only if the dictionary passed to 'utm_route'
#               contains a utm waypoint value for each key.
#       for a block site it is expected that the muliple routes will be dictionaries nested within
#           the dictionary variable passed to this function.
#       the function will need to handle this situation.
#
def utm2ll_route(utm_route):

    route_LL = {}
    for key in utm_route.keys():
        route_LL[key] = geodesy.UTM2LL(utm_route[key][0],
                                       utm_route[key][1],
                                       utm_route[key][2],
                                       utm_route[key][3]
                                       )

    return(route_LL)    # returns a dictionary of the latitude/longitude coordinates
    
#===============================================================================
#   test stuff
#
if __name__ == "__main__":

    import WaypointTarget_IO as wpio

    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\test_sites_1.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    site_utm_db = wpio.generic2site_db(temp_db) # the target database
                  
    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\test_plan_1.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    plan_utm_db = wpio.generic2plan_db(temp_db) # the planning database
    
    mytestfile=r'c:\Documents and Settings\owner\My Documents\Python\pyMap\casi302_config.txt'
    temp_db = wpio.ReadDatabase(mytestfile)
    sensor_db = wpio.generic2sensor_db(temp_db)   # the sensor configuration database
    
    
    #=========================================================================================
    #   test of a single point site
    #
    
    site = 'Sb-1'
    print '\n', site_utm_db[site], plan_utm_db[site][0],'\n'
       
    Result = PointSite2Route(site_utm_db[site], plan_utm_db[site][0])
    utm_route = Result[0]               # get the utm route from Result
    ll_route = Result[1]
    solar_dat = Result[2]               # get the solar data from Result

    # the 6 lines above show how to obtain a route for a point target, code below
    # is window dressing to display the results
    #
    print 'SiteID', site
    print 'Solar Data', solar_dat, '\n'
    print 'Routing Waypoints as UTM Coordinates\n'
    key = utm_route.keys()      # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()                  # sort the integers
    for x in (key):    
        print '\t', x, utm_route[str(x)] # integer converted to string for key

    print '\nRouting Waypoints as Latitude / Longitude Coordinates\n'
    key = ll_route.keys()       # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()
    # sort the integers
    for x in (key):
        print '\t', x, ll_route[str(x)]  # integer converted to string for key

    
    #=========================================================================================
    #   test of a two point site (a predefined line)
    #
    
    site='Pj-6'
    print '\n', site_utm_db[site], plan_utm_db[site][0],'\n'

    Result = LineSite2Route(site_utm_db[site], plan_utm_db[site][0])
    utm_route = Result[0]
    ll_route = Result[1]
    solar_dat = Result[2]
    
    print 'SiteID', site
    print 'Solar Data', solar_dat, '\n'
    print 'Routing Waypoints as UTM Coordinates\n'
    key = utm_route.keys()      # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()                  # sort the integers
    for x in (key):    
        print '\t', x, utm_route[str(x)] # integer converted to string for key

    print '\nRouting Waypoints as Latitude / Longitude Coordinates\n'
    key = ll_route.keys()       # get the keys as strings
    for x in range(0,len(key),1):
        key[x]=int(key[x])      # convert to integers
    key.sort()
    # sort the integers
    for x in (key):
        print '\t', x, ll_route[str(x)]  # integer converted to string for key
    
    
    #=========================================================================================
    #   test of a block site
    #

    site = 'Pj-76'      # in a real program this value will be selected from a list
    config = 'mmeris'   # in a real program this value will be selected from a list
    # this is a spatial config read from the list of multiple plans (if any) for the site
    config = plan_utm_db[site][0][-3] # if the configuration name is 3rd from the end
    
    print 'Start of MAIN TEST Output for a Block Site\n'    
    print '\nSite Selected\n', site_utm_db[site], '\n'
    print '\nPlan Selected\n', plan_utm_db[site][0], '\n'
    print '\nSensor Configuration\n', sensor_db[config][0], '\n'
    
    debug = 0   # turn on debugging for the block site section
    Result = BlockSite2Route(site_utm_db[site],
                             plan_utm_db[site][0],
                             sensor_db[config][0])
    utm_route = Result[0]
    ll_route = Result[1]
    solar_dat = Result[2]
    vertices = Result[3]
    expanded_vertices = Result[4]
    centre = Result[5]
    
    # print 'UTM Routing Data\n', utm_route, '\n'
    # print 'Lat/Long Routing Data\n', ll_route, '\n'
    print 'Solar Ephemerus Data\n', solar_dat, '\n'
    # print '\nEND OF MAIN TEST OUTPUT for a Block Site\n'
    
    # Output of the Vertices and Routing data in a sensible fashion so the results can be copied and
    # checked as an ordered list of data
    #
    print 'Vertices'
    for x in range(len(vertices)):
        print x, vertices[x]
    print 0, vertices[0]
    print '\nExpanded_Vertices'
    for x in range(len(expanded_vertices)):
        print x, expanded_vertices[x]
    print 0, expanded_vertices[0]
    print '\nCentre_Waypoint'
    print '0', centre, '\n'
    
    key = utm_route.keys()          # get the keys as strings
    key.sort()                      # sort the integers
    print 'Block_Nav_UTM'
    for x in range(len(key)):
        key1 = utm_route[key[x]].keys()
        key1.sort()
        for y in range(len(key1)):
            print key[x], key1[y], utm_route[key[x]][key1[y]]
        print ''

    key = ll_route.keys()          # get the keys as strings
    key.sort()                      # sort the integers
    print 'Block_Nav_LL'
    for x in range(len(key)):
        key1 = ll_route[key[x]].keys()
        key1.sort()
        for y in range(len(key1)):
            print key[x], key1[y], ll_route[key[x]][key1[y]]
        print ''
    

>>>>>>> .r108
