from datetime import datetime
from uuid import UUID
from pydantic import Field
from .common import Schema, UUIDRead

class ReferenceCategoryCreate(Schema):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None

class ReferenceCategoryRead(ReferenceCategoryCreate, UUIDRead):
    pass

class AccessGroupCreate(Schema):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = None

class AccessGroupRead(UUIDRead):
    name: str
    # Existing database column is misspelled: describtion
    describtion: str | None

class AccessGroupRoleRead(UUIDRead):
    access_group_id: UUID
    role_id: UUID

class ReferenceArticleCreate(Schema):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    category_id: UUID
    access_group: UUID

class ReferenceArticleUpdate(Schema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)
    category_id: UUID | None = None
    access_group: UUID | None = None

class ReferenceArticleRead(ReferenceArticleCreate, UUIDRead):
    created_at: datetime
    updated_at: datetime
    author_id: UUID
    editor_id: UUID | None
