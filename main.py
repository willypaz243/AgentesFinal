import cv2
import numpy as np

from project.controllers import ServerVision

sv = ServerVision()

def camara():
    cap = cv2.VideoCapture()
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.CV_FOURCC(*'H264')
    #out = cv2.VideoWriter('./media/video_test_1_1.avi', fourcc, 20.0, (640,480))
    active = cap.open('./media/video_test_1.mp4')
    while active:
        active, frame = cap.read()
        if active:
            frame = np.transpose(frame, axes=(1,0,2))
            frame = cv2.resize(frame, (1080,720))
            #frame = np.float32(frame)
            angulos_de_giro = sv.detect_object(frame, color="red", shape="cubo")
            print("angulos", angulos_de_giro)
            cv2.imshow('Video', frame)

        if cv2.waitKey(1) == ord('q'):
            active = False
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camara()