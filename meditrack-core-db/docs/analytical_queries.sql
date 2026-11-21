-- 1. Total revenue collected vs pending
SELECT
    status,
    COUNT(invoice_id) AS total_invoices,
    SUM(amount) AS total_amount
FROM invoices
GROUP BY status;

-- 2. Claim approval rate and settled amount
SELECT
    status,
    COUNT(claim_id) AS claims_count,
    ROUND(SUM(claim_amount), 2) AS aggregated_value
FROM claims
GROUP BY status;

-- 3. High-volume patients with billed amounts
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    COUNT(i.invoice_id) AS total_invoices_billed,
    SUM(i.amount) AS total_billed_amount
FROM patients p
JOIN invoices i ON p.patient_id = i.patient_id
WHERE i.status = 'PAID'
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY total_billed_amount DESC
LIMIT 10;
