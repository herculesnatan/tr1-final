import gi
gi.require_version("Gtk", "3.0")
import matplotlib.pyplot as plt
from gi.repository import Gtk, Gdk, Pango
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from cliente.transmitter import Transmitter
import numpy as np
from camada_enlace.enquadramento import contagem_caracteres, insercao_bytes
from camada_enlace.deteccao_erros import bit_paridade, crc
from camada_enlace.hamming import hamming_encode

class ClientUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmissor")
        self.set_border_width(10)
        self.set_default_size(900, 700)

        self.transmitter = Transmitter()
        self.username = None
        self.show_name_dialog()

        # HeaderBar 
        header = Gtk.HeaderBar(title="Transmissor de Dados")
        header.set_subtitle("Envio e visualização de sinais")
        header.set_show_close_button(True)
        self.set_titlebar(header)

        # Layout principal
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

        # Entrada de texto
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite o texto para transmitir")
        self.entry.set_margin_bottom(5)
        self.entry.set_margin_top(5)
        self.vbox.pack_start(self.entry, False, False, 0)

        # Configurações (agrupadas)
        config_box = Gtk.Box(spacing=10)
        self.vbox.pack_start(config_box, False, False, 0)

        self.modulation_combo = self.create_combo("Modulação Digital", ["NRZ", "Manchester", "Bipolar"])
        config_box.pack_start(self.modulation_combo, True, True, 0)

        self.carrier_modulation_combo = self.create_combo("Modulação por Portadora", ["ASK", "FSK", "8QAM"])
        config_box.pack_start(self.carrier_modulation_combo, True, True, 0)

        self.framing_combo = self.create_combo("Enquadramento", ["Contagem de caracteres", "Inserção de bytes"])
        config_box.pack_start(self.framing_combo, True, True, 0)

        self.error_detection_combo = self.create_combo("Detecção de Erros", ["Bit de paridade par", "CRC"])
        config_box.pack_start(self.error_detection_combo, True, True, 0)

        # Botão de transmissão
        self.transmit_button = Gtk.Button(label="🚀 Transmitir")
        self.transmit_button.connect("clicked", self.on_transmit_clicked)
        self.vbox.pack_start(self.transmit_button, False, False, 0)

        # Área de saída de texto
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_height(160)
        self.scrolled_window.set_hexpand(True)

        self.output_label = Gtk.Label()
        self.output_label.set_line_wrap(True)
        self.output_label.set_xalign(0)

        # Fonte monoespaçada para bits e dados
        monospace = Pango.FontDescription("Monospace 11")
        self.output_label.modify_font(monospace)
        #self.output_label.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("#333"))
        self.output_label.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("#f9f9f9"))

        self.scrolled_window.add(self.output_label)
        self.vbox.pack_start(self.scrolled_window, False, False, 0)

        # Área do gráfico
        self.canvas = None
        self.figure = None

    def create_combo(self, tooltip, options):
        combo = Gtk.ComboBoxText()
        combo.set_tooltip_text(tooltip)
        for opt in options:
            combo.append(opt, opt)
        combo.set_active(0)
        return combo

    def show_name_dialog(self):
        dialog = Gtk.Dialog(title="Informe seu Nome", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_default_size(300, 100)
        box = dialog.get_content_area()
        box.set_spacing(6)

        label = Gtk.Label(label="Digite seu nome:")
        box.add(label)

        name_entry = Gtk.Entry()
        box.add(name_entry)

        dialog.show_all()
        response = dialog.run()
        self.username = name_entry.get_text().strip() or "Usuário Desconhecido"
        dialog.destroy()

    def on_transmit_clicked(self, widget):
        texto = self.entry.get_text()
        if not texto:
            self.output_label.set_text("⚠️ Por favor, insira um texto para transmitir.")
            return

        modulation_type = self.modulation_combo.get_active_text()
        carrier_modulation_type = self.carrier_modulation_combo.get_active_text()
        framing_type = self.framing_combo.get_active_text()
        error_detection_type = self.error_detection_combo.get_active_text()

        self.transmitter.modulation_type = modulation_type
        self.transmitter.carrier_modulation_type = carrier_modulation_type

        mensagem_codificada = self.transmitter.encode_text(texto)
        tamanho = len(texto)
        hamming = ''.join([str(bit) for bit in hamming_encode(mensagem_codificada)])

        if error_detection_type == "Bit de paridade par":
            dado_deteccao = bit_paridade(hamming)
        else:
            dado_deteccao = crc(hamming)

        if framing_type == "Contagem de caracteres":
            bits = contagem_caracteres(dado_deteccao, tamanho)
        else:
            bits = insercao_bytes(dado_deteccao)

        bits = [int(b) for b in bits]
        signal = self.transmitter.modulate(bits)
        carrier_signal = self.transmitter.carrier_modulate(bits)

        output_text = (
            f"📨 Mensagem: {texto}\n"
            f"Bits       : {" ".join(str(num) for num in mensagem_codificada)}\n"
            f"Hamming    : {" ".join(hamming)}\n"
            f"Erro       : {" ".join(dado_deteccao)}\n"
            f"Enquadrado : {" ".join(str(num) for num in bits[:50])}{'...' if len(bits) > 50 else ''}\n"
            f"→ Sinal transmitido:"
        )
        self.output_label.set_text(output_text)

        if self.canvas:
            self.vbox.remove(self.canvas)

        self.figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.plot_signal(signal, f"Modulação - {modulation_type}", ax1)

        if carrier_modulation_type == "8QAM":
            self.plot_constellation(carrier_signal, ax2)
        else:
            self.plot_ondas(carrier_signal, f"Portadora - {carrier_modulation_type}", ax2)

        self.canvas = FigureCanvas(self.figure)
        self.vbox.pack_start(self.canvas, True, True, 0)
        self.canvas.show()

    def plot_ondas(self, signal, title, ax):
        tempo, sinal = signal
        ax.plot(np.array(tempo), np.array(sinal), label=title)
        ax.set_title(title)
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Amplitude")
        ax.grid()
        ax.legend()
        self.transmitter.send(signal, self.carrier_modulation_combo.get_active_text(),
                              self.framing_combo.get_active_text(),
                              self.error_detection_combo.get_active_text(), self.username)

    def plot_signal(self, signal, title, ax):
        ax.step(np.arange(len(signal)), signal, where='post', label=title)
        ax.set_title(title)
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Amplitude")
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        ax.grid()
        ax.legend()

    def mostrar_aviso(self,aviso):
        dialog = Gtk.MessageDialog(
        parent=self,                          # Janela pai
        #flags=Gtk.DialogFlags.MODAL,          # Modal (bloqueia a janela principal)
        type=Gtk.MessageType.WARNING,         # Tipo (WARNING, ERROR, INFO, etc.)
        buttons=Gtk.ButtonsType.OK,           # Botões (OK, YES_NO, etc.)
        message_format=aviso               # Mensagem principal
        )
        dialog.set_title("Aviso")                 # Título da janela
        dialog.run()                              # Mostra e espera resposta
        dialog.destroy()                          # Fecha o diálogo

    def plot_constellation(self, signal, ax):
        t, mod_signal = signal
        ax.plot(t, mod_signal, label='8QAM')
        ax.set_title("8QAM")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Amplitude")
        ax.grid()
        ax.legend()
        self.transmitter.send([t.tolist(), mod_signal.tolist()],
                              self.carrier_modulation_combo.get_active_text(),
                              self.framing_combo.get_active_text(),
                              self.error_detection_combo.get_active_text(), self.username)

if __name__ == "__main__":
    app = ClientUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
