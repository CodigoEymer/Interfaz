import rospy
from mavros_msgs.msg import *
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *

def land():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        land_service = rospy.ServiceProxy('/mavros/cmd/land', CommandTOL)
        response = land_service(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
        return response.success
    except rospy.ServiceException as e:
        print("Service call failed: {}".format(e))

def globalPositionCallback(posicion):
    print("hhola")
    latitude = posicion.latitude
    longitude = posicion.longitude
    altitude = posicion.altitude
    print ("longitude: %.7f" %longitude)
    print ("latitude: %.7f" %latitude)
    print ("latitude: %.7f" %altitude)

def takeoff(altitude):
    rospy.init_node('takeoff', anonymous=True)

    # Crear un objeto que representa el servicio de comando de despegue
    takeoff_service = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)

    # Llamar al servicio de despegue con la altura deseada (en metros)
    if takeoff_service(altitude=altitude):
        print("Comando de despegue enviado. Altitud: %f metros", altitude)
    else:
        print("No se pudo enviar el comando de despegue")

if __name__ == '__main__':
    rospy.init_node('landing')
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)

    takeoff(1)

    rospy.spin()
    #globalPositionCallback()
    #land()

