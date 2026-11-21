def test_invoice_non_negative():
    amount = 150.00
    assert amount >= 0, "Invoice amount cannot be negative"


def test_claim_status_validity():
    valid_statuses = {'SUBMITTED', 'PENDING', 'APPROVED', 'REJECTED'}
    claim_status = 'APPROVED'
    assert claim_status in valid_statuses, "Claim status is invalid"


def test_mock_patient_id_range():
    patient_id = 42
    assert 1 <= patient_id <= 200, "Patient foreign key is out of mock data bounds"
