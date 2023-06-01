Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Assignment 1: instructions
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

Clone the repository https://github.com/CarmineD8/python_simulator
and switch to the assignment22 branch and run:
python2 run.py assignment.py

Write a python node that:
- search a find a silver box in the environment
- put this silver box close to a golden box
In the end you should try to have silver and golden boxes distributed in pairs.

When done, you can run the program with:

```bash
$ python run.py assignment22.py
```

```bash
$ python run.py solutions/exercise1_solution.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Variables ###

- a_th = 2.0: float: Threshold for the control of the linear distance for SILVER tokens
- a_th1 = 2.0: float: Threshold for the control of the linear distance for GOLD tokens



- d_th = 0.5: float: Threshold for the control of the orientation for SILVER tokens
- d_th1 = 0.5: float: Threshold for the control of the orientation for GOLD tokens


- counter=0: integer: variable for controlling the motion of robot after all tokens are paired (stop)

- a=0, b=0: variables for incrementing the arrays 

Initializing arrays of None and length 6:
- current_silver_token=[None] * 6
- current_golden_token=[None] * 6

Check variable is used to check if silver and golden tokens codes are already stored in the list.
if the token code is present in the list then we ignore that token and find another one:
- Check = False



### Functions ###

* `R.see()` = function used to get the code of each token, the distance of robot from each token and the rotation along the y-axis

* `R.grab()` = function used to grab the nearest token

* `R.release()` = function used to release token

* `def drive(speed, seconds`: Function for setting a linear velocity
Args: speed (int): the speed of the wheels
	seconds (int): the time interval
Syntax: motor board srABC1, channel 1 to half power forward
    	R.motor_boards["srABC1"].motors[1].power = 0.5

* `def turn(speed, seconds)`: Function for setting an angular velocity
Args: speed (int): the speed of the wheels
	  seconds (int): the time interval

* `def find_silver_token()`: Function to find the closest silver token
Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
Use `R.see()`

* `def find_golden_token()`:Function to find the closest golden token
Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
Use `R.see()`

* `def put_Silver_near_Gold()`: Function to put the Silver Token close to the Golden Token
Robot checks the distance from golden token and if distance is less than threshold then the robot releases the silver token
Then the robot drives a bit and exits the loop to go back to the main loop and find another silver token

We make the variable b global so that we can use it inside the function
While loop to move the robot until no golden token is found and silver token is not paired
Get Golden token unique code, the distance from robot and the rotation along y-axis

Check if the visible token's code is present in the list, if yes, Check variable is true, otherwise, false. 
The robot only pairs tokens that haven't been paired before, so whose codes are not present in the list. 
If Golden token is near, use `R.release()` to drop the silver token to make the pair. 
 
Add the current golden token's code to the list on current index (starting at 0). 
Increase the value of the index b to update list.    

### Main code ###

- Find closest silver token (get the code of silver token, the distance from robot and the rotation along y-axis)
	- Check if token's code is present in the list
		- if yes, robot turns and drives (Robot only grabs the Silver Token if not previously stored in the list)
		- if not, robot grabs the token using R.grab()
			- add token's code to the list (list updated)
			- robot turns and drives around to find a golden token
	- Find closest golden token
	- Check if token's code is present in the list
		 - if yes, robot turns and drives
		 - if not, robot releases the silver token near the golden token using function put_silver_near_gold()
			- add token's code to the list (list updated)
			- robot turns and drives around to find the next silver token
	- Repeat all steps until all tokens have been paired (both lists are full)
	- Exit code


### Pseudo Code ###
```
while True
    call find_silver_token
    call find_golden_token

    if currently visible silver token is in the list 
        Check is True 
	
    else
        Check is False 

    if Check is False
    
        if no token is detected
	        robot turns

        elif robot is close to the token
	   if we grab the token
		add the code of the token on the current index of the list
	         robot turns
	         call put_Silver_near_Gold
		 
        elif the robot is well aligned with the token
            robot drives
	    
        elif the robot is not well aligned with the token
            robot turns left or right
	    
    else
        robot turns
  
        if all tokens'code are present in the list, all paired
            robot turns
            robot drives
            exit code
```

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

