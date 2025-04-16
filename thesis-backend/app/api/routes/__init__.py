from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .department import router as department_router
from .staff import router as staff_router
from .patient import router as patient_router
from .shift import router as shift_router
from .appointment import router as appointment_router
from .surgery import router as surgery_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(department_router, prefix="/departments", tags=["Departments"])
router.include_router(staff_router, prefix="/staff", tags=["Staff"])
router.include_router(patient_router, prefix="/patients", tags=["Patients"])
router.include_router(shift_router, prefix="/shifts", tags=["Shifts"])
router.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
router.include_router(surgery_router, prefix="/surgeries", tags=["Surgeries"])



