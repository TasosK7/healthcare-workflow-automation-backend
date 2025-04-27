from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .department import router as department_router
from .staff import router as staff_router
from .patient import router as patient_router
from .shift import router as shift_router
from .appointment import router as appointment_router
from .surgery import router as surgery_router
from .lab_test import router as lab_test_router
from .special_care_assignment import router as special_care_assignment_router


router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(department_router, prefix="/departments", tags=["Departments"])
router.include_router(staff_router, prefix="/staff", tags=["Staff"])
router.include_router(patient_router, prefix="/patients", tags=["Patients"])
router.include_router(shift_router, prefix="/shifts", tags=["Shifts"])
router.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
router.include_router(surgery_router, prefix="/surgeries", tags=["Surgeries"])
router.include_router(lab_test_router, prefix="/lab-tests", tags=["Lab Tests"])
router.include_router(special_care_assignment_router, prefix="/special-care-assignments", tags=["Special Care"])





