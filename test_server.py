from fastapi.testclient import TestClient

from server import app

client = TestClient(app)

cust = {
    "customerID": 100000,
    "dob": "01/01/1977",
    "income": 25000,
    "bureauScore": 700,
    "applicationScore": 750,
    "maxDelL12M": 0,
    "allowedFoir": 60,
    "existingEMI": 2000,
    "loanTenure": 24,
    "currentAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037",
    "bureauAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037"
}


def test_status():

    response = client.post("/status", json=cust)
    assert response.status_code == 200
    assert response.json() == {
        "addressMatchingScore": 100,
        "approvalStatus": "Approved",
        "loanAmount": 312000.0,
        "loanTenure": 24
    }
