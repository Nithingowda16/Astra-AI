from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.copilot import CopilotQueryRequest, CopilotQueryResponse
from backend.app.copilot.copilot_service import CopilotService

router = APIRouter(prefix="/copilot", tags=["Copilot"])

@router.post("/query", response_model=CopilotQueryResponse)
def query_copilot(req: CopilotQueryRequest, db: Session = Depends(get_db)):
    result = CopilotService.process_query(
        query=req.query,
        db=db,
        context_customer_id=req.context_customer_id,
        context_transaction_id=req.context_transaction_id
    )
    return CopilotQueryResponse(**result)
