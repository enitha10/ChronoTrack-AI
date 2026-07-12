import json
import os
import time

LEDGER_FILE = "active_occupants.json"

def display_live_dashboard():
    while True:
        # Clear terminal screen dynamically for a clean UI look
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*60)
        print("    CHRONOTRACK AI - LIVE LIBRARY MANAGEMENT DASHBOARD")
        print("="*60)

        if not os.path.exists(LEDGER_FILE):
            print("\n[SYSTEM STATE] Database uninitialized. No active records.")
            time.sleep(3)
            continue

        with open(LEDGER_FILE, 'r') as f:
            ledger = json.load(f)

        # Segmenting data populations using dictionary filtering
        inside_students = [uid for uid, data in ledger.items() if data["status"] == "Inside"]
        checked_out_students = [uid for uid, data in ledger.items() if data["status"] == "Checked Out"]

        total_registered_today = len(ledger)
        current_occupancy = len(inside_students)

        # 1. Macro Metrics Window
        print(f" ► TOTAL STUDENT TOKENS LOGGED TODAY : {total_registered_today}")
        print(f" ► CURRENT ACTIVE REAL-TIME OCCUPANCY: {current_occupancy}")
        print("-" * 60)

        # 2. Dynamic Room State Condition Checklist
        if current_occupancy == 0:
            print(" [STATUS] 🟢 ZONE CLEAR: The library is completely empty.")
        else:
            print(f" [STATUS] 🔴 ZONE OCCUPIED: {current_occupancy} student(s) actively inside.")
        print("-" * 60)

        # 3. Micro Target Tracking Panels
        print(f" Active Occupants Inside ({current_occupancy}):")
        if inside_students:
            for uid in inside_students:
                print(f"   • Student Token ID: {uid} [STATUS: ACTIVE INSIDE]")
        else:
            print("   (No students currently inside)")

        print(f"\n Clear Egress History ({len(checked_out_students)}):")
        if checked_out_students:
            for uid in checked_out_students:
                print(f"   • Student Token ID: {uid} [STATUS: SAFELY EXITED]")
        else:
            print("   (No egress actions logged yet)")

        print("="*60)
        print(" Updating live dashboard views every 3 seconds... (Ctrl+C to Exit)")
        
        # Poll the JSON database file dynamically for changes
        time.sleep(3)

if __name__ == "__main__":
    display_live_dashboard()