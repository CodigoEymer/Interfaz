import rospy
from mavros_msgs.srv import CommandLong

# Send the command to start the mission
start_mission = CommandLong()
start_mission.command = 300  # MAV_CMD_MISSION_START
start_mission.param1 = 0  # Mission sequence number to start from (0 for first)
start_mission.param2 = 0  # Mission type (0: waypoints, 1: orbit, 2: spline, ...)
start_mission.param3 = 0  # Reserved (set to 0)
start_mission.param4 = 0  # Reserved (set to 0)
start_mission.param5 = 0  # Reserved (set to 0)
start_mission.param6 = 0  # Reserved (set to 0)
start_mission.param7 = 0  # Reserved (set to 0)
start_mission_pub = rospy.Publisher('/mavros/cmd/command', CommandLong, queue_size=10)
start_mission_pub.publish(start_mission)