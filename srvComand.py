#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
from mavros_msgs.msg import WaypointList, Waypoint, State



#global variable
latitude =0.0
longitude=0.0


def setGuidedMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
    except rospy.ServiceException as e:
        print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)
        
def setStabilizeMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
    except rospy.ServiceException as e:
        print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)

def setLandMode():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException as e:
        print("service land call failed: %s. The vehicle cannot land "%e)
          
def setArm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)
    except rospy.ServiceExceptiona as e:
        print("Service arm call failed: %s"%e)
        
def setDisarm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(False)
    except rospy.ServiceException as e:
        print("Service arm call failed: %s"%e)


def setTakeoffMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
    except rospy.ServiceException as e:
        print("service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e)


    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
        takeoffService(altitude = 1, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
    except rospy.ServiceException as e:
        print("Service takeoff call failed: %s"%e)
    
    

def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    global altitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude
    altitude = globalPositionCallback.altitude
    #print ("longitude: %.7f" %longitude)
    #print ("latitude: %.7f" %latitude)

def loadWp():
    # Crear una lista de waypoints
    waypoints = WaypointList()

    # Agregar los waypoints a la lista
    wp1 = Waypoint()
    wp1.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
    wp1.command = 16 # MAV_CMD_NAV_WAYPOINT
    wp1.is_current = True
    wp1.autocontinue = True
    wp1.param1 = 0.1 # Velocidad en m/s
    wp1.param2 = 0 # Aceptable distancia en metros
    wp1.param3 = 0 # angulo de viraje en grados
    #wp1.x_lat = 149.1652374 # Latitud en grados
    wp1.x_lat = 150.1652374 # Latitud en grados
    wp1.y_long = -35.3632621 # Longitud en grados
    wp1.z_alt = 2 # Altitud en metros

    wp2 = Waypoint()
    wp2.frame = 3 # MAV_FRAME_GLOBAL_RELATIVE_ALT
    wp2.command = 16 # MAV_CMD_NAV_WAYPOINT
    wp2.is_current = False
    wp2.autocontinue = True
    wp2.param1 = 0.2 # Velocidad en m/s
    wp2.param2 = 0 # Aceptable distancia en metros
    wp2.param3 = 0 # angulo de viraje en grados
    wp2.x_lat = 149.1652374 # Latitud en grados
    wp2.y_long = -35.3632621 # Longitud en grados
    wp2.z_alt = 3 # Altitud en metros

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

    waypoints.waypoints = [wp1, wp2,wp3]

    # Enviar los waypoints al drone utilizando el servicio WaypointPush
    rospy.wait_for_service('/mavros/mission/push')
    waypoint_push = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
    response = waypoint_push(start_index=0, waypoints=waypoints.waypoints) 

    # Esperar a que se complete la carga de la mision
    rospy.sleep(1)

def validarWp():
    # Esperar a que se inicie la conexin con el drone
    rospy.wait_for_message('/mavros/mission/waypoints', WaypointList)

    # Obtener los waypoints actuales del drone
    waypoints = rospy.wait_for_message('/mavros/mission/waypoints', WaypointList)

    # Mostrar los waypoints en la consola
    print(waypoints.waypoints)


def startMission():
    # Activar la mision
    rospy.wait_for_service('/mavros/cmd/mission/start')
    mission_start = rospy.ServiceProxy('/mavros/cmd/mission/start',CommandLong)
    mission_start_response = mission_start(command=300)

def menu():
    print("Press")
    print("1: to set mode to GUIDED")
    print("2: to set mode to STABILIZE")
    print("3: to set mode to ARM the drone")
    print("4: to set mode to DISARM the drone")
    print("5: to set mode to TAKEOFF")
    print("6: to set mode to LAND")
    print("7: print GPS coordinates")
    print("8: cargar WP")
    print("9: START MISSION")
    print("10: Validar WP")
    
def myLoop():
    x='1'
    while ((not rospy.is_shutdown())and (x in ['1','2','3','4','5','6','7','8','9','10'])):
        menu()
        x = raw_input("Enter your input: ")
        if (x=='1'):
            setGuidedMode()
        elif(x=='2'):
            setStabilizeMode()
        elif(x=='3'):
            setArm()
        elif(x=='4'):
            setDisarm()
        elif(x=='5'):
            setTakeoffMode()
        elif(x=='6'):
            setLandMode()
        elif(x=='7'):
            global latitude
            global longitude
            print ("longitude: %.7f" %longitude)
            print ("latitude: %.7f" %latitude)
            print ("altitude: %.7f" %altitude)
        elif(x=='8'):
            loadWp()
        elif(x=='9'):
            startMission()
        elif(x=='10'):
            validarWp()
        else: 
            print("Exit")
        
        
    

if __name__ == '__main__':
    rospy.init_node('srvComand_node', anonymous=True)
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
    # spin() simply keeps python from exiting until this node is stopped
    
    #listener()
    myLoop()
    #rospy.spin()
