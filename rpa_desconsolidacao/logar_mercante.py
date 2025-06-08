import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from playwright.async_api import async_playwright
from pywinauto import Application
from pywinauto.findwindows import WindowNotFoundError
import time # Importa a biblioteca time para usar sleep
import os # Importar os para criar o diretório se não existir
import json
import logging 

#URL inicial
initial_page_url = 'https://www.mercante.transportes.gov.br/g33159MT/jsp/logon.jsp'

js_certificado = "subForm()"

#pasta base rpa
pasta_base = "c:\\rpa_mercante_descon\\ce-mercante"
config_filename = "c:\\rpa_mercante_descon\\config.json"

js_valida_logado = 'document.body.innerText.indexOf("CPF");'

js_retorna_cpf = """
(() => {
    return document.querySelector("body").querySelectorAll('font')[0].innerText;
})()
"""#fazer goto para a tela para pegar o cpf

# --- Configuração de Log ---
LOG_DIR = "C:\\rpa_mercante_descon\\log" # Diretório para os arquivos de log
LOG_FILENAME_BASE = "rpa_consula_mercante" # Base do nome do arquivo de log

def adicionar_log(log_text, logger, mensagem, nivel=logging.INFO):
    log_text.config(state="normal")
    if nivel == logging.ERROR:
        log_text.tag_configure("error", foreground="red")
        log_text.insert(tk.END, mensagem + "\n", "error")
        logger.error(mensagem)
    else:
        log_text.insert(tk.END, mensagem + "\n")
        logger.info(mensagem)
    #log_text.insert(tk.END, mensagem + "\n")
    log_text.see(tk.END)
    log_text.config(state="disabled")
    log_text.update_idletasks()

def fazer_login(logger, log_text, page, browser_context):
    
    # --- Configurar o logger no início da execução ---
    adicionar_log(log_text, logger, "Script rpa consulta iniciado.")
    try:
        # 1. Carregar a página inicial (logon.jsp)
        adicionar_log(log_text, logger, f"Navegando para {initial_page_url} (ignorando erros de HTTPS)...")
        page.goto(initial_page_url)
        page.wait_for_load_state()
        adicionar_log(log_text, logger, "Página inicial (logon.jsp) carregada.")

        # 2. Chamar a função JavaScript que dispara o popup do certificado
        adicionar_log(log_text, logger, "Chamando a função JavaScript para selecionar o certificado...")
        page.evaluate(js_certificado) # AWAIT É NECESSÁRIO
        adicionar_log(log_text, logger, "'js que faz a chamada do certificado executada.")

        # --- Tentar Interagir com a Janela de Certificado do Sistema (Pywinauto) ---
        # Esta parte é executada para lidar com o popup do sistema operacional.
        adicionar_log(log_text, logger, "Aguardando um momento para a janela do sistema operacional aparecer...")
        time.sleep(2) # Ajuste este tempo conforme necessário
        try:
            from pywinauto.findwindows import find_window
            #pega a tela ativa
            hwnd = find_window(active_only=True)
            
            app = Application().connect(handle=hwnd)
            main_window = app.window(handle=hwnd)

            #manda um enter para selecionar o certificado
            main_window.type_keys('{ENTER}')

            #Aguarda usuario dar ok que logou no mercante
            
            #resposta = messagebox.askquestion("Certificado", "Após selecionar o certificado, clique em Continuar.\nDeseja continuar?")

            #if resposta == 'yes':
            #    adicionar_log(log_text, logger, "Usuário clicou em Continuar")
            #else:
            #    adicionar_log(log_text, logger, "Usuário clicou em Cancelar")

            # Criar janela principal
            #janela = tk.Tk()
            #janela.withdraw()


            #caso tenha mais de um, pode usar por posição
            
            adicionar_log(log_text, logger, "Interação com janela do sistema finalizada (Enter enviado).")
            page.wait_for_load_state()

            valida_logado = page.evaluate(js_valida_logado)
            retorno_cpf_logado = ""

            if(valida_logado != -1):
                retorno_cpf_logado = "Login não efetuado com sucesso!"
            else:
                retorno_cpf_logado = page.evaluate(js_retorna_cpf)
            
            return retorno_cpf_logado

        except Exception as e:
            adicionar_log(log_text, logger, f"Ocorreu um erro no Pywinauto durante a interação da janela: {e}", logging.ERROR)
    except Exception as e:
        adicionar_log(log_text, logger, f"ERRO: {e}", logging.ERROR)

