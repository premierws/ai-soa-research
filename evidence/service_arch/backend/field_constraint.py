from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class FieldConstraint(Base):
    __tablename__ = "field_constraints"

    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("snapshots.id"))
    field_fqn: Mapped[str] = mapped_column(String(512))
    constraint_type: Mapped[str] = mapped_column(String(255))
    constraint_value: Mapped[str] = mapped_column(String(255))
    source_options_file: Mapped[str | None] = mapped_column(String(1024))
