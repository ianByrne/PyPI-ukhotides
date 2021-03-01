import json
import logging

from aiohttp import ClientSession
from http import HTTPStatus
from datetime import datetime
from typing import List

from .const import BASE_ENDPOINT, DISCOVERY_ENDPOINT, FOUNDATION_ENDPOINT, PREMIUM_ENDPOINT
from .dataclasses import Station, TidalEvent, TidalHeight
from .enums import ApiLevel
from .exceptions import ApiError, InvalidApiKeyError, ApiQuotaExceededError, TooManyRequestsError, StationNotFoundError

_LOGGER = logging.getLogger(__name__)


class UkhoTides:
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
            
            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            
            return await resp.json()

    async def async_get_stations(self, name: str = None) -> List[Station]:
        url = self._base_url

        if name is not None:
            url = url + "?name=" + name

        data = await self._async_get_data(url)
        
        return [Station.from_dict(s) for s in data["features"]]

    async def async_get_station(self, station_id: str) -> Station:
        url = self._base_url + "/" + station_id
        data = await self._async_get_data(url)
        return Station.from_dict(data)

    async def async_get_tidal_events(self, station_id: str, duration: int = None) -> List[TidalEvent]:
        url = self._base_url + "/" + station_id + "/TidalEvents"

        if duration is not None:
            url = url + "?duration=" + str(duration)

        data = await self._async_get_data(url)

        return [TidalEvent.from_dict(e) for e in data]
        
    async def async_get_tidal_events_for_date_range(self, station_id: str, start_date: datetime, end_date: datetime) -> List[TidalEvent]:
        """Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalEventsForDateRange?"
        url = url + "StartDate=" + start_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&EndDate=" + end_date.strftime("%Y-%m-%d")

        data = await self._async_get_data(url)

        return [TidalEvent.from_dict(e) for e in data]

    async def async_get_tidal_height(self, station_id: str, date_time: datetime) -> float:
        """Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalHeight?"
        url = url + "DateTime=" + date_time.strftime("%Y-%m-%d %H:%M:%S")

        data = await self._async_get_data(url)

        return data["Height"]

    async def async_get_tidal_heights(self, station_id: str, start_date: datetime, end_date: datetime, interval: int) -> float:
        """Only available for premium subscriptions"""

        url = self._base_url + "/" + station_id + "/TidalHeights?"
        url = url + "StartDateTime=" + start_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&EndDateTime=" + end_date.strftime("%Y-%m-%d %H:%M:%S")
        url = url + "&IntervalInMinutes=" + str(interval)

        data = await self._async_get_data(url)

        return [TidalHeight.from_dict(h) for h in data]