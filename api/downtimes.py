from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.auth import ServicemanRequired
from api.pagination import PaginationParams, paginate, PaginationResponseSchema
from api.schemas.downtimes import DowntimeResponseSchema, DowntimeCreateSchema
from database import SessionDep
from models import TelemetryLogModel

router = APIRouter(
    prefix="/downtimes",
)


@router.get("/", response_model=PaginationResponseSchema[DowntimeResponseSchema])
async def get_downtimes(
    _: ServicemanRequired,
    session: SessionDep,
    params: Annotated[PaginationParams, Depends()],
):
    """
    Get all downtimes
    """
    return paginate(
        session.query(TelemetryLogModel).order_by(
            TelemetryLogModel.end_date.desc(), TelemetryLogModel.start_date.desc()
        ),
        params,
        DowntimeResponseSchema,
    )


@router.post(
    "/",
    status_code=201,
    responses={400: {"description": "Access point does not exist"}},
)
async def create_downtime(
    _: ServicemanRequired,
    session: SessionDep,
    downtime: DowntimeCreateSchema,
):
    access_point = session.get(TelemetryLogModel, downtime.access_point_id)
    if access_point is None:
        raise HTTPException(400, "Access point does not exist")
    downtime_model = TelemetryLogModel(
        access_point_id=downtime.access_point_id,
        start_date=downtime.start_date,
        end_date=downtime.end_date,
    )
    session.add(downtime_model)
    session.commit()
    return {"status": "ok"}


@router.put("/{id}", status_code=204)
async def update_downtime(
    _: ServicemanRequired,
    session: SessionDep,
    downtime_update: DowntimeCreateSchema,
    downtime_id: int,
):
    downtime: TelemetryLogModel = session.get(TelemetryLogModel, downtime_id)
    if downtime is None:
        raise HTTPException(404, "Downtime not found")
    downtime.start_date = downtime_update.start_date
    downtime.end_date = downtime_update.end_date
    downtime.access_point_id = downtime_update.access_point_id
    session.commit()
