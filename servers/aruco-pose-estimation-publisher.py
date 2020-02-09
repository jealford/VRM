import zmq
import base64
import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math

#--- Define Tag
id_to_find  = 75
marker_size  = 5 #- [cm]

# ZMQ setup
# context = zmq.Context()
# footage_socket = context.socket(zmq.PUB)
# footage_socket.connect('tcp://localhost:5556')

#------------------------------------------------------------------------------
#------- ROTATIONS https://www.learnopencv.com/rotation-matrix-to-euler-angles/
#------------------------------------------------------------------------------
# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])




#--- Get the camera calibration path
calib_path  = ""
camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_webcam.txt', delimiter=',')
camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_webcam.txt', delimiter=',')

#--- 180 deg rotation matrix around the x axis
R_flip  = np.zeros((3,3), dtype=np.float32)
R_flip[0,0] = 1.0
R_flip[1,1] =-1.0
R_flip[2,2] =-1.0

#--- Define the aruco dictionary
aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
parameters  = aruco.DetectorParameters_create()


#--- Capture the videocamera (this may also be a video or a picture)
cap = cv2.VideoCapture(0)
#-- Set the camera size as the one it was calibrated with
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#-- Font for the text in the image
font = cv2.FONT_HERSHEY_PLAIN
i = 0
rvecs, tvecs = None, None
while True:

    #-- Read the camera frame
    ret, frame = cap.read()

    #-- Convert in gray scale
    gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #-- remember, OpenCV stores color images in Blue, Green, Red

    #-- Find all the aruco markers in the image
    corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters)

    if ids is not None: #and ids[0] == id_to_find:



        #-- Unpack the output, get only the first
        rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
        #rvec =
        #tvec # = ret[0][0,0,:], ret[1][0,0,:]

        #ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion, rvec, tvec)
        #-- Draw the detected marker and put a reference frame over it
        aruco.drawDetectedMarkers(frame, corners ) #ids=ids

        #for id in ids:
            #aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec[id], tvec[id], 10)

        #aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 10)


        for rvec, tvec in zip(rvecs, tvecs):
            aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 10)





    # Package and send the frame to Unity
    #encoded, buffer = cv2.imencode('.jpg', frame)
    #jpg_as_text = base64.b64encode(buffer)
    #footage_socket.send(jpg_as_text)
    

    

    #--- use 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
