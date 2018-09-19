# A test program to exercise the Linear Equation Solver in
# the Route Generator Module.

# to help debug and verify the routine

#import RouteGenerator as RG
import math
import Numeric as N
import LinearAlgebra as LA

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

    '''
    if e2<>e1:  # so a division by zero error does not result
        theta = math.degrees(math.atan((n2-n1)/(e2-e1)))
    '''

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

    This function will fail if the two lines are parallel, this must be trapped
    in some future revison
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
                            #   data is ignored anyway
    # End of New Section
                    
    temp = GridRangeBearing((0, nerb1[0], nerb1[1], ''),
                            (0, c[0], c[1], '')
                            )
    
    flag=0
    if temp[0] < nerb1[2]:
        if abs(nerb1[3]-temp[1])<15 or abs(abs(nerb1[3]-temp[1])-360)<15:
            flag = 1

    return (c[0], c[1], flag)
    
    
nerb1 = []
nerb2 = []
answer = []

nerb1.append([1000, -1000, 1000, 90])
nerb2.append([-2000, -2000, 1000, 0])
answer.append((1000, -2000, 0))

nerb1.append([-2000, -2000, 2000, 45])
nerb2.append([-2000, 2000, 2000, 315])
answer.append((0,0,0))

nerb1.append([-2000, -2000, 4000, 45])
nerb2.append([-2000, 2000, 4000, 315])
answer.append((0,0,1))

nerb1.append([1000, -1000, 1000, 90])
nerb2.append([-2000, -2000, 1000, 45])
answer.append((1000, 1000, 0))

nerb1.append([1000, -1000, 1000, 225])
nerb2.append([-2000, -2000, 1000, 0])
answer.append((0, -2000, 0))

# Define a square in which the intersections are inside the nerb

nerb1.append([-3000, -2000, 1500, 0])
nerb2.append([-2000, 3000, 1500, 270])
answer.append((-2000, -2000, 1))

nerb1.append([2000, -3000, 1500, 90])
nerb2.append([-3000, -2000, 1500, 0])
answer.append((2000, -2000, 1))

nerb1.append([3000, 2000, 1500, 180])
nerb2.append([2000, -3000, 1500, 90])
answer.append((2000, 2000, 1))

nerb1.append([-2000, 3000, 1500, 270])
nerb2.append([3000, 2000, 1500, 180])
answer.append((-2000, 2000, 1))

# Define a square in which the intersections are outside the nerb

nerb1.append([-1000, -2000, 1000, 0])
nerb2.append([2000, -1000, 1000, 90])
answer.append((2000, -2000, 0))

nerb1.append([2000, -1000, 1000, 90])
nerb2.append([1000, 2000, 1000, 180])
answer.append((2000, 2000, 0))

nerb1.append([1000, 2000, 1000, 180])
nerb2.append([-2000, 1000, 1000, 270])
answer.append((-2000, 2000, 0))

nerb1.append([-2000, 1000, 1000, 270])
nerb2.append([-1000, -2000, 1000, 0])
answer.append((-2000, -2000, 0))


for x in range(len(nerb1)):
    result=NERBsIntersect(nerb1[x],nerb2[x])
    print nerb1[x], '\n', nerb2[x]
    print 'Expected Answer', answer[x]
    print 'Output',
    for y in range(len(result)):
        print int(result[y]),
    print '\n\n',
