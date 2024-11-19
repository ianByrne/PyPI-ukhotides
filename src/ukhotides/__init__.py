"""Client for the UKHO Tides API"""

# pylint: disable=line-too-long

import logging
from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

from aiohttp import ClientSession

from .const import (
    BASE_ENDPOINT,
    DISCOVERY_ENDPOINT,
    FOUNDATION_ENDPOINT,
    PREMIUM_ENDPOINT,
)
from .dataclasses import Station, TidalEvent, TidalHeight
from .enums import ApiLevel
from .exceptions import (
    ApiError,
    ApiQuotaExceededError,
    InvalidApiKeyError,
    StationNotFoundError,
    TooManyRequestsError,
)

_LOGGER = logging.getLogger(__name__)


class UkhoTides:
    """UKHO Tides"""

    def __init__(self, session: ClientSession, api_key: str, api_level: ApiLevel = ApiLevel.Discovery):
        self._session = session
        self._api_key = api_key
        self._api_level = api_level

        if api_level == ApiLevel.Foundation:
            self._base_url = BASE_ENDPOINT + FOUNDATION_ENDPOINT
        elif api_level == ApiLevel.Premium:
            self._base_url = BASE_ENDPOINT + PREMIUM_ENDPOINT
        else:
            self._base_url = BASE_ENDPOINT + DISCOVERY_ENDPOINT

    async def _async_get_data(self, url: str):
        async with self._session.get(
            url, headers={"Ocp-Apim-Subscription-Key": self._api_key}
        ) as resp:
            if resp.status == HTTPStatus.UNAUTHORIZED:
                raise InvalidApiKeyError("Invalid API key")
            if resp.status == HTTPStatus.FORBIDDEN:
                raise ApiQuotaExceededError("API quota exceeded")
            if resp.status == HTTPStatus.TOO_MANY_REQUESTS:
                raise TooManyRequestsError("Too many API requests")
            if resp.status == HTTPStatus.NOT_FOUND:
                raise StationNotFoundError("Station not found")
            if resp.status != HTTPStatus.OK:
                raise ApiError(f"Invalid response from API: {resp.status}")

            _LOGGER.debug("Data retrieved from %s, status: %s",
                          url, resp.status)

            return await resp.json()

    async def async_get_stations(self, name: Optional[str] = None) -> List[Station]:
        """Return all stations, filtered by name"""
        url = self._base_url

        if name is not None:
            url = url + "?name=" + name

        data = await self._async_get_data(url)

        return [Station.from_dict(s) for s in data["features"]]

    async def async_get_station(self, station_id: str) -> Station:
        """Return a station by ID"""
        url = self._base_url + "/" + station_id
        data = await self._async_get_data(url)
        return Station.from_dict(data)

    async def async_get_tidal_events(self, station_id: str, duration: Optional[int] = None) -> List[TidalEvent]:
        """Return all tidal events for a station, filtered by duration"""
        url = self._base_url + "/" + station_id + "/TidalEvents"

        if duration is not None:
            url = url + "?duration=" + str(duration)

        data = await self._async_get_data(url)
        events = [TidalEvent.from_dict(e) for e in data]

        return [e for e in events if e is not None]

    async def async_get_tidal_events_for_date_range(self, station_id: str, start_date: datetime, end_date: datetime) -> List[TidalEvent]:
        """Return all tidal events for a station, filtered by date range. Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalEventsForDateRange?"
        url = url + "StartDate=" + start_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&EndDate=" + end_date.strftime("%Y-%m-%d")

        data = await self._async_get_data(url)
        events = [TidalEvent.from_dict(e) for e in data]

        return [e for e in events if e is not None]

    async def async_get_tidal_height(self, station_id: str, date_time: datetime) -> float:
        """Return the tidal height for a station at a given datetime. Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalHeight?"
        url = url + "DateTime=" + date_time.strftime("%Y-%m-%d %H:%M:%S")

        data = await self._async_get_data(url)

        return data["Height"]

    async def async_get_tidal_heights(self, station_id: str, start_date: datetime, end_date: datetime, interval: int) -> list[TidalHeight]:
        """Return the tidal heights for a station between a date range. Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalHeights?"
        url = url + "StartDateTime=" + start_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&EndDateTime=" + end_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&IntervalInMinutes=" + str(interval)

        data = await self._async_get_data(url)
        heights = [TidalHeight.from_dict(h) for h in data]

        return [h for h in heights if h is not None]
