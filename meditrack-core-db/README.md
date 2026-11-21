# Meditrack Core Database (`meditrack-core-db`)

Core PostgreSQL relational database module for Checklife clinical operations and financial tracking. Built with strict referential integrity and optimized indexes.

## Architecture
- **Patients & Visits**: Core demographics and footfall tracking.
- **Departments & Staff**: Organizational structure and personnel mapping.
- **Appointments**: Scheduling engine.
- **Billing**: Invoices and claims with strict enum validation.

## Development Setup & Seeding
To completely reset the database and seed it with 100% synthetic, compliance-safe data, run:
`python seed/reset_and_seed.py`

## ERD Diagram
The full ASCII entity-relationship model is located in `docs/erd.md`.
