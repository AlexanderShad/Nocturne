# downloads_queue_button.py

from gi.repository import Gtk, Adw, Gio

@Gtk.Template(resource_path='/com/jeffser/Nocturne/containers/downloads_queue_button.ui')
class DownloadsQueueButton(Gtk.MenuButton):
    __gtype_name__ = 'NocturneDownloadsQueueButton'

    
