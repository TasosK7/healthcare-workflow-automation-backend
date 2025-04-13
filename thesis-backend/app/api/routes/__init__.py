from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .department import router as department_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(department_router, prefix="/departments", tags=["Departments"])