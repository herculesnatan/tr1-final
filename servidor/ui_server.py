import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango
from servidor.receiver import Receiver  # Sua classe existente

class ServerUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # HeaderBar 
        header = Gtk.HeaderBar(title="Servidor de Recepção")
        header.set_subtitle("Monitor de mensagens recebidas")
        header.set_show_close_button(True)
        self.set_titlebar(header)

        # Layout principal
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(self.vbox)

        # Campo de texto com estilo
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_left_margin(10)
        self.text_view.set_right_margin(10)

        monospace = Pango.FontDescription("Monospace 12")
        self.text_view.modify_font(monospace)

        self.text_view.modify_base(Gtk.StateType.NORMAL, Gdk.color_parse("#f9f9f9"))
        self.text_view.modify_text(Gtk.StateType.NORMAL, Gdk.color_parse("#333333"))

        self.text_buffer = self.text_view.get_buffer()

        # Scroll automático para o TextView
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        self.scroll.add(self.text_view)
        self.vbox.pack_start(self.scroll, True, True, 0)

        # Botão de iniciar servidor
        self.start_button = Gtk.Button(label="🚀 Iniciar Servidor")
        self.start_button.connect("clicked", self.on_start_server)
        self.start_button.set_hexpand(True)  # Ocupa toda a largura
        self.vbox.pack_start(self.start_button, False, False, 0)

        # Receptor
        self.receiver = Receiver(self.update_ui)

    def on_start_server(self, button):
        self.receiver.start()
        self.start_button.set_sensitive(False)
        self.add_text("✅ Servidor iniciado...\n")

    def update_ui(self, data):
        self.add_text(f"{data}\n")

    def add_text(self, text):
        end_mark = self.text_buffer.create_mark(None, self.text_buffer.get_end_iter(), False)
        self.text_buffer.insert(self.text_buffer.get_end_iter(), text)
        self.text_view.scroll_to_mark(end_mark, 0.0, False, 0, 0)

if __name__ == "__main__":
    app = ServerUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
