"""Data classes"""

# pylint: disable=missing-function-docstring

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Station:
    """UKHO Station"""

    id: str
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> Station:
        return cls(
            id = data["properties"]["Id"],
            name = data["properties"]["Name"],
        )

@dataclass
class TidalEvent:
    """UKHO Tidal Event"""

    event_type: str
    date_time: str
    height: float

    @classmethod
    def from_dict(cls, data: dict) -> TidalEvent | None:
        try:
            return cls(
                event_type = data["EventType"],
                date_time = data["DateTime"],
                height = data["Height"],
            )
        except KeyError:
            return None


@dataclass
class TidalHeight:
    """UKHO Tidal Height"""

    date_time: str
    height: float

    @classmethod
    def from_dict(cls, data: dict) -> TidalHeight | None:
        try:
            return cls(
                date_time = data["DateTime"],
                height = data["Height"],
            )
        except KeyError:
            return None
