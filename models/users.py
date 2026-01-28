from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Model
import bcrypt

user_role = Table(
    'user_role', Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class Role(Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("Users", secondary=user_role, back_populates="roles")

class Users(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    middle_name = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    roles = relationship("Role", secondary=user_role, back_populates="users", lazy="selectin")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
