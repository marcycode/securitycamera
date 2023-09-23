import cv2
import time
import datetime
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

recording = True
detection = False
detection_stopped_time = None 
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5
frame_size = (int(cap.get(3)), int(cap.get(4)))

fourcc = cv2.VideoWriter_fourcc(*"mp4v") #video code format

while True:
    _,cammy = cap.read() 

    gray = cv2.cvtColor(cammy,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3, 5)
    # reading from the frame

    bodies = face_cascade.detectMultiScale(gray,1.3,5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4",fourcc,20.0,frame_size)
            print("Started recording!")
    
    elif detection:
        '''in this part, we detect if a person has left the frame for a specific amount of time, 
        if a person has then the video will stop '''
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()
    


    if detection:
        out.write(cammy)
    cv2.imshow("My Camera",cammy) #title of window that shows you the frame

    if cv2.waitKey(1) == ord('q'):
       
        break #breaks the program once the q key is hit


cap.release()
cv2.destroyAllWindows()