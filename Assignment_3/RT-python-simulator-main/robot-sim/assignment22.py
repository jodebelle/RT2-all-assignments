#! /usr/bin/env python3

"""
This program is made so the robot finds and grabs silver tokens and pair them with a golden token.
With the codes associated to each token, stored in a list, the robot can verify whether a token has been paired or not.

Functions:
	- def drive(speed, seconds): Function for setting a linear velocity
	- def turn(speed, seconds): Function for setting an angular velocity
	- def find_silver_token(): Function to find the closest silver token
	- def find_golden_token():Function to find the closest golden token
	- def put_Silver_near_Gold(): Function to put the Silver Token close to the Golden Token
	- Following functions of the Robot class are used:
--R.see() = to get the code of each token, the distance of robot from each token and the rotation along the y-axis
--R.grab() = to grab the nearest token
--R.release() = to release token

Steps:
	- Find closest silver token
	- Check if token's code is present in the list
		--> if yes, robot turns and drives
		--> if not, robot grabs the token using R.grab()
			- add token's code to the list
			- robot turns and drives around to find a golden token
	- Find closest golden token
	- Check if token's code is present in the list
		--> if yes, robot turns and drives
		--> if not, robot releases the silver token near the golden token using function put_silver_near_gold()
			- add token's code to the list
			- robot turns and drives around to find the next silver token
	- Repeat all steps until all tokens have been paired (both lists are full)
	- Exit code

"""

from __future__ import print_function
import time
from sr.robot import * # import * is used to import all functions and classes of the sr.robot module
""" Import required libraries"""

a_th = 2.0
a_th1 = 2.0
""" float: Threshold for the control of the linear distance for both Tokens (SILVER/GOLD)"""

d_th = 0.5
d_th1 = 0.5
""" float: Threshold for the control of the orientation for both Tokens (SILVER/GOLD)"""

counter=0
""" integer: variable for controlling the motion of robot after all tokens are paired (stop)"""

a=0
b=0
current_silver_token=[None] * 6
current_golden_token=[None] * 6
""" initializing arrays of None and length 6, and variables a, b for incrementing the arrays """

Check = False

"""
Check variable is used to check if silver and golden tokens codes are already stored in the list.
if the token code is present in the list then we ignore that token and find another one.
"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    
    Syntax: motor board srABC1, channel 1 to half power forward
    R.motor_boards["srABC1"].motors[1].power = 0.5
    """
    R.motors[0].m0.power = speed # setting power of motor 0 connected to motor board (motors[0]) of robot
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    R.see() function 
    """
    dist=100
    for token in R.see(): # getting all the values of the R.see() function in token variable. 
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            Silver_code=token.info.code # This gives us the unique code associated with each Silver Token
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1, -1
    else:
   	return Silver_code, dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist1=100
    for token in R.see():
        if token.dist < dist1 and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist1=token.dist
            Golden_code=token.info.code # This gives us the unique code associated with each Silver Token
	    rot_y1=token.rot_y
    if dist1==100:
	return -1, -1, -1
    else:
   	return Golden_code, dist1, rot_y1


def put_Silver_near_Gold():
    """
    Function to put the Silver token close to the Golden token

    Robot checks the distance from golden token and if distance is less than threshold then the robot releases the silver token
    Then the robot drives a bit and exits the loop to go back to the main loop and find another silver token

    """
    global b # Making the variable b global so that we can use it inside the function
    while 1: # While loop to move the robot until Golden token is not found and silver token is not paired
    	Golden_code, dist1, rot_y1 = find_golden_token() # Getting Golden token unique code, dist from robot and rotation along y-axis

        # Check if the visible token's code is present in the list 
        # if yes, Check variable is true, otherwise, false
        if Golden_code in current_golden_token:
            Check = True
            print("token's code present in the list")
        else:
            Check = False
            print("token's code is not present in the list \n")
        # the robot only pairs tokens that haven't been paired before, so whose codes are not present in the list
        if Check == False:
            if dist1==-1: # if no token is detected, we make the robot turn 
	            turn(10, 1)
            elif dist1 <d_th1: 
                print("Golden token found")
                R.release() # if Golden token is near, release the Silver token to make the pair
                current_golden_token[b]=Golden_code # add the current golden token's code to the list on current index (index starts at 0)
                b=b+1 # increase the value of the index to update list       
                drive(-30,2)
                turn(20,2)
                break # break the loop if golden token is released
            elif -a_th1<= rot_y1 <= a_th1: # if the robot is well aligned with the token, we go forward
                drive(85, 0.5)

            elif rot_y1 < -a_th1: # if the robot is not well aligned with the token, we move it on the left or on the right
                print("Turn a bit left")
                turn(-2, 0.5)
            elif rot_y1 > a_th1:
                print("Turn a bit right")
                turn(+2, 0.5)
        else:
            turn(10,1)
            drive(10,1)

"""Main While loop of the Code: """
while 1:
    # get the code of silver token, distance from robot and the rotation along y-axis
    Silver_code, dist, rot_y = find_silver_token()
    Golden_code, dist1, rot_y1 = find_golden_token()


    # Check if code of visible silver token is present in the list
    if Silver_code in current_silver_token: 
        Check = True # if it is present, then change the value of the Check variable
    else:
        Check = False # else don't change

    # Robot only grabs the silver token if code of the token was not previously stored in the list
    if Check == False:
        if dist==-1: # if no token is detected, we make the robot turn 
	        turn(10, 1)
        elif dist <d_th: # if we are close to the token, we grab it
            # if we grab the token, then we add the code of the token on the current index of the list
            # the value of the index is increased and list is updated so that same token cannot be grabbed again
            if R.grab(): 
                current_silver_token[a]=Silver_code
                a=a+1
	        turn(-25, 2)
	        put_Silver_near_Gold() # if token is grabbed, we call function put_silver_near_gold() to pair it with a golden token
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we make it drive forward
            drive(85, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we make it turn left or right
            turn(-2, 0.5)
        elif rot_y > a_th:
            turn(+2, 0.5)
    else: # if code of the token is in the list, we make the robot turn a bit to check and find another token not present in the list
        turn(10,1)
        # Check if all the tokens are paired correctly and if so, exit the code
        if None not in current_golden_token:
            turn(15,0.5)
            drive(85,1.5)
            exit()
