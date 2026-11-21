+-----------------------+          +---------------------------+
|       patients        |          |          visits           |
+-----------------------+          +---------------------------+
| patient_id (PK, Int)  |<---+     | visit_id (PK, Int)        |
| first_name (VarChar)  |    +----| patient_id (FK, Int)      |
| last_name (VarChar)   |          | visit_date (Timestamp)    |
| date_of_birth (Date)  |          | reason_for_visit (VarChar)|
| contact_number (Var)  |          | notes (Text)              |
| created_at (Timestamp)|          +---------------------------+
+-----------------------+
