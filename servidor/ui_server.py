import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango
from servidor.receiver import Receiver
from gi.repository import GLib

class ServerUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # HeaderBar 
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)

        # Título à esquerda com fonte robusta
        title_label = Gtk.Label()
        title_label.set_markup('<span font="18" weight="bold" foreground="#333">Servidor de recepção</span>')
        title_label.set_xalign(0.0)
        header.pack_start(title_label)

        # Subtítulo à direita
        subtitle_label = Gtk.Label()
        subtitle_label.set_markup('<span font="10" weight="semi-bold" foreground="#666">Terminal</span>')
        subtitle_label.set_xalign(1.0)
        header.pack_end(subtitle_label)

        self.set_titlebar(header)

        # Layout principal
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(self.vbox)

        # Campo de texto com estilo (não adicionado ainda)
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_left_margin(10)
        self.text_view.set_right_margin(10)
        monospace = Pango.FontDescription("Monospace 12")
        self.text_view.modify_font(monospace)

        # CSS para fundo cinza
        css = b"""
        textview, textview text, scrolledwindow {
            background: #e0e0e0;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.text_buffer = self.text_view.get_buffer()

        # Scroll automático para o TextView (não adicionado ainda)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)
        self.scroll.add(self.text_view)
        # NÃO adicione self.vbox.pack_start(self.scroll, ...) aqui!

        # Botão de iniciar servidor
        self.start_button = Gtk.Button(label="🚀 Iniciar Servidor")
        self.start_button.connect("clicked", self.on_start_server)
        self.start_button.set_hexpand(True)
        self.vbox.pack_start(self.start_button, False, False, 0)

        # Receptor
        self.receiver = Receiver(self.update_ui)

    def on_start_server(self, button):
        # Só agora adiciona o campo de texto ao layout
        self.vbox.pack_start(self.scroll, True, True, 0)
        self.show_all()
        self.receiver.start()
        self.start_button.set_label("✅ Servidor em execução")
        self.start_button.set_sensitive(False)
        self.add_text("✅ Servidor iniciado!\n")
        self.add_text("- Aguardando conexão...\n")

    def update_ui(self, data):
        GLib.idle_add(self.add_text, f"{data}\n")

    def add_text(self, text):
        end_mark = self.text_buffer.create_mark(None, self.text_buffer.get_end_iter(), False)
        self.text_buffer.insert(self.text_buffer.get_end_iter(), text)
        self.text_view.scroll_to_mark(end_mark, 0.0, False, 0, 0)

if __name__ == "__main__":
    app = ServerUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
