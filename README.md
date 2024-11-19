# UKHO Tides

This package provides a client wrapper for the [Admiralty Tidal API](https://admiraltyapi.portal.azure-api.net/) endpoints.

# Installation

Install via [pip](https://pypi.org/project/ukhotides/).

```
pip install ukhotides
```

# API Key

To call the API you will need an API key from the Admiralty Maritime Data Solutions developer portal. Follow [their guide](https://admiraltyapi.portal.azure-api.net/docs/startup) on how to do so and select one of the **UK Tidal API** products - the **Discovery** tier is free (the paid APIs have not been tested for this package).

# Usage

```python
from ukhotides import UkhoTides
from aiohttp import ClientSession

session = ClientSession()
client = UkhoTides(session, "<api_key>")

# Get all stations
stations = await client.async_get_stations()

# Get stations with name filter
stations = await client.async_get_stations("StationName")

# Get station by id
station = await client.async_get_station("0001")

# Get tidal events for station by id
events = await client.async_get_tidal_events("0001")

# Get 4 days of tidal events for station by id
events = await client.async_get_tidal_events("0001", 4)
```

There are also several premium endpoints exposed, however these are built based on the documentation and have not been tested.

```python
### Premium API Endpoints ###
### UNTESTED ###
from ukhotides import UkhoTides, ApiLevel
from aiohttp import ClientSession
from datetime import datetime

session = ClientSession()
client = UkhoTides(session, "<api_key>", ApiLevel.Premium)

# Get tidal events for a station between a given date range
start_date = datetime(2020,1,1)
end_date = datetime(2020,1,30)
events = await client.async_get_tidal_events_for_date_range("0001", start_date, end_date)

# Get tide height for a station for a given datetime
date_time = datetime(2020,1,1)
height = await client.async_get_tidal_height("0001", date_time)

# Get tide heights for a station between a given date range and at a given interval
interval_in_minutes = 60
start_date = datetime(2020,1,1)
end_date = datetime(2020,1,1,2)
heights = await client.async_get_tidal_heights("0001", start_date, end_date, interval_in_minutes)
```

# Publish to PyPi

Update the version number in `pyproject.toml` and then run:

```sh
poetry config pypi-token.pypi $PYPI_TOKEN
poetry publish --build
```

# TODO

- Better docs (sorry)
- Webhooks to automate distribution and versioning

# Attribution

Contains ADMIRALTY® Tidal Data: © Crown copyright and database right
