# sidebar.py

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/com/jeffser/Nocturne/pages/sidebar.ui')
class MainSidebar(Adw.NavigationPage):
    __gtype_name__ = 'NocturneMainSidebar'

    main_sidebar = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        list(list(self.main_sidebar)[0])[0].get_child().set_margin_bottom(75)
