meArmPi
=======

Inverse Kinematics movement control library in Python for Phenoptix meArm on Raspberry Pi via Adafruit PWM Servo driver.

The meArm has four mini servos - one for the gripper, and one each to rotate the base, shoulder joint and elbow joint. But it's not terribly convenient to be specifying things in terms of servo angles when you're much more interested in where you would like to place the gripper, in normal Cartesian (x, y, z) coordinates.

This library solves the angles required to send to the servos in order to meet a given position, allowing for much simpler coding.

Coordinates are (approximately) measured in mm from the base rotation centre. Initial 'home' position is at (0, 100, 50), i.e. 100mm forward of the base and 50mm off the ground.

Various other versions of this library exist:
* [Arduino](https://github.com/yorkhackspace/meArm)
* [Arduino with Adafruit PWM driver board](https://github.com/RorschachUK/meArm_Adafruit)
* [Beaglebone Black](https://github.com/RorschachUK/meArmBBB)

[![meArm moving with Inverse Kinematics](http://img.youtube.com/vi/HbxhVs3UmuE/0.jpg)](http://www.youtube.com/watch?v=HbxhVs3UmuE)

Wiring
------

This uses an Adafruit 16-channel PWM servo driver board to connect the servos to the Raspberry Pi.  Use the first block of four servo connectors, and connect yellow wire to the top, brown wire to the bottom.
* Servo 0: meArm rotating base
* Servo 1: meArm shoulder (right hand side servo)
* Servo 2: meArm elbow (left hand side servo)
* Servo 3: meArm gripper

Connect the Adafruit PWM Servo driver to the Pi as follows (I used Adafruit Pi Cobbler to help breadboard it):
* Adafruit GND to RPi GND
* Adafruit SCL to RPi SCL0
* Adafruit SDA to RPi SDA0
* Adafruit VCC to RPi 3.3V
* Adafruit V+ to RPi 5V

Usage
-----

```
import meArm

def main():
    arm = meArm.meArm()
    arm.begin()
	
    while True:
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()
        arm.closeGripper()
        arm.openGripper()
        
        #Go up and left to grab something
        arm.gotoPoint(-80,100,140) 
        arm.closeGripper()
        #Go down, forward and right to drop it
        arm.gotoPoint(70,200,10)
        arm.openGripper()
        #Back to start position
        arm.gotoPoint(0,100,50)
    return 0

if __name__ == '__main__':
	main()
```

One usage examples is included:
* DemoIK follows a pre-programmed path defined in Cartesian coordinates

Installation
------------
* Clone this repository to your local machine
* Run with sudo, i.e. 'sudo python DemoIK.py'

Class methods of meArm object
-----------------------------
* begin(block=0, address=0x40) - determines which block of four servo connections to use (0 to 3) and which I2C address the Adafruit can be found on - defaults to 0x40.  Begin must be called before any other calls to the meArm instance are made.
* openGripper() - opens the gripper, letting go of anything it was holding
* closeGripper() - closes the gripper, perhaps grabbing and holding something as it does so
* gotoPoint(x, y, z) - move in a straight line from the current point to the requested position
* goDirectlyTo(x, y, z) - set the servo angles to immediately go to the requested point without caring what path the arm swings through to get there - faster but less predictable than gotoPoint
* isReachable() - returns true if the point can theoretically be reached by the arm
* getPos() - current [x, y, z] coordinates
