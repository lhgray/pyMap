# simple array test
#
import math
import Numeric as N
import LinearAlgebra as LA

a1=1
a2=1
b1=-1
b2=-0.5
c1=0
c2=1

a = N.array([(a1,b1),(a2,b2)])
b = N.array([(c1),(c2)])

c = LA.solve_linear_equations(a,b)

print a,'\n'
print b,'\n'
print c, c[0], c[1],'\n'

#===================================================
#
# test to solve the intersection of 2 lines specifed as
# a start point (northing, easting) & range & bearing
#
#   Bearing is degrees from Grid North

# intersection point of 2 'NERB's (Northing, Easting, Range, Bearing)

P1=(200,200,100,45) # P1=(Northing, Easting, Range, Bearing)
P2=(200,300,200,315)

a1 = 1
a2 = 1
theta1 = math.fmod(450-P1[3], 360)
theta2 = math.fmod(450-P2[3], 360)
if theta1 == 90 or theta1 == 270:
    a1 = 0
    b1 = 1
    c1 = P1[1]
else:
    a1 = 1
    b1 = -math.tan(math.radians(theta1))
    c1 = P1[0]-P1[1]*math.tan(math.radians(theta1))

if theta2 == 90 or theta2 == 270:
    a2 = 0
    b2 = 1
    c2 = P2[1]
else:
    a2 = 1
    b2 = -math.tan(math.radians(theta2))
    c2 = P2[0]-P2[1]*math.tan(math.radians(theta2))

a = N.array([(a1,b1),(a2,b2)])
b = N.array([(c1),(c2)])
c = LA.solve_linear_equations(a,b)

print 'theta1 =' , theta1, 'theta2 =', theta2
print a,'\n'
print b,'\n'
print c, c[0], c[1],'\n'
 
