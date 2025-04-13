from enum import Enum

class UserRole(str, Enum):
    patient = "patient"
    staff = "staff"
    hr = "hr"
    admin = "admin"