from servidor.ui_server import ServerUI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == "__main__":
    app = ServerUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
