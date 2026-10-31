import os
import random
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

class MeditrackAPIClient:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000")
        self.token = None

    def login(self, username, password):
        try:
            response = requests.post(
                f"{self.base_url}/login",
                data={"username": username, "password": password},
                timeout=3
            )
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                return True
        except requests.exceptions.RequestException:
            # Offline synthetic fallback mode if local API container is asleep
            if username == "admin_user" and password == "admin123":
                self.token = "offline_synthetic_dev_token"
                return True
        return False

    def _get_headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def get_patients(self):
        try:
            response = requests.get(f"{self.base_url}/patients", headers=self._get_headers(), timeout=3)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return self._generate_fallback_patients()

    def get_appointments(self):
        try:
            response = requests.get(f"{self.base_url}/appointments", headers=self._get_headers(), timeout=3)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return self._generate_fallback_appointments()

    def get_visits(self):
        try:
            response = requests.get(f"{self.base_url}/visits", headers=self._get_headers(), timeout=3)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return []

    def get_invoices(self):
        try:
            response = requests.get(f"{self.base_url}/invoices", headers=self._get_headers(), timeout=2)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass

        random.seed(42)
        statuses = ['PAID', 'PAID', 'PAID', 'ISSUED', 'CANCELLED']
        invoices = []
        base_date = datetime.now()
        for i in range(1, 401):
            dt = base_date - timedelta(days=random.randint(0, 90))
            invoices.append({
                "invoice_id": i,
                "patient_id": random.randint(1, 200),
                "appointment_id": random.randint(1, 300),
                "amount": round(random.uniform(50.0, 750.0), 2),
                "status": random.choice(statuses),
                "issued_date": dt.strftime("%Y-%m-%d %H:%M:%S")
            })
        return invoices

    def get_claims(self):
        try:
            response = requests.get(f"{self.base_url}/claims", headers=self._get_headers(), timeout=2)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass

        random.seed(101)
        statuses = ['APPROVED', 'APPROVED', 'PENDING', 'SUBMITTED', 'REJECTED']
        codes = ['CONSULT-001', 'LAB-DENTAL-02', 'DIAG-PANEL-04', 'PROC-BASIC-11']
        claims = []
        base_date = datetime.now()
        for c_id in range(1, 251):
            dt = base_date - timedelta(days=random.randint(0, 90))
            claims.append({
                "claim_id": c_id,
                "invoice_id": random.randint(1, 400),
                "claim_code": random.choice(codes),
                "claim_amount": round(random.uniform(40.0, 500.0), 2),
                "status": random.choice(statuses),
                "submission_date": dt.strftime("%Y-%m-%d %H:%M:%S")
            })
        return claims

    def _generate_fallback_patients(self):
        random.seed(42)
        first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Riya", "Aadhya", "Ananya", "Diya"]
        last_names = ["Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Khan", "Rao", "Das", "Joshi"]
        patients = []
        for i in range(1, 201):
            patients.append({
                "patient_id": i,
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "date_of_birth": f"{random.randint(1960, 2005)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                "contact_number": f"+91-98{random.randint(10000000, 99999999)}",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d %H:%M:%S")
            })
        return patients

    def _generate_fallback_appointments(self):
        random.seed(42)
        statuses = ["COMPLETED", "COMPLETED", "SCHEDULED", "NO_SHOW", "CANCELLED"]
        appts = []
        for i in range(1, 301):
            appts.append({
                "appointment_id": i,
                "patient_id": random.randint(1, 200),
                "staff_id": random.randint(1, 10),
                "scheduled_time": (datetime.now() - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d %H:%M:%S"),
                "status": random.choice(statuses)
            })
        return appts
    def get_vision_telemetry(self):
        """Fetches and parses YOLOv8 waiting room telemetry from the Visits endpoint."""
        visits = self.get_visits()
        vision_logs = [v for v in visits if v.get("reason_for_visit") == "VISION_AUTO_TELEMETRY"]
        
        parsed_data = []
        for v in vision_logs:
            try:
                # Format: "Entries:12 | Exits:8 | Occ:4 | AvgWait:42.5s"
                notes = v.get("notes", "")
                parts = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in notes.split("|")}
                parsed_data.append({
                    "timestamp": v.get("visit_date"),
                    "entries": int(parts.get("Entries", 0)),
                    "exits": int(parts.get("Exits", 0)),
                    "occupancy": int(parts.get("Occ", 0)),
                    "avg_wait_sec": float(parts.get("AvgWait", "0").replace("s", ""))
                })
            except Exception:
                continue

        if parsed_data:
            return parsed_data

        # Synthetic fallback if live camera stream hasn't pushed records yet
        random.seed(77)
        base_time = datetime.now() - timedelta(hours=4)
        entries, exits = 0, 0
        fallback_logs = []
        for i in range(24):
            t = base_time + timedelta(minutes=i * 10)
            new_in = random.randint(1, 5)
            new_out = random.randint(0, 4)
            entries += new_in
            exits = min(entries, exits + new_out)
            occ = max(0, min(18, entries - exits))
            fallback_logs.append({
                "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                "entries": entries,
                "exits": exits,
                "occupancy": occ,
                "avg_wait_sec": round(random.uniform(25.0, 95.0) if occ > 0 else 0.0, 1)
            })
        return fallback_logs
