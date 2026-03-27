# jellyfin.py

from gi.repository import Gtk, GLib, GObject, Gdk, Gio, GdkPixbuf
from . import secret, models
from ..constants import get_pc_name
from .base import Base
import requests, subprocess

class Jellyfin(Base):
    __gtype_name__ = 'NocturneIntegrationJellyfin'

    login_page_metadata = {
        'icon-name': "music-note-symbolic",
        'title': "Jellyfin",
        'entries': ["url", "user", "password"]
    }
    button_metadata = {
        'title': "Jellyfin",
        'subtitle': _("Use an existing Jellyfin instance")
    }
    url = GObject.Property(type=str)
    user = GObject.Property(type=str)

    AUTH_HEADER = 'MediaBrowser Client="Nocturne", Device="{}", DeviceId="{}", Version="1.0.0"'.format(get_pc_name(), '1234')

    # Loaded by API
    accessToken = GObject.Property(type=str)
    userId = GObject.Property(type=str)

    def get_base_params(self) -> dict:
        #TODO
        return {}

    def get_url(self, action:str) -> str:
        return '{}/{}'.format(self.get_property('url').strip('/'), action)

    def make_request(self, action:str, json:dict={}, params:dict={}, mode:str="GET") -> dict:
        params = {
            **self.get_base_params(),
            **params
        }
        try:
            if mode == 'GET':
                response = requests.get(
                    self.get_url(action),
                    params=params,
                    json=json,
                    headers={"X-Emby-Authorization": self.AUTH_HEADER}
                )
            elif mode == 'POST':
                response = requests.post(
                    self.get_url(action),
                    params=params,
                    json=json,
                    headers={"X-Emby-Authorization": self.AUTH_HEADER}
                )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            pass
        return {}

    # ----------- #

    def start_instance(self) -> bool:
        return True

    def terminate_instance(self):
        pass

    def on_login(self):
        pass

    def get_stream_url(self, song_id:str) -> str:
        return self.get_url('/Audio/{}/stream'.format(song_id))

    def getCoverArt(self, id:str=None) -> tuple:
        #TODO
        return None, None

    def ping(self) -> bool:
        response = self.make_request(
            action='Users/AuthenticateByName',
            json={
                'Username': self.get_property('user'),
                'Pw': secret.get_plain_password()
            },
            mode='POST'
        )
        self.set_property('accessToken', response.get('AccessToken'))
        self.set_property('userId', response.get('User', {}).get('Id'))
        return self.get_property('accessToken') and self.get_property('userId')
