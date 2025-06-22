import gi
gi.require_version("Gtk", "3.0")
import matplotlib.pyplot as ax
from gi.repository import Gtk
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from cliente.transmitter import Transmitter
import numpy as np
from camada_enlace.enquadramento import contagem_caracteres, insercao_bytes
from camada_enlace.deteccao_erros import bit_paridade, crc
from camada_enlace.hamming import hamming_encode


class ClientUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmissor")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        self.transmitter = Transmitter()
        self.username = None  # Variável para armazenar o nome do usuário

        # Exibe o popup para capturar o nome
        self.show_name_dialog()



    

        # Layout principal
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(self.vbox)


        # Entrada de texto
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite o texto para transmitir")
        self.vbox.pack_start(self.entry, False, False, 0)

        # Box modulação
        self.modulation_combo = Gtk.ComboBoxText()
        self.modulation_combo.append("NRZ", "NRZ")
        self.modulation_combo.append("Manchester", "Manchester")
        self.modulation_combo.append("Bipolar", "Bipolar")
        self.modulation_combo.set_active(0)
        self.vbox.pack_start(self.modulation_combo, False, False, 0)

        self.carrier_modulation_combo = Gtk.ComboBoxText()
        self.carrier_modulation_combo.append("ASK", "ASK")
        self.carrier_modulation_combo.append("FSK", "FSK")
        self.carrier_modulation_combo.append("8QAM", "8QAM")
        self.carrier_modulation_combo.set_active(0)
        self.vbox.pack_start(self.carrier_modulation_combo, False, False, 0)

        # Box Enquadramento
        self.framing_combo = Gtk.ComboBoxText()
        self.framing_combo.append("Contagem de caracteres", "Contagem de caracteres")
        self.framing_combo.append("Inserção de bytes", "Inserção de bytes")
        self.framing_combo.set_active(0)
        self.vbox.pack_start(self.framing_combo, False, False, 0)

        # Box Detecção de Erros
        self.error_detection_combo = Gtk.ComboBoxText()
        self.error_detection_combo.append("Bit de paridade par", "Bit de paridade par")
        self.error_detection_combo.append("CRC", "CRC")
        self.error_detection_combo.set_active(0)
        self.vbox.pack_start(self.error_detection_combo, False, False, 0)

        # Botão de transmissão
        self.transmit_button = Gtk.Button(label="Transmitir")
        self.transmit_button.connect("clicked", self.on_transmit_clicked)
        self.vbox.pack_start(self.transmit_button, False, False, 0)

        # Área de saída de texto com barra de rolagem
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_min_content_height(150)

        self.output_label = Gtk.Label(label="Saída:")
        self.output_label.set_line_wrap(True)
        self.output_label.set_line_wrap_mode(Gtk.WrapMode.WORD)
        self.output_label.set_justify(Gtk.Justification.LEFT)
        self.output_label.set_xalign(0)
        self.scrolled_window.add(self.output_label)

        self.vbox.pack_start(self.scrolled_window, False, False, 0)

        # Área do gráfico
        self.canvas = None
        self.figure = None
        self.ax = None

    def show_name_dialog(self):
        """Exibe um diálogo para capturar o nome do usuário."""
        dialog = Gtk.Dialog(title="Informe seu Nome", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        dialog.set_default_size(300, 100)
        box = dialog.get_content_area()

        label = Gtk.Label(label="Digite seu nome:")
        box.add(label)

        name_entry = Gtk.Entry()
        box.add(name_entry)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.username = name_entry.get_text().strip()

        if not self.username:  # Se o nome não for fornecido, força o preenchimento
            self.username = "Usuário Desconhecido"

        dialog.destroy()

    def on_transmit_clicked(self, widget):
        texto = self.entry.get_text()
        modulation_type = self.modulation_combo.get_active_text()
        carrier_modulation_type = self.carrier_modulation_combo.get_active_text()
        framing_type = self.framing_combo.get_active_text()
        error_detection_type = self.error_detection_combo.get_active_text()

        if not texto:
            self.output_label.set_text("Por favor, insira um texto para transmitir.")
        else:
            # Configurar modulação e processar o texto
            self.transmitter.modulation_type = modulation_type
            self.transmitter.carrier_modulation_type = carrier_modulation_type

            # Codificação inicial
            mensagem_codificada = self.transmitter.encode_text(texto)

            # Salvar o tamanho original do texto
            tamanho = len(texto)

            # Aplicação do Hamming
            hamming = hamming_encode(mensagem_codificada)
            hamming = ''.join([str(bit) for bit in hamming])

            # Detecção de erros
            if error_detection_type == "Bit de paridade par":
                dado_deteccao = bit_paridade(hamming)
            elif error_detection_type == "CRC":
                dado_deteccao = crc(hamming)

            # Enquadramento
            bits = None  # Defina a variável bits com um valor padrão
            if framing_type == "Contagem de caracteres":
                bits = contagem_caracteres(dado_deteccao, tamanho)
            elif framing_type == "Inserção de bytes":
                bits = insercao_bytes(dado_deteccao)

            # Verifique se bits foi atribuído corretamente
            if not bits:
                self.output_label.set_text("Erro: Nenhum enquadramento válido selecionado.")
                return

            bits = [int(bit) for bit in bits]

            signal = self.transmitter.modulate(bits)
            carrier_signal = self.transmitter.carrier_modulate(bits)
            print(len(bits))
            
            # Atualizar a saída de texto
            output_text = (
                f"Mensagem transmitida: {texto}\n"
                f"Mensagem bits: {mensagem_codificada}\n"
                f"Mensagem com Hamming: {hamming}\n"
                f"Mensagem com detecção de erros: {dado_deteccao}\n"
                f"Mensagem enquadrada: {bits}\n"
                f"sinal transmitido:"
            )
            self.output_label.set_text(output_text)

            # Limpar a entrada de texto
            self.entry.set_text("")

            # Atualizar os gráficos
            if self.canvas:
                self.vbox.remove(self.canvas)  # Remover gráfico anterior, se houver

            # Criar a figura com 2 subgráficos (lado a lado)
            self.figure, (self.ax1, self.ax2) = ax.subplots(1, 2, figsize=(16, 8))  # Ajuste o tamanho conforme necessário

            # Plotando o gráfico da modulação digital (NRZ, Bipolar, Manchester)
            self.plot_signal(signal, f"Modulação Digital - {modulation_type}", self.ax1)

            # Plotando o gráfico de modulação por portadora
            if carrier_modulation_type == "8QAM":
                self.plot_constellation(carrier_signal, self.ax2)
            elif carrier_modulation_type in ["FSK", "ASK"]:
                self.plot_ondas(carrier_signal, f"Modulação por Portadora - {carrier_modulation_type}", self.ax2)

            # Atualizar o canvas
            self.canvas = FigureCanvas(self.figure)
            self.vbox.pack_start(self.canvas, True, True, 0)
            self.canvas.show()

    # Gera gráfico FSK E ASK
    def plot_ondas(self, signal: list, title: str, ax):
        tempo, sinal = signal
        tempo = np.array(tempo)
        sinal = np.array(sinal)
        ax.plot(tempo, sinal, label=title)
        ax.set_title(title)
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Amplitude")
        ax.grid()
        ax.legend()
        self.transmitter.send(signal, self.carrier_modulation_combo.get_active_text(), self.framing_combo.get_active_text(), self.error_detection_combo.get_active_text(), self.username)

    # Gera gráficos NRZ, Bipolar e Manchester
    def plot_signal(self, signal: list, title: str, ax):
        tempo = np.arange(len(signal))
        ax.step(tempo, signal, where='post', label=title)
        ax.set_title(title)
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Sinal")
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax.grid(True)
        ax.legend()
        #self.transmitter.send(signal, self.modulation_combo.get_active_text(), self.framing_combo.get_active_text(), self.error_detection_combo.get_active_text(), self.username)

    # Gera gráfico 8QAM
    def plot_constellation(self, signal:list, ax):
        print(signal)
        t = signal[0]
        modulated_signal = signal[1]
         
         # Plotar o sinal modulado
        ax.plot(t, modulated_signal, label='Sinal Modulado (8QAM)')
        ax.set_title('Modulação 8QAM', fontsize=14)
        ax.set_xlabel('Tempo', fontsize=12)
        ax.set_ylabel('Amplitude', fontsize=12)
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        ax.grid()
        ax.legend()
        self.transmitter.send([signal[0].tolist(), signal[1].tolist()], self.carrier_modulation_combo.get_active_text(), self.framing_combo.get_active_text(), self.error_detection_combo.get_active_text(), self.username)

if __name__ == "__main__":
    app = ClientUI()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()