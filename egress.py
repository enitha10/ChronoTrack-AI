import cv2
import face_recognition
import json
import os
import numpy as np

LEDGER_FILE = "active_occupants.json"

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_ledger(ledger):
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)

def run_egress():
    print("\n[INFO] Starting ChronoTrack AI - Egress System...")
    print("[INFO] Press 'q' to quit the application window.")
    
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        ledger = load_ledger()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), current_encoding in zip(face_locations, face_encodings):
            matched_user_id = None
            
            # Dynamic matching process against our database ledger
            for user_id, data in ledger.items():
                if data["status"] == "Inside":
                    known_embedding = np.array(data["embedding"])
                    # Compare current face with registered ledger faces
                    matches = face_recognition.compare_faces([known_embedding], current_encoding, tolerance=0.5)
                    
                    if matches[0]:
                        matched_user_id = user_id
                        break

            if matched_user_id:
                # Dynamic Drop: Remove/Pop status instantly from active set
                ledger[matched_user_id]["status"] = "Checked Out"
                save_ledger(ledger)
                print(f"[SUCCESS] Egress Match: {matched_user_id} detected exiting. Token dropped from active ledger.")
                
                # Visual feedback on screen
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, f"{matched_user_id} Checked Out", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.putText(frame, "Unknown / External", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('ChronoTrack AI - Egress Station', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_egress()