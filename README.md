# RT2-all-assignments
# Assignment 1: Sphinx documentation
Sphinx documentation about Assignment 2 of Research Track 1
# Assignment 2: Jupyter notebook

This notebook pertains to the second assignment completed in the Research Track 1 course. The objective was to develop a notebook that would serve as a replacement for the user interface on node_a.

This Python script provides a robot controller for goal reaching and visualizes the robot's position and sensor data in real-time using Matplotlib and IPython widgets. 

## Dependencies
Make sure you have the necessary dependencies installed before running the script.
- Python 3
- ROS (Robot Operating System)
- 'assignment_2_2022' ROS package

## Usage
- Make sure you have ROS running and the assignment_2_2022 package set up.
- Run the script.
- The script will initialize the ROS node and set up the necessary publishers, subscribers, and action clients.
- You will see an input field where you can enter the goal coordinates (x and y) for the robot.
- Click the "Send Goal" button to send the goal to the robot. The robot will start moving towards the goal.
- The robot's position will be plotted in real-time using Matplotlib. The plot will be updated as the robot moves.
- The script also displays a bar chart showing the number of goals reached and goals cancelled.
- If you want to cancel the current goal, click the "Cancel Goal" button.
- The script will continue running until you stop it.

## Components
### Visualiser Class
- Manages the real-time visualization of the robot's position using Matplotlib.
- Initializes the plot and sets the plot limits.
- Receives odometry and scan data from the robot and updates the plot accordingly.
- Provides a method to display the final trajectory.
### RobotController Class
- Initializes the ROS node and sets up the necessary publishers, subscribers, and action clients.
- Uses IPython widgets to provide a user interface for sending and canceling goals.
- Updates the bar chart showing the number of goals reached and goals cancelled.
- Handles the callback function for goal reaching status.
- Runs the main loop to keep the ROS node alive.
### Laser Callback Function
- Callback function for the LaserScan topic.
- Updates the value of the closest obstacle distance.

# Assignment 3: Statistic analysis
A statistic analysis was made about the efficiency of our python simulator assignment done in Research Track 1.
