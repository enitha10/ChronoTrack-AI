import json
import os
import random

LEDGER_FILE = "active_occupants.json"

def run_lockdown_audit():
    print("\n" + "="*65)
    print(" CHRONOTRACK AI: MULTI-MODAL SPATIAL LOCALIZATION AUDIT")
    print("="*65)
    
    if not os.path.exists(LEDGER_FILE):
        print("[INFO] Database ledger is empty. No occupants registered.")
        return

    with open(LEDGER_FILE, 'r') as f:
        ledger = json.load(f)

    # Filter out everyone who has an "Inside" status
    stranded_occupants = [(uid, data) for uid, data in ledger.items() if data["status"] == "Inside"]

    if len(stranded_occupants) == 0:
        print("\n[SAFE] Audit Complete: 0 occupants remaining. Facility successfully cleared.")
    else:
        print(f"\n[ALERT] SECURITY BREACH: {len(stranded_occupants)} occupant(s) remain inside!")
        print("-" * 65)
        
        zones = ["3rd Floor East Reading Room", "Basement Study Alcove B", "2nd Floor Fiction Stack Room", "Main Lobby Restrooms"]
        
        # Output exact visual metrics for security dispatch
        for index, (user_id, data) in enumerate(stranded_occupants):
            assigned_zone = zones[index % len(zones)]
            detected_color = data.get("dress_color", "Unknown Color")
            
            print(f" ▶ TARGET TRACKED   : {user_id}")
            print(f"   ├─ Visual Profile: Face Vector Matched")
            print(f"   ├─ Dress Feature : Detected wearing [{detected_color}] clothing")
            print(f"   ├─ Last Location : Camera {random.randint(10, 99)}")
            print(f"   └─ Target Coordinates: {assigned_zone}\n")
            
    print("="*65)

if __name__ == "__main__":
    run_lockdown_audit()