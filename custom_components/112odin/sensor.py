import logging
import voluptuous as vol
import feedparser
from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_BEREDSKAB_ID = "beredskabsID"
CONF_STATION_NAME = "stations_navn"
CONF_MAX_EVENTS = "antal_haendelser"

DEFAULT_NAME = "112 Odin"
DEFAULT_MAX_EVENTS = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_BEREDSKAB_ID): cv.string,
    vol.Optional(CONF_STATION_NAME, default=""): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_MAX_EVENTS, default=DEFAULT_MAX_EVENTS): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=20)
    ),
})

SCAN_INTERVAL = timedelta(minutes=10)

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    beredskabs_id = config.get(CONF_BEREDSKAB_ID)
    station_navn = config.get(CONF_STATION_NAME)
    antal = config.get(CONF_MAX_EVENTS)

    url = f"http://www.odin.dk/RSS/RSS.aspx?beredskabsID={beredskabs_id}"
    add_entities([Odin112Sensor(name, url, station_navn, antal)], True)

class Odin112Sensor(Entity):
    def __init__(self, name, url, station_navn, max_events):
        self._name = name
        self._url = url
        self._station_navn = station_navn
        self._max_events = max_events
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"112odin_{self._station_navn}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        _LOGGER.debug("Henter ODIN data fra %s", self._url)
        feed = feedparser.parse(self._url)
        entries = feed.entries[:self._max_events]
        self._state = len(entries)
        self._attributes = {
            f"event_{i+1}": {
                "title": entry.title,
                "summary": entry.summary,
                "published": entry.published,
            }
            for i, entry in enumerate(entries)
        }
