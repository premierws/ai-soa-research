from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ServiceInstance(Base):
    __tablename__ = "service_instances"

    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id"))
    application_id: Mapped[int | None] = mapped_column(ForeignKey("applications.id"))
    service_package: Mapped[str] = mapped_column(String(255))
    service_name: Mapped[str] = mapped_column(String(255))
    service_instance_name: Mapped[str] = mapped_column(String(255))
    source_kind: Mapped[str] = mapped_column(String(32))
