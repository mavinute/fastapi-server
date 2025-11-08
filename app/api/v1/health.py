from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/", summary="Health Check")
async def health_check():
    return {"status": "Ok", "service": "Servidor em funcionamento"}
