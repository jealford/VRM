import time
import json
import zmq
from ik import ik
from sensors import sensors

# Setting up zmq stuff
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Setting up our ik and sensors objects
ikObj = ik.ik()
sensorsObj = sensors.sensors()

while True:
    # Wait for next request from the client
    message = socket.recv_string()
    print("goal_position received\n")
   
    # Parse the message to get goalPOS values
    messageJSON = json.loads(message)
    goalPOS = messageJSON["goal_position"]
    print("goal_position: \n" + goalPOS)

    # call IK with goalPOS
    motor_angles = ikObj.inv_kine(goalPOS)
    print("motor_angles calculated: \n" + motor_angles)
    # call temperature gather
    temperature = sensorsObj.getTemp()
    # call moisture gather
    moisture = sensorsObj.getSoil()
    
    # Get our send data and setting up the JSON packet
    send_dict = {
        "motor_angles" : motor_angles,
        "temperature" : 0,
        "moisture" : 0
    }

    send_packet = json.dumps(send_dict)

    socket.send(send_packet)
    print("JSON packet sent!: \n" + send_packet)
    time.sleep(0.0667)