# context.py

from gi.repository import Gtk, Adw, GLib, Gio

class ContextButton(Gtk.Button):
    __gtype_name__ = 'NocturneContextButton'

    def __init__(self, name:str, icon_name:str, css:list, connect_style:bool):
        super().__init__(
            css_classes=css,
            child=Adw.ButtonContent(
                label=name,
                icon_name=icon_name,
                halign=Gtk.Align.FILL if connect_style else Gtk.Align.START
            ),
            tooltip_text=name
        )
        if connect_style:
            self.settings = Gio.Settings(schema_id="com.jeffser.Nocturne")
            self.settings.connect('changed::show-context-button-label', self.label_visibility_toggled)
            self.label_visibility_toggled(self.settings, 'show-context-button-label')

    def label_visibility_toggled(self, settings, key):
        labelVisible = settings.get_value(key).unpack()
        label = list(list(self.get_child())[0])[1]
        label.set_visible(labelVisible)
        if labelVisible:
            self.remove_css_class('circular')
            self.remove_css_class('flat')
        else:
            self.add_css_class('circular')
            self.add_css_class('flat')

def get_context_buttons_list(options:dict, model_id:str, cb_handler:callable=None, connect_style:bool=True) -> list:
    if cb_handler is None:
        cb_handler = lambda btn, callback: callback() if callback else None
    buttons = []
    for data in options.values():
        btn = ContextButton(data.get('name', ""), data.get('icon-name', ""), data.get('css', []), connect_style)
        if data.get('sensitive', True):
            btn.connect('clicked', cb_handler, data.get('connection'))
        if data.get('action-name') and data.get('sensitive', True):
            btn.set_action_name(data.get('action-name'))
            if data.get('action-target'):
                btn.set_action_target_value(GLib.Variant.new_string(data.get('action-target')))
            elif model_id:
                btn.set_action_target_value(GLib.Variant.new_string(model_id))
        btn.set_sensitive(data.get('sensitive', True))
        buttons.append(btn)
    return buttons

class ContextContainer(Gtk.Box):
    __gtype_name__ = 'NocturneContextContainer'

    def __init__(self, options:dict, model_id:str):
        #options:
        #name : {
        #   icon-name:str
        #   css:list
        #   connection:callable
        #   action-name:str
        #   action-target:str
        #   sensitive:bool
        #}

        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )
        buttons = get_context_buttons_list(options, model_id, cb_handler=self.callback_handler, connect_style=False)
        for btn in buttons:
            btn.add_css_class('flat')
            btn.set_tooltip_text('')
            self.append(btn)

    def callback_handler(self, button, callback):
        popover = button.get_ancestor(Gtk.Popover)
        if popover:
            popover.popdown()
        if callback:
            callback()
        
