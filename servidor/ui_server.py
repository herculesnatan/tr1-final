import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from servidor.receiver import Receiver  # Importa a classe Receiver do outro arquivo

class ServerUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        # Layout principal
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(self.vbox)

        # Campo de texto para exibir os dados recebidos
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_buffer = self.text_view.get_buffer()

        # Scroll para o campo de texto
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)
        self.scroll.add(self.text_view)
        self.vbox.pack_start(self.scroll, True, True, 0)

        # Botão para iniciar o servidor
        self.start_button = Gtk.Button(label="Iniciar Servidor")
        self.start_button.connect("clicked", self.on_start_server)
        self.vbox.pack_start(self.start_button, False, False, 0)

        # Criação do receptor e passagem do callback para atualizar a interface
        self.receiver = Receiver(self.update_ui)

    def on_start_server(self, button):
        """Inicia o servidor em uma thread separada"""
        self.receiver.start()
        self.start_button.set_sensitive(False)
        self.add_text("Servidor iniciado...\n")

    def update_ui(self, data):
        """Atualiza a interface gráfica com os dados recebidos."""
        self.add_text(f"{data}\n")

    def add_text(self, text):
        #Adiciona texto ao campo de texto, garantindo iteradores válidos.
        # Cria uma marca no final do buffer
        end_mark = self.text_buffer.create_mark(None, self.text_buffer.get_end_iter(), False)
    
        # Insere o texto no buffer
        self.text_buffer.insert(self.text_buffer.get_end_iter(), text)
    
        # Move a visualização para o final do texto automaticamente
        self.text_view.scroll_to_mark(end_mark, 0.0, False, 0, 0)


if __name__ == "__main__":
    app = ServerUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
