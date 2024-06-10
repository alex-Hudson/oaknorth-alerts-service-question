from typing import Annotated

import fastapi.exceptions
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from alerts_service import models
from alerts_service.types import *

router = APIRouter(prefix="/api/v1")


def get_session() -> Session:
    from alerts_service.db import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/borrowers")
async def create_borrower(
    payload: BorrowerCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Borrower:
    """
    Create a new Borrower by adding a row to the borrowers table

    :param payload: BorrowerCreate - does not contain generated fields such as borrower_id and last_modified
    :param session: SQLAlchemy ORM session injected using FastAPI dependency injection mechanism
    :return: Borrower - the full Borrower model with generated fields
    """
    db_borrower = models.Borrower(
        name=payload.name,
        total_revenue=payload.total_revenue,
        ebitda=payload.ebitda,
        dscr=payload.dscr,
        debt_to_ebitda=payload.debt_to_ebitda,
    )
    session.add(db_borrower)
    session.commit()
    session.refresh(db_borrower)
    return Borrower(
        borrower_id=db_borrower.borrower_id,
        name=db_borrower.name,
        last_modified=db_borrower.last_modified,
        total_revenue=db_borrower.total_revenue,
        ebitda=db_borrower.ebitda,
        dscr=db_borrower.dscr,
        debt_to_ebitda=db_borrower.debt_to_ebitda,
    )


@router.put("/borrowers/{borrower_id}")
async def update_borrower(
    borrower_id: int,
    payload: BorrowerCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Borrower:
    """
    Update an existing borrower given a borrower ID

    This is a full update that replaces all field values with those in the payload

    :param borrower_id: ID of the borrower to update
    :param payload: BorrowerCreate - does not contain generated fields such as borrower_id and last_modified
    :param session: SQLAlchemy ORM session injected using FastAPI dependency injection mechanism
    :return: Borrower - the full Borrower model after the update has been applied
    """
    borrower = session.get(models.Borrower, borrower_id)
    borrower.name = payload.name
    borrower.total_revenue = payload.total_revenue
    borrower.ebitda = payload.ebitda
    borrower.dscr = payload.dscr
    borrower.debt_to_ebitda = payload.debt_to_ebitda
    borrower.last_modified = datetime.now()
    session.commit()
    return Borrower(
        borrower_id=borrower.borrower_id,
        name=borrower.name,
        last_modified=borrower.last_modified,
        total_revenue=borrower.total_revenue,
        ebitda=borrower.ebitda,
        dscr=borrower.dscr,
        debt_to_ebitda=borrower.debt_to_ebitda,
    )


@router.get("/borrowers")
async def list_borrowers(
    session: Annotated[Session, Depends(get_session)],
) -> list[Borrower]:
    """
    Return all Borrowers in the borrower table
    :param session: SQLAlchemy ORM session injected using FastAPI dependency injection mechanism
    :return: List of Borrower objects
    """
    borrowers = session.query(models.Borrower).all()
    return [
        Borrower(
            borrower_id=brw.borrower_id,
            name=brw.name,
            last_modified=brw.last_modified,
            total_revenue=brw.total_revenue,
            ebitda=brw.ebitda,
            dscr=brw.dscr,
            debt_to_ebitda=brw.debt_to_ebitda,
        )
        for brw in borrowers
    ]


@router.post("/alerts")
async def create_alert(
    payload: AlertCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Alert:
    """
    Create a new Alert by adding a row to the alerts table
    :param payload: AlertCreate - the Alert model minus generated fields
    :return: Alert - the full Alert model with all fields including generated fields
    """
    db_alert = models.Alert(
        data_item=payload.data_item,
        operator=payload.operator.value,
        value=payload.value,
    )
    session.add(db_alert)
    session.commit()
    session.refresh(db_alert)
    return Alert(
        alert_id=db_alert.alert_id,
        data_item=db_alert.data_item,
        operator=db_alert.operator,
        value=db_alert.value,
        last_modified=db_alert.last_modified,
    )


@router.get("/alerts")
async def list_alerts(session: Annotated[Session, Depends(get_session)]) -> list[Alert]:
    """
    List all Alerts in the alerts table
    :param session: SQLAlchemy ORM session injected using FastAPI dependency injection mechanism
    :return: List of Alert objects
    """
    alerts = session.query(models.Alert).all()
    return [
        Alert(
            alert_id=alert.alert_id,
            data_item=alert.data_item,
            operator=alert.operator,
            value=alert.value,
            last_modified=alert.last_modified,
        )
        for alert in alerts
    ]


@router.get("/alerts/{alert_id}/borrowers")
async def get_triggered_borrowers(
    alert_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> list[Borrower]:
    """
    Return the borrowers who have triggered an alert with a given alert_id
    :param alert_id: The ID of the Alert
    :param session: SQLAlchemy ORM session injected using FastAPI dependency injection mechanism
    :return: List of Borrower objects which have triggered the Alert
    """
    alert = session.get(models.Alert, alert_id)
    if alert is None:
        raise fastapi.HTTPException(404, detail="Alert not found")
    base_query = session.query(models.Borrower)
    match alert.operator:
        case "lt":
            query = base_query.where(getattr(models.Borrower, alert.data_item) < alert.value)
        case "gt":
            query = base_query.where(getattr(models.Borrower, alert.data_item) > alert.value)
        case "eq":
            query = base_query.where(getattr(models.Borrower, alert.data_item) == alert.value)
        case _:
            raise ValueError(f"Unknown operator {alert.operator}")

    borrowers = query.all()

    return [
        Borrower(
            borrower_id=brw.borrower_id,
            name=brw.name,
            last_modified=brw.last_modified,
            total_revenue=brw.total_revenue,
            ebitda=brw.ebitda,
            dscr=brw.dscr,
            debt_to_ebitda=brw.debt_to_ebitda,
        )
        for brw in borrowers
    ]
