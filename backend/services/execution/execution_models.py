from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineField:
    label: str
    value: Any


@dataclass
class PipelineStep:
    id: str
    title: str
    icon: str
    status: str = "waiting"
    expandable: bool = True
    fields: list[PipelineField] = field(default_factory=list)


@dataclass
class PipelineHeader:
    session: str
    provider: str
    model: str
    latency: float | None = None


@dataclass
class Pipeline:
    header: PipelineHeader
    steps: list[PipelineStep]
