import time
import json
import zmq
from ik import ik

# Setting up zmq stuff
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5000")

ikObj = ik.ik()

while True:
    message = socket.recv()
    print("goal_position received\n")

    # Parse the message to get goalPOS values
    messageJSON = json.loads(message)
    goalPOS = messageJSON["goal_position"]
    print("goal_position: ")
    print(goalPOS)

    # call IK with goalPOS
    motor_angles = ikObj.inv_kine(goalPOS)
    print("motor_angles calculated: ")
    print(motor_angles)

    # Creating an 'Empty' JSON packet to send as signal
    send_dict{
        "lol" : 0
    }

    send_packet = json.dumps(send_dict)

    # Sending our signal packet
    socket.send_string(send_packet)
    print("JSON packet sent!: \n" + send_packet)

    # Tell the arm to move to the calculated angles
    