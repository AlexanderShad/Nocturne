# carousel.py

from gi.repository import Gtk, Adw, GLib

@Gtk.Template(resource_path='/com/jeffser/Nocturne/containers/carousel.ui')
class Carousel(Gtk.Box):
    __gtype_name__ = 'NocturneCarousel'

    header_button = Gtk.Template.Child()
    list_el = Gtk.Template.Child()

    def set_header(self, label:str, icon_name:str, action_name:str=None):
        self.header_button.set_tooltip_text(label)
        self.header_button.get_child().set_label(label)
        self.header_button.get_child().set_icon_name(icon_name)
        self.header_button.set_action_name(action_name)
        self.header_button.set_sensitive(bool(action_name))

    def remove_all(self):
        for page in list(self.list_el):
            self.list_el.remove(page)

    def set_widgets(self, widgets:list):
        GLib.idle_add(self.set_visible, len(widgets) > 0)
        if self.list_el.get_n_pages() > 0:
            GLib.idle_add(self.remove_all)
        for page in widgets:
            GLib.idle_add(self.list_el.append, page)
