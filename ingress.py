import cv2
import face_recognition
import json
import os

# Dynamic Ledger file representing our unordered tracking database
LEDGER_FILE = "active_occupants.json"

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_ledger(ledger):
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)

def run_ingress():
    print("\n[INFO] Starting ChronoTrack AI - Ingress System...")
    print("[INFO] Press 's' to simulate an incoming occupant registration.")
    print("[INFO] Press 'q' to quit the application window.")
    
    # Open the default built-in camera/webcam
    video_capture = cv2.VideoCapture(0)
    ledger = load_ledger()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Camera feed not found.")
            break

        # Convert image color spaces for face_recognition library compatibility
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # Overlay visual tracking rectangles over detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking Active", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show the video feed rendering window
        cv2.imshow('ChronoTrack AI - Ingress Station', frame)
        key = cv2.waitKey(1) & 0xFF

        # Look at camera and press 's' to save the facial embedding and clothing color to our ledger
        if key == ord('s') and face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            if face_encodings:
                user_id = f"ID_{len(ledger) + 101}"
                
                # --- NEW FEATURE: DRESS COLOR EXTRACTION LOGIC ---
                # 1. Grab coordinates for the torso directly below the target's face bounding box
                height, width, _ = frame.shape
                (top, right, bottom, left) = face_locations[0]
                
                torso_top = min(bottom + 20, height - 1)
                torso_bottom = min(bottom + 160, height - 1)
                torso_left = max(left - 30, 0)
                torso_right = min(right + 30, width - 1)

                # 2. Extract clothing region and classify the color profile using pixel intensity thresholds
                if torso_bottom > torso_top and torso_right > torso_left:
                    torso_roi = frame[torso_top:torso_bottom, torso_left:torso_right]
                    avg_color_bgr = torso_roi.mean(axis=0).mean(axis=0)
                    
                    b, g, r = avg_color_bgr[0], avg_color_bgr[1], avg_color_bgr[2]
                    
                    if r > g * 1.3 and r > b * 1.3:
                        dress_color = "Red / Pink"
                    elif g > r * 1.2 and g > b * 1.2:
                        dress_color = "Green"
                    elif b > r * 1.2 and b > g * 1.2:
                        dress_color = "Blue"
                    elif r > 190 and g > 190 and b > 190:
                        dress_color = "White / Light"
                    elif r < 75 and g < 75 and b < 75:
                        dress_color = "Black / Dark"
                    else:
                        dress_color = "Mixed / Casual"
                else:
                    dress_color = "Unknown"
                # -------------------------------------------------

                # Convert vector arrays to list format for JSON serialization
                embedding_list = face_encodings[0].tolist()
                
                # Dynamic push operation into the dictionary ledger with dress color data included
                ledger[user_id] = {
                    "embedding": embedding_list,
                    "status": "Inside",
                    "dress_color": dress_color  # Saving our custom clothing property
                }
                
                save_ledger(ledger)
                print(f"[SUCCESS] Registered: Dynamic Push executed.")
                print(f"          {user_id} added to database ledger.")
                print(f"          Visual Attributes Captured: [{dress_color}] clothing detected.\n")

        elif key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_ingress()