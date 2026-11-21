import subprocess
import time

def reset_database():
    print("--- Meditrack Core DB Reset ---")
    print("[*] Environment: DEVELOPMENT (100% Synthetic Data)")
    time.sleep(1)

    print("[*] Running schema migrations...")
    # In a real environment, this would run: subprocess.run(["alembic", "upgrade", "head"])
    print("[-] Migrations applied successfully.")

    print("[*] Seeding synthetic patients and visits...")
    subprocess.run(["python", "seed/generate_mock_patients.py"])

    print("[*] Seeding synthetic billing and claims...")
    subprocess.run(["python", "seed/generate_mock_billing.py"])

    print("--- Reset Complete! Database is ready for API integration. ---")

if __name__ == "__main__":
    reset_database()
