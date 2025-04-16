from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from api.auth import ConsultantRequired
from api.pagination import PaginationParams, paginate, PaginationResponseSchema
from api.schemas.invoices import InvoiceResponseSchema, InvoiceCreateSchema
from database import SessionDep
from invoices.creator import generate_single_invoice
from invoices.csv import create_single_csv
from invoices.pdf import create_single_pdf
from models import InvoiceModel, CustomerModel

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
)


@router.get("/", response_model=PaginationResponseSchema[InvoiceResponseSchema])
def get_invoices(
    _: ConsultantRequired,
    session: SessionDep,
    params: Annotated[PaginationParams, Depends()],
    customer_id: str,
):
    return paginate(
        session.query(InvoiceModel).filter(InvoiceModel.customer_id == customer_id),
        params,
        InvoiceResponseSchema,
    )


@router.post(
    "/",
    status_code=201,
    response_model=InvoiceResponseSchema,
    responses={404: {"description": "Customer not found"}},
)
def create_invoice(
    _: ConsultantRequired,
    session: SessionDep,
    request: InvoiceCreateSchema,
):
    customer = session.get(CustomerModel, request.customer_id)
    if customer == None:
        raise HTTPException(404, "Customer not found")
    return generate_single_invoice(session, request.month, customer)


@router.get(
    "/pdf/{invoice_id}",
    status_code=200,
    responses={404: {"description": "Invoice not found"}},
)
def get_pdf(_: ConsultantRequired, session: SessionDep, invoice_id: int):
    invoice = session.get(InvoiceModel, invoice_id)
    if invoice is None:
        raise HTTPException(404, "Invoice not found")
    out_path = create_single_pdf(session, invoice)
    return FileResponse(out_path)


@router.get(
    "/csv/{invoice_id}",
    status_code=200,
    responses={404: {"description": "Invoice not found"}},
)
def get_csv(_: ConsultantRequired, session: SessionDep, invoice_id: int):
    invoice = session.get(InvoiceModel, invoice_id)
    if invoice is None:
        raise HTTPException(404, "Invoice not found")
    out_path = create_single_csv(session, invoice)
    return FileResponse(out_path)
