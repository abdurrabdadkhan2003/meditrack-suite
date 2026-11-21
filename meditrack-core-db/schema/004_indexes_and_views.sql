-- Indexes on Foreign Keys and Temporal Columns
CREATE INDEX idx_visits_patient_id ON visits(patient_id);
CREATE INDEX idx_visits_visit_date ON visits(visit_date);

CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_staff_id ON appointments(staff_id);
CREATE INDEX idx_appointments_scheduled_time ON appointments(scheduled_time);

CREATE INDEX idx_staff_department_id ON staff(department_id);

-- Analytical View: Daily Visit Summary
CREATE OR REPLACE VIEW view_daily_visit_summary AS
SELECT
    DATE(v.visit_date) AS visit_day,
    COUNT(v.visit_id) AS total_visits,
    COUNT(DISTINCT v.patient_id) AS unique_patients
FROM visits v
GROUP BY DATE(v.visit_date)
ORDER BY visit_day DESC;
-- Analytical View: Department Load / Utilization
CREATE OR REPLACE VIEW view_department_utilization AS
SELECT
    d.department_id,
    d.name AS department_name,
    COUNT(DISTINCT s.staff_id) AS total_staff,
    COUNT(a.appointment_id) AS total_appointments,
    COUNT(CASE WHEN a.status = 'COMPLETED' THEN 1 END) AS completed_appointments,
    COUNT(CASE WHEN a.status = 'NO_SHOW' THEN 1 END) AS no_shows
FROM departments d
LEFT JOIN staff s ON d.department_id = s.department_id
LEFT JOIN appointments a ON s.staff_id = a.staff_id
GROUP BY d.department_id, d.name
ORDER BY total_appointments DESC;

-- Optimization Pass: Composite index for multi-table join and status filtering
CREATE INDEX idx_appointments_staff_status ON appointments(staff_id, status);
