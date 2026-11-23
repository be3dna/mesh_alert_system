from datetime import UTC, datetime
from uuid import UUID

from core.exceptions import NodeNotFoundError
from models.node import Node
from repositories.interfaces.node import INodeRepository
from repositories.pagination import Page, Pagination
from schemas.nodes import NodeCreate, NodeUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class NodeService:
    """Manage nodes within the caller's unit of work."""

    def __init__(self, repository: INodeRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def register_node(self, data: NodeCreate) -> Node: ##TODO: check permission to register in controller
        
        return await self.repository.add(Node(**data.model_dump()))

    async def get_node(self, node_id: UUID) -> Node:
        node = await self.repository.get_by_id(node_id)
        if node is None:
            raise NodeNotFoundError(node_id)
        return node

    async def get_nodes(self, pagination: Pagination | None = None) -> Page[Node]:
        return await self.repository.get_all(pagination or Pagination())

    async def update_node(self, node_id: UUID, data: NodeUpdate) -> Node:##TODO: check permission to update in controller
        async with self.session.begin():
            node = await self.get_node(node_id)
            for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
                setattr(node, field, value)
            await self.session.flush()
        return node

    async def update_status(self, node_id: UUID, status_id: UUID) -> None:##TODO: check permission to update in controller
        async with self.session.begin():
            node = await self.get_node(node_id)
            node.status_id = status_id
            await self.session.flush()

    async def register_heartbeat(self, node_id: UUID) -> None:##TODO: check permission to update in controller
        async with self.session.begin():
            node = await self.get_node(node_id)
            node.last_seen_at = datetime.now(UTC)
            await self.session.flush()
