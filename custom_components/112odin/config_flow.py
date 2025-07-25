import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_BEREDSKAB_ID, CONF_STATION_NAME, CONF_MAX_EVENTS

BREDESKABER = {
    "101": "Station Nord",
    "102": "Station Syd",
    "103": "Station Øst",
    "104": "Station Vest"
}

class OdinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default="112 Odin"): str,
                vol.Required(CONF_BEREDSKAB_ID, default="101"): vol.In(BREDESKABER),
                vol.Required(CONF_STATION_NAME, default="Station Nord"): vol.In(list(BREDESKABER.values())),
                vol.Optional(CONF_MAX_EVENTS, default=5): vol.All(vol.Coerce(int), vol.Range(min=1, max=20)),
            }),
            errors=errors,
        )
