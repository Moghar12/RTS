import cv2
import mediapipe as mp
import math
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# ===== Classe Publisher ROS2 =====
class FatiguePublisher(Node):
    def __init__(self):
        super().__init__('fatigue_publisher')
        self.publisher_ = self.create_publisher(String, 'fatigue_events', 10)

    def publish_event(self, blink_count, yawn_count):
        msg = String()
        msg.data = f'Blinks: {blink_count}, Yawns: {yawn_count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Event sent: {msg.data}')


# ===== Initialisation Mediapipe =====
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Indices des landmarks Mediapipe
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374

# Seuils (ajustables selon la caméra et distance)
MOUTH_OPEN_THRESHOLD = 20  # pixels
EYE_CLOSED_THRESHOLD = 5   # pixels

# Compteurs
yawn_count = 0
blink_count = 0

# États et temporisations
blink_state = False
yawn_state = False
last_blink_time = 0
last_yawn_time = 0
BLINK_COOLDOWN = 0.3  # secondes
YAWN_COOLDOWN = 1.0   # secondes

# ===== Initialisation ROS2 =====
rclpy.init()
publisher = FatiguePublisher()

# ===== Capture Vidéo =====
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            def landmark_to_pixel(landmark):
                return int(landmark.x * w), int(landmark.y * h)

            # Coordonnées bouche
            mouth_top = landmark_to_pixel(face_landmarks.landmark[MOUTH_TOP])
            mouth_bottom = landmark_to_pixel(face_landmarks.landmark[MOUTH_BOTTOM])
            mouth_distance = math.hypot(mouth_bottom[0] - mouth_top[0], mouth_bottom[1] - mouth_top[1])

            # Coordonnées yeux gauche et droit
            left_eye_top = landmark_to_pixel(face_landmarks.landmark[LEFT_EYE_TOP])
            left_eye_bottom = landmark_to_pixel(face_landmarks.landmark[LEFT_EYE_BOTTOM])
            left_eye_distance = math.hypot(left_eye_bottom[0] - left_eye_top[0], left_eye_bottom[1] - left_eye_top[1])

            right_eye_top = landmark_to_pixel(face_landmarks.landmark[RIGHT_EYE_TOP])
            right_eye_bottom = landmark_to_pixel(face_landmarks.landmark[RIGHT_EYE_BOTTOM])
            right_eye_distance = math.hypot(right_eye_bottom[0] - right_eye_top[0], right_eye_bottom[1] - right_eye_top[1])

            # Détection bâillement
            if mouth_distance > MOUTH_OPEN_THRESHOLD:
                if not yawn_state and (current_time - last_yawn_time) > YAWN_COOLDOWN:
                    yawn_count += 1
                    yawn_state = True
                    last_yawn_time = current_time
                    publisher.publish_event(blink_count, yawn_count)
            else:
                yawn_state = False

            # Détection clignement (si les 2 yeux sont fermés)
            if left_eye_distance < EYE_CLOSED_THRESHOLD and right_eye_distance < EYE_CLOSED_THRESHOLD:
                if not blink_state and (current_time - last_blink_time) > BLINK_COOLDOWN:
                    blink_count += 1
                    blink_state = True
                    last_blink_time = current_time
                    publisher.publish_event(blink_count, yawn_count)
            else:
                blink_state = False

            # Affichage des mesures et compteurs
            cv2.putText(frame, f'Yawn Count: {yawn_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f'Blink Count: {blink_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Affichage
    cv2.imshow("Fatigue Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Nettoyage
cap.release()
cv2.destroyAllWindows()
publisher.destroy_node()
rclpy.shutdown()
