from sqlalchemy.orm import Mapped, relationship

from models.alert import Alert
from models.base import Base


class Territory(Base):
    __tablename__="territories"
    
    
    
    
    
    
    
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="territory"
    )