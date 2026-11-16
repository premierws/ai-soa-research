from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    source_kind: str
    repository_role: str | None = None
    relative_path: str | None = None
    locator: str | None = None
    schema: str | None = None
    vehicle_model: str | None = None
    version: str | None = None

    def __post_init__(self) -> None:
        values = asdict(self).values()
        if any(value and any(ord(char) < 32 for char in value) for value in values):
            raise ValueError("Source evidence must not contain control characters")
        if self.relative_path is None:
            return
        path = PurePosixPath(self.relative_path.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or not self.relative_path:
            raise ValueError("Source evidence path must be relative")
        object.__setattr__(self, "relative_path", path.as_posix())

    @classmethod
    def from_path(
        cls,
        *,
        source_kind: str,
        path: Path,
        source_root: Path,
        repository_role: str | None = None,
        locator: str | None = None,
    ) -> "SourceEvidence":
        try:
            relative_path = path.resolve().relative_to(source_root.resolve()).as_posix()
        except ValueError as error:
            raise ValueError("Source evidence path must be relative to source root") from error
        return cls(
            source_kind=source_kind,
            repository_role=repository_role,
            relative_path=relative_path,
            locator=locator,
        )

    def to_payload(self) -> dict[str, str | None]:
        return asdict(self)


def dedupe_evidence(items: list[SourceEvidence]) -> list[SourceEvidence]:
    return sorted(
        set(items),
        key=lambda item: tuple(value or "" for value in asdict(item).values()),
    )

