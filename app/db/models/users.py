from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.cors.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    profile = relationship("Profile", back_populates='owner', uselist=False)


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    followers = Column(Integer, nullable=False)
    bio = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete="SET NULL"), nullable=False)
    owner = relationship('User', back_populates='profile')
