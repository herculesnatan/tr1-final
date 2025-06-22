from cliente.ui_client import ClientUI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == "__main__":
    app = ClientUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
