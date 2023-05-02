#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State

# Inicializar el nodo de ROS
rospy.init_node('mission_node')

# Crear una lista de waypoints
waypoints = WaypointList()

# Agregar los waypoints a la lista
wp1 = Waypoint()
wp1.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
wp1.command = 16 # MAV_CMD_NAV_WAYPOINT
wp1.is_current = True
wp1.autocontinue = True
wp1.param1 = 0 # Velocidad en m/s
wp1.param2 = 0 # Aceptable distancia en metros
wp1.param3 = 0 # angulo de viraje en grados
wp1.x_lat = 47.398039 # Latitud en grados
wp1.y_long = 8.545572 # Longitud en grados
wp1.z_alt = 100 # Altitud en metros

wp2 = Waypoint()
wp2.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
wp2.command = 16 # MAV_CMD_NAV_WAYPOINT
wp2.is_current = False
wp2.autocontinue = True
wp2.param1 = 0 # Velocidad en m/s
wp2.param2 = 0 # Aceptable distancia en metros
wp2.param3 = 0 # angulo de viraje en grados
wp2.x_lat = 47.398036 # Latitud en grados
wp2.y_long = 8.545581 # Longitud en grados
wp2.z_alt = 200 # Altitud en metros

wp3 = Waypoint()
wp3.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
wp3.command = 16 # MAV_CMD_NAV_WAYPOINT
wp3.is_current = False
wp3.autocontinue = True
wp3.param1 = 0.3 # Velocidad en m/s
wp3.param2 = 0 # Aceptable distancia en metros
wp3.param3 = 0 # angulo de viraje en grados
wp3.x_lat = 149.1652374 # Latitud en grados
wp3.y_long = -35.3632621 # Longitud en grados
wp3.z_alt = 4 # Altitud en metros


# Modo ESTABLE
print("Activando modo automatico")
rospy.wait_for_service('/mavros/set_mode')
try:
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
except rospy.ServiceException, e:
    print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e



waypoints.waypoints = [wp1, wp2, wp3]

# Enviar los waypoints al drone utilizando el servicio WaypointPush
rospy.wait_for_service('/mavros/mission/push')
waypoint_push = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
response = waypoint_push(start_index=0, waypoints=waypoints.waypoints) 

# Esperar a que se complete la carga de la mision
rospy.sleep(1)

# Armar el drone
rospy.wait_for_service('/mavros/cmd/arming')
arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
arm_response = arm_service(True)
print("armando dron")

# Esperar a que el drone este armado
rate = rospy.Rate(10) # 10 Hz
while not rospy.is_shutdown():
    state = rospy.wait_for_message('/mavros/state', State, timeout=5)
    if state.armed:
        rospy.loginfo('Drone ARMED')
        print("Dron armado")
        break
    rate.sleep()
# Modo automatico
print("Activando modo automatico")
rospy.wait_for_service('/mavros/set_mode')
try:
    flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
    #http://wiki.ros.org/mavros/CustomModes for custom modes
    isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
except rospy.ServiceException, e:
    print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e

# Despegar
print("despegando dron")
rospy.wait_for_service('/mavros/cmd/takeoff')

try:
    takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
    takeoff_response = takeoffService(altitude = 1, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
except rospy.ServiceException, e:
    print "Service takeoff call failed: %s"%e

# Esperar a que el drone alcance la altitud deseada
while not rospy.is_shutdown():
    state = rospy.wait_for_message('/mavros/state', State, timeout=5)
    estadoTake = rospy.wait_for_message('/mavros/cmd/takeoff',mavros_msgs.msg.CommandTOL)
    print(estadoTake)
    if state.armed and state.mode == 'OFFBOARD' and state.system_status == 3:
        print('El dron se encuentra en el aire')  # El dron ha completado el despegue
    rate.sleep() 


# Activar la mision
rospy.wait_for_service('/mavros/cmd/mission/start')
mission_start = rospy.ServiceProxy('/mavros/cmd/mission/start',CommandLong)
mission_start_response = mission_start(command=3001)

while not mission_start_response.success:
    rospy.sleep(0.1)

rospy.wait_for_service('/mavros/cmd/land')
land_service = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
land_response = land_service()

while not land_response.success:
    rospy.sleep(0.1)

rospy.wait_for_service('/mavros/cmd/arming')
disarm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
disarm_response = disarm_service(False)

while not disarm_response.success:
    rospy.sleep(0.1)

rospy.signal_shutdown('Mission complete')