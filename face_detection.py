import cv2
import mediapipe as mp

face_mesh = None
face_detected = False

def config_camera(screen_width, screen_height):
    global cap, face_mesh
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def process_face_detection():
    global cap, face_mesh, face_detected
    ret, camera_image = cap.read()

    results = face_mesh.process(camera_image)
    
    if results.multi_face_landmarks:
        return True
    else:
        return False
        