# Inverse kinetics, adapted for Python by Bob Stone from C++ original by Nick Moriarty May 2014
# Original is here: https://github.com/aquila12/me-arm-ik
#
# This code is provided under the terms of the MIT license.
# 
# The MIT License (MIT)
# 
# Copyright (c) 2014 Nick Moriarty
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

L1 = 80 # Shoulder to elbow length
L2 = 80 # Elbow to wrist length
L3 = 68 # Wrist to hand plus base centre to shoulder
	
def cart2polar(x, y):
    # Determine magnitude of cartesian coordinates
    r = math.hypot(x, y)
    # Don't try to calculate zero magnitude vectors angles
    if r == 0:
        return
		
    c = x / r
    s = y / r
	
    # Safety!
    if s > 1: s = 1
    if c > 1: c = 1
    if s < -1: s = -1
    if c < -1: c = -1
	
    # Calculate angle in 0..PI
    theta = math.acos(c)
	
    # Convert to full range
    if s < 0: theta = -theta
	
    return r, theta

# Get angle from triangle using cosine rule
def cosangle(opp, adj1, adj2, theta):
    # Cosine rule:
    # C^2 = A^2 + B^2 - 2*A*B*cos(Angle_AB)
    # cos(Angle_AB) = (A^2 + B^2 - C^2)/(2*A*B)
    # C is opposite
    # A, B are adjacent
	
    den = 2 * adj1 * adj2
	
    if den == 0:
        return False
    c = (adj1 * adj1 + adj2 * adj2 - opp * opp)/den
    if c > 1 or c < -1:
        return False
    theta[0] = math.acos(c)
    return True
	
# Solve angles
def solve(x, y, z, angles):
    # Solve top-down view
    r, th0 = cart2polar(y, x)
    r -= L3 # Account for the wrist length
	
    # In arm plane, convert to polar
    R, ang_P = cart2polar(r, z)
	
    parmB = [0]
    parmC = [0]
	
    # Solve arm inner angles as required
    if not cosangle(L2, L1, R, parmB): return False
    if not cosangle(R, L1, L2, parmC): return False
    B = parmB[0]
    C = parmC[0]
	
    # Solve for servo angles from horizontal
    a0 = th0
    a1 = ang_P + B
    a2 = C + a1 - math.pi
	
    angles[0] = a0
    angles[1] = a1
    angles[2] = a2
	
    return True
	
# Forward kinematics - for unsolving!

def polar2cart(r, theta):
    a = r * math.cos(theta)
    b = r * sin(theta)
    return a,b
	
def distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
	
def unsolve(a0, a1, a2):
    # Calculate u,v coordinates for arm
    u01, v01 = polar2cart(L1, a1)
    u12, v12 = polar2cart(L2, a2)
	
    # Add vectors
    u = u01 + u12 + L3
    v = v01 + v12
	
    # Calculate in 3D space - note x/y reversal!
    y, x = polar2cart(u, a0)
    z = v
    return x, y, z
