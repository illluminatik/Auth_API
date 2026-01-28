from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Model

class BlacklistedToken(Model):
    __tablename__ = "blacklisted_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())

class BusinessElement(Model):
    __tablename__ = "business_elements"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

class AccessRule(Model):
    __tablename__ = "access_rules"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    element_id = Column(Integer, ForeignKey("business_elements.id"), nullable=False)
    can_read = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    role = relationship("Role")
    element = relationship("BusinessElement")
