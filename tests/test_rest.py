from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from alerts_service import models


@pytest.mark.asyncio
async def test_create_borrower(client: TestClient, session: Session) -> None:
    resp = client.post("/api/v1/borrowers", json={"name": "Test Company"})
    assert resp.status_code == 200
    borrower_json = resp.json()
    assert borrower_json["name"] == "Test Company"
    assert borrower_json["total_revenue"] is None
    assert borrower_json["borrower_id"] > 0
    assert datetime.fromisoformat(borrower_json["last_modified"]) is not None


@pytest.mark.asyncio
async def test_create_list_borrowers(client: TestClient, session: Session) -> None:
    create_resp = client.post("/api/v1/borrowers", json={"name": "Test Company"})
    borrower = create_resp.json()

    list_resp = client.get("/api/v1/borrowers").json()
    assert list_resp == [borrower]


@pytest.mark.asyncio
async def test_update_borrower(client: TestClient, session: Session) -> None:
    borrower = models.Borrower(name="Test Company")
    session.add(borrower)
    session.flush()
    session.refresh(borrower)
    create_timestamp = borrower.last_modified

    borrower_update_resp = client.put(
        f"/api/v1/borrowers/{borrower.borrower_id}",
        json={"name": "Test Company", "total_revenue": 1000.0},
    )
    assert borrower_update_resp.status_code == 200
    updated_borrower = borrower_update_resp.json()
    assert updated_borrower["total_revenue"] == 1000.0
    assert datetime.fromisoformat(updated_borrower["last_modified"]) > create_timestamp

    # Update the borrower again, but don't specify `total_revenue`
    # This should set the `total_revenue` value to null, as this is a full update (a put not a patch)
    borrower_update_2_resp = client.put(
        f"/api/v1/borrowers/{borrower.borrower_id}",
        json={"name": "Test Company", "ebitda": 100.0},
    )
    assert borrower_update_2_resp.status_code == 200
    updated_borrower_2 = borrower_update_2_resp.json()
    assert updated_borrower_2["total_revenue"] is None
    assert updated_borrower_2["ebitda"] == 100.0


@pytest.mark.asyncio
async def test_create_alert(client: TestClient, session: Session) -> None:
    resp = client.post(
        "/api/v1/alerts", json={"data_item": "total_revenue", "operator": "lt", "value": 1}
    )
    alert_json = resp.json()
    assert alert_json["data_item"] == "total_revenue"
    assert alert_json["operator"] == "lt"
    assert alert_json["value"] == 1.0
    assert alert_json["alert_id"] > 0
    assert datetime.fromisoformat(alert_json["last_modified"]) is not None


@pytest.mark.asyncio
async def test_create_list_alert(client: TestClient, session: Session) -> None:
    resp = client.post(
        "/api/v1/alerts", json={"data_item": "total_revenue", "operator": "lt", "value": 1}
    )
    alert_json = resp.json()

    list_resp = client.get("/api/v1/alerts").json()
    assert list_resp == [alert_json]


@pytest.mark.asyncio
async def test_triggered_alert(client: TestClient, session: Session) -> None:
    good_borrower = models.Borrower(name="Good Company", total_revenue=100.0)
    bad_borrower = models.Borrower(name="Bad Company", total_revenue=0.0)
    null_borrower = models.Borrower(name="Null Company")
    session.add_all([good_borrower, bad_borrower, null_borrower])
    session.flush()

    alert_resp = client.post(
        "/api/v1/alerts", json={"data_item": "total_revenue", "operator": "lt", "value": 1}
    )
    alert_json = alert_resp.json()

    triggered_borrowers = client.get(
        f"/api/v1/alerts/{alert_json['alert_id']}/borrowers"
    ).json()
    assert len(triggered_borrowers) == 1
    assert triggered_borrowers[0]["borrower_id"] == bad_borrower.borrower_id
