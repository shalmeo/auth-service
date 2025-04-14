from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column

mapper_registry = registry()


class Base(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False)
