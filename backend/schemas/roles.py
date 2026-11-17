from datetime import datetime
from uuid import UUID
from pydantic import Field
from .common import Schema, UUIDRead

class RoleCreate(Schema):
    name: str = Field(min_length=1, max_length=50)
    description: str

class RoleRead(RoleCreate, UUIDRead):
    pass

class RoleAssign(Schema):
    role_id: UUID

class RoleHistoryRead(UUIDRead):
    user_id: UUID
    role_id: UUID
    assigned_at: datetime
    assigned_by: UUID
    previous_assignment_id: UUID | None
