import random
from faker import Faker

fake = Faker()

DEPARTMENTS = ["General Medicine", "Dental", "Cardiology", "Diagnostics", "Orthopedics"]
ROLES = ["Physician", "Specialist", "Consultant", "Head Surgeon"]
STATUSES = ["SCHEDULED", "COMPLETED", "CANCELLED", "NO_SHOW"]

def generate_org_seed():
    with open("seed/mock_org_and_appointments.sql", "w") as f:
        # 1. Departments
        f.write("-- Departments Seed\n")
        f.write("INSERT INTO departments (department_id, name, description) VALUES\n")
        dept_lines = [f"({i+1}, '{name}', '{name} Clinical Unit')" for i, name in enumerate(DEPARTMENTS)]
        f.write(",\n".join(dept_lines) + ";\n\n")

        # 2. Staff (10 synthetic personnel)
        f.write("-- Staff Seed\n")
        f.write("INSERT INTO staff (staff_id, department_id, first_name, last_name, role, email) VALUES\n")
        staff_lines = []
        for s_id in range(1, 11):
            d_id = random.randint(1, len(DEPARTMENTS))
            fn = fake.first_name().replace("'", "")
            ln = fake.last_name().replace("'", "")
            role = random.choice(ROLES)
            email = f"{fn.lower()}.{ln.lower()}@checklife-synthetic.internal"
            staff_lines.append(f"({s_id}, {d_id}, '{fn}', '{ln}', '{role}', '{email}')")
        f.write(",\n".join(staff_lines) + ";\n\n")

        # 3. Appointments (300 mock appointments)
        f.write("-- Appointments Seed\n")
        f.write("INSERT INTO appointments (patient_id, staff_id, scheduled_time, status) VALUES\n")
        appt_lines = []
        for _ in range(300):
            p_id = random.randint(1, 200)
            s_id = random.randint(1, 10)
            t = fake.date_time_between(start_date="-6m", end_date="+1m").strftime("%Y-%m-%d %H:%M:%S")
            st = random.choice(STATUSES)
            appt_lines.append(f"({p_id}, {s_id}, '{t}', '{st}')")
        f.write(",\n".join(appt_lines) + ";\n")

    print("Success: Generated 5 departments, 10 staff members, and 300 appointments.")

if __name__ == "__main__":
    generate_org_seed()
