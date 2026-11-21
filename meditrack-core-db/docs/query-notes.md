# Database Performance & Query Execution Notes

## Baseline Benchmarking (EXPLAIN ANALYZE)

### Query 1: Filter Visits by Patient ID
```sql
'''
EXPLAIN ANALYZE 
SELECT * FROM visits 
WHERE patient_id = 42;



Execution Plan Before Index: Sequential Scan across table (cost=0.00..12.50 rows=3 width=72).

Execution Plan After Index: Bitmap Heap Scan on idx_visits_patient_id (cost=4.29..8.30 rows=3 width=72).

Execution Time: Reduced from ~1.12ms to ~0.08ms (~14x faster retrieval).


 s

Query 2: Daily Appointment Lookups
SQL
EXPLAIN ANALYZE 
SELECT * FROM appointments 
WHERE scheduled_time BETWEEN '2026-08-01 00:00:00' AND '2026-08-31 23:59:59';
Execution Plan After Index: Index Scan using idx_appointments_scheduled_time.
Execution Time: ~0.11ms.''' 

## Optimization Pass: Department Utilization Joins

### Aggregation Query:
```sql
EXPLAIN ANALYZE 
SELECT * FROM view_department_utilization;

