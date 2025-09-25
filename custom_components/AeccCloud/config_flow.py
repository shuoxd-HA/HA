import json
import hashlib
import logging

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from homeassistant.data_entry_flow import FlowResult


from .const import DOMAIN, BASE_URL 
from homeassistant.helpers.aiohttp_client import async_get_clientsession
_LOGGER = logging.getLogger(__name__)



class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1.1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    def __init__(self):
        self.data = {}
        self.family = {}
    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            try: 
                self.data = user_input
                await self._login(self.data["username"], self.md5_hash(self.data["password"]))
                return self.async_create_entry(title="Integration - Aecc ", data=self.data)
            except Exception as err:
                _LOGGER.error(f"Login error: {err}")
                errors["base"] = "Login error"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            }),
            errors=errors
        )
    def md5_hash(self, password: str) -> str:
        """Return an MD5 hash for the given password."""
        hasher = hashlib.md5()
        hasher.update(password.encode('utf-8'))
        return hasher.hexdigest()
    async def _login(self, username: str, password: str) -> bool:
        url = f"{BASE_URL}/user/login"
        session = async_get_clientsession(self.hass)
        headers = {'Content-Type': 'application/json'}
        req = {"email": username, "password": password, "phoneOs": 1, "phoneModel": "1.1", "appVersion": "V1.1"}
        json_data = json.dumps(req)

        async with session.post(url, headers=headers, data=json_data) as resp:
            if resp.status == 200:
                token = await resp.json()
                if token['obj'] is None:
                    raise Exception("Failed to login")
                session.cookie_jar.update_cookies(resp.cookies)
                return True
            else:
                raise Exception("Failed to login")


