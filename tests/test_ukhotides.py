"""Tests for the API client."""
import pytest
import json

from aiohttp import ClientSession
from ukhotides import UkhoTides, TidalEvent, TidalHeight, Station, ApiError, InvalidApiKeyError, ApiQuotaExceededError, TooManyRequestsError, StationNotFoundError, ApiLevel
from http import HTTPStatus
from aioresponses import aioresponses
from datetime import datetime

@pytest.fixture
def mock_session():
    """Mocked ClientSession"""
    with aioresponses() as m:
        yield m

@pytest.fixture
def mock_stations_data():
    """Example response from stations API"""
    with open("resources/stations.json") as f:
        return json.load(f)

@pytest.fixture
def mock_station_data():
    """Example response from station API"""
    with open("resources/station.json") as f:
        return json.load(f)

@pytest.fixture
def mock_tidal_events_data():
    """Example response from tidal events API"""
    with open("resources/tidal_events.json") as f:
        return json.load(f)
        
@pytest.fixture
def mock_height_data():
    """Example response from tidal height API"""
    with open("resources/height.json") as f:
        return json.load(f)
        
@pytest.fixture
def mock_heights_data():
    """Example response from tidal heights API"""
    with open("resources/heights.json") as f:
        return json.load(f)

# Station
@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestStation_thenReturnStation(mock_session, mock_station_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_station_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)
    station = await client.async_get_station("0001")
    
    assert station == Station.from_dict(mock_station_data)

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001", ApiLevel.Premium)
])
async def test_givenInvalidApiKey_whenRequestStation_thenThrowInvalidApiKeyError(mock_session, mock_station_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.UNAUTHORIZED)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    with pytest.raises(InvalidApiKeyError):
        station = await client.async_get_station("0001")

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001", ApiLevel.Premium)
])
async def test_givenQuotaExceeded_whenRequestStation_thenThrowApiQuotaExceededError(mock_session, mock_station_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.FORBIDDEN)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    with pytest.raises(ApiQuotaExceededError):
        station = await client.async_get_station("0001")

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001", ApiLevel.Premium)
])
async def test_givenTooManyRequests_whenRequestStation_thenThrowTooManyRequestsError(mock_session, mock_station_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.TOO_MANY_REQUESTS)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    with pytest.raises(TooManyRequestsError):
        station = await client.async_get_station("0001")

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestBogusStation_thenThrowStationNotFound(mock_session, mock_station_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.NOT_FOUND)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    with pytest.raises(StationNotFoundError):
        station = await client.async_get_station("0001")

# Stations
@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestStations_thenReturnStations(mock_session, mock_stations_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_stations_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)
    stations = await client.async_get_stations()

    mock_stations = [Station.from_dict(s) for s in mock_stations_data["features"]]
    
    assert stations == mock_stations

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations?name=StationName", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations?name=StationName", ApiLevel.Foundation),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations?name=StationName", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestStationsWithName_thenReturnStations(mock_session, mock_stations_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_stations_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)
    stations = await client.async_get_stations("StationName")

    mock_stations = [Station.from_dict(s) for s in mock_stations_data["features"]]
    
    assert stations == mock_stations

# Tidal Events
@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001/TidalEvents", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001/TidalEvents", ApiLevel.Foundation)
])
async def test_givenValidApiKey_whenRequestTidalEvents_thenReturnTidalEvents(mock_session, mock_tidal_events_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_tidal_events_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)
    events = await client.async_get_tidal_events("0001")

    mock_events = [TidalEvent.from_dict(e) for e in mock_tidal_events_data]
    
    assert events == mock_events

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001/TidalEvents?duration=4", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001/TidalEvents?duration=4", ApiLevel.Foundation)
])
async def test_givenValidApiKey_whenRequestTidalEventsWithDuration_thenReturnTidalEvents(mock_session, mock_tidal_events_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_tidal_events_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)
    events = await client.async_get_tidal_events("0001", 4)

    mock_events = [TidalEvent.from_dict(e) for e in mock_tidal_events_data]
    
    assert events == mock_events

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0001/TidalEvents?duration=20", ApiLevel.Discovery),
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-foundation/api/V2/Stations/0001/TidalEvents?duration=20", ApiLevel.Foundation)
])
async def test_givenValidApiKey_whenRequestTidalEventsWithInvalidDuration_thenThrowApiError(mock_session, mock_tidal_events_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.BAD_REQUEST,
        payload=mock_tidal_events_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    with pytest.raises(ApiError):
        events = await client.async_get_tidal_events("0001", 20)

# Premium
# Tidal Events
@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001/TidalEventsForDateRange?StartDate=2020-01-01 00:00:00&EndDate=2020-01-30", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestTidalEventsForDateRange_thenReturnTidalEvents(mock_session, mock_tidal_events_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_tidal_events_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    start_date = datetime(2020,1,1)
    end_date = datetime(2020,1,30)
    events = await client.async_get_tidal_events_for_date_range("0001", start_date, end_date)

    mock_events = [TidalEvent.from_dict(e) for e in mock_tidal_events_data]
    
    assert events == mock_events

# Tidal Height
@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001/TidalHeight?DateTime=2020-01-01 00:00:00", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestTidalHeight_thenReturnTidalHeight(mock_session, mock_height_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_height_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    date_time = datetime(2020,1,1)
    height = await client.async_get_tidal_height("0001", date_time)

    assert height == mock_height_data["Height"]

@pytest.mark.parametrize("url, level",[
    pytest.param("https://admiraltyapi.azure-api.net/uktidalapi-premium/api/V2/Stations/0001/TidalHeights?StartDateTime=2020-01-01 00:00:00&EndDateTime=2020-01-01 02:00:00&IntervalInMinutes=60", ApiLevel.Premium)
])
async def test_givenValidApiKey_whenRequestTidalHeights_thenReturnTidalHeights(mock_session, mock_heights_data, url, level):
    mock_session.get(
        url=url,
        status=HTTPStatus.OK,
        payload=mock_heights_data)

    session = ClientSession()
    client = UkhoTides(session, "api_key", level)

    start_date = datetime(2020,1,1)
    end_date = datetime(2020,1,1,2)
    heights = await client.async_get_tidal_heights("0001", start_date, end_date, 60)

    mock_heights = [TidalHeight.from_dict(h) for h in mock_heights_data]

    assert heights == mock_heights