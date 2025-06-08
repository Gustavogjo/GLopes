import tkinter as tk
import logging
import json
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from pywinauto import Application
from pywinauto.findwindows import WindowNotFoundError
from logar_mercante import fazer_login

playwright = None
browser_context = None
page = None

initial_page_url = 'https://www.mercante.transportes.gov.br/g33159MT/jsp/logon.jsp'
js_certificado = "subForm()"
js_atualiza_radio_ce = "atualiza_radio(1)"

# Diretório para dados persistentes do navegador, pasta pode ser apagado, é só para não gravar na temp
user_data_directory_path = "C:\\rpa_mercante_descon\\user_data_navegador"
#pasta base rpa
pasta_base = "c:\\rpa_mercante_descon\\ce-mercante"
config_filename = "c:\\rpa_mercante_descon\\config.json"

# --- Configuração de Log ---
LOG_DIR = "C:\\rpa_mercante_descon\\log" # Diretório para os arquivos de log
LOG_FILENAME_BASE = "rpa_desconsolidacao_mercante" # Base do nome do arquivo de log

# Configuração do logger
logging.basicConfig(
    filename="log_atividades.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

def adicionar_log(mensagem):
    log_text.config(state="normal")
    log_text.insert(tk.END, mensagem + "\n")
    log_text.see(tk.END)
    log_text.config(state="disabled")
    log_text.update_idletasks()
    logging.info(mensagem)

def limpar_log():
    log_text.config(state="normal")
    log_text.delete(1.0, tk.END)
    log_text.config(state="disabled")
    adicionar_log("Log limpo pelo usuário.")

def acao_botao1():
    adicionar_log("Passo 1 executado")
    atualizar_passo_atual("Passo 1")
    botao1.config(state="disabled")

    page.goto("https://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.MercanteControler?acao=CE-DESCON&passo=1")
    page.wait_for_load_state()

    time.sleep(1)

    adicionar_log(f"Espera campo de ce mercante!")
    page.wait_for_selector('input[name="nrCeMercante"]')
    page.fill('input[name="nrCeMercante"]', '182505163430269')

    adicionar_log(f"ce mercante: ")

    page.get_by_role("button", name="Enviar").click()
    page.wait_for_load_state()
    time.sleep(1)
    
def acao_botao2():
    adicionar_log("Passo 2 executado")
    atualizar_passo_atual("Passo 2")
    botao1.config(state="disabled")
    botao2.config(state="disabled")

    page.wait_for_selector('input[name="qtdCEs"]')
    page.wait_for_selector('input[name="cdAgtNaveg"]')
    page.wait_for_selector('input[name="cdEmpNaveg"]')

    page.fill('input[name="qtdCEs"]', '1')
    page.fill('input[name="cdAgtNaveg"]', '11070723000183')
    page.fill('input[name="cdEmpNaveg"]', 'CN007868')

    page.get_by_role("button", name="Enviar").click()
    page.wait_for_load_state()

    #passo2
    #get_by_role("textbox", name="Informe a Quantidade de") qtdCEs
    #get_by_role("textbox", name="Informe o Agente") cdAgtNaveg
    #get_by_role("textbox", name="Informe Empresa do") cdEmpNaveg
    #get_by_role("button", name="Enviar") Enviar


def acao_botao3():
    adicionar_log("Passo 3 executado")
    atualizar_passo_atual("Passo 3")
    botao2.config(state="disabled")
    botao3.config(state="disabled")

    page.goto('https://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.MercanteControler?acao=CE-DB&passo=1')
    page.wait_for_load_state()
    time.sleep(1)

    page.evaluate(js_atualiza_radio_ce)
    time.sleep(1)

    page.wait_for_selector('input[name="nrCeMercante"]')
    page.fill('input[name="nrCeMercante"]', '182505163430269')

    page.get_by_role("button", name="Enviar").click()
    page.wait_for_load_state()
    time.sleep(1)

    page.wait_for_selector('input[name="nrBlConhecimento"]')
    page.fill('input[name="nrBlConhecimento"]', '1234567890')

    page.wait_for_selector('input[name="cdPortoOrigem"]')
    page.fill('input[name="cdPortoOrigem"]', 'CNNGB')

    page.wait_for_selector('input[name="cdPortoDestino"]')
    page.fill('input[name="cdPortoDestino"]', 'BRNVT')

    page.wait_for_selector('input[name="dtEmissaoCe"]')
    page.fill('input[name="dtEmissaoCe"]', '18/05/2025')

    page.wait_for_selector('input[name="cdConsignatario"]')
    page.fill('input[name="cdConsignatario"]', '10869047000140')

    page.get_by_role("input", name="Enviar").click()

def alternar_estado_botao(var, botao):
    botao.config(state="disabled" if var.get() else "normal")

def carregar_configuracoes():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    else:
        config_padrao = {"passo1": False, "passo2": False, "passo3": False}
        with open("config.json", "w") as f:
            json.dump(config_padrao, f)
        return config_padrao

def salvar_configuracoes():
    config = {
        "passo1": var1.get(),
        "passo2": var2.get(),
        "passo3": var3.get()
    }
    with open("config.json", "w") as f:
        json.dump(config, f)

def atualizar_passo_atual(passo):
    info3.config(text=f"CPF do Certificado: 123.456.789-00\nPasso Atual: {passo}")

def iniciar_navegador():
    global playwright, browser_context, page

    # Certifica que o diretório de dados do usuário existe
    if not os.path.exists(user_data_directory_path):
        os.makedirs(user_data_directory_path)
        adicionar_log(f"Diretório de dados do usuário criado em: {user_data_directory_path}")
    else:
        adicionar_log(f"Usando diretório de dados do usuário existente: {user_data_directory_path}")

    playwright = sync_playwright().start()
    
    browser_context = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_directory_path,
        ignore_https_errors=True,
        headless=False
    )
    
    page = browser_context.new_page()


def iniciar_robo():
    from logar_mercante import fazer_login

    iniciar_navegador()
    
    strRetorno = fazer_login(logger, log_text, page, browser_context)
    time.sleep(2)

    #page.pause()

    if not var1.get():
        botao1.config(state="normal")
    if not var2.get():
        botao2.config(state="normal")
    if not var3.get():
        botao3.config(state="normal")

def setup_logging():
    """Configura o logger para salvar mensagens em um arquivo diário."""
    # Obter a data atual
    data_atual = datetime.now()
    # Formatar o nome do arquivo de log (rpa_consula_mercante_YYYYMMDD.log)
    nome_arquivo_log = f"{LOG_FILENAME_BASE}_{data_atual.strftime('%Y%m%d')}.log"
    caminho_arquivo_log = os.path.join(LOG_DIR, nome_arquivo_log)

    # Criar o diretório de log se ele não existir
    os.makedirs(LOG_DIR, exist_ok=True)

    # Configurar o logger
    # Usamos getLogger(__name__) para obter um logger específico para este módulo
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO) # Define o nível mínimo de mensagens a serem logadas (INFO e acima)

    # Impedir que handlers sejam duplicados se a função for chamada múltiplas vezes
    if not logger.handlers:
        # Criar um handler para escrever no arquivo
        file_handler = logging.FileHandler(caminho_arquivo_log, encoding='utf-8')
        # Criar um formatador para as mensagens de log (incluindo timestamp)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # Adicionar o formatador ao handler
        file_handler.setFormatter(formatter)
        # Adicionar o handler ao logger
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# --- Fim da Configuração de Log ---
# Carregar configurações
config = carregar_configuracoes()

#from conexao_banco import consulta_ce_supabase
#consulta_ce_supabase()

# --- Configurar o logger no início da execução ---
logger = setup_logging()
logger.info("Script rpa consulta iniciado.")

# Criar janela principal
janela = tk.Tk()
janela.title("Automatização de Desconsolidação")
janela.geometry("900x550")
janela.attributes("-topmost", True)

# Frame de Informações
info_frame = tk.LabelFrame(janela, text="Informações", padx=10, pady=10)
info_frame.pack(fill="x", padx=10, pady=10)

info_columns = tk.Frame(info_frame)
info_columns.pack(fill="x")

label1 = tk.Label(info_columns, text="Número do CE: 123456789\nNº Processo: 2025.0001\nQuantidade de House: 5",
                  justify="left", anchor="w")
label1.pack(side="left", expand=True, padx=10)

label2 = tk.Label(info_columns, text="CNPJ Desconsolidação: 12.345.678/0001-90\nCódigo NVOCC: NV123456",
                  justify="center", anchor="center")
label2.pack(side="left", expand=True, padx=10)

info3 = tk.Label(info_columns, text="CPF do Certificado: 123.456.789-00\nPasso Atual: Nenhum",
                 justify="right", anchor="e")
info3.pack(side="left", expand=True, padx=10)

# Botão Iniciar Robo
btn_iniciar = tk.Button(janela, text="Iniciar Robo", command=iniciar_robo)
btn_iniciar.pack(pady=10)

# Frame dos passos
frame_passos = tk.Frame(janela)
frame_passos.pack(fill="x", padx=10, pady=10)

var1 = tk.BooleanVar(value=config["passo1"])
var2 = tk.BooleanVar(value=config["passo2"])
var3 = tk.BooleanVar(value=config["passo3"])

def criar_groupbox_passo(titulo, var, comando):
    group = tk.LabelFrame(frame_passos, text=titulo, padx=10, pady=10)
    group.pack(side="left", expand=True, fill="both", padx=5)
    check = tk.Checkbutton(group, text="Automático", variable=var, state="normal" if var.get() else "disabled")
    check.pack(pady=5)
    botao = tk.Button(group, text="Executar", command=comando, state="disabled")
    botao.pack(pady=5)
    alternar_estado_botao(var, botao)
    var.trace_add("write", lambda *args: alternar_estado_botao(var, botao))
    return botao

botao1 = criar_groupbox_passo("Acessar CE para desconsolidação", var1, acao_botao1)
botao2 = criar_groupbox_passo("Preencher dados para desconsolidação", var2, acao_botao2)
botao3 = criar_groupbox_passo("Incluir Dados Basicos CE", var3, acao_botao3)

# Frame do log
log_frame = tk.LabelFrame(janela, text="Log de Atividades", padx=10, pady=5)
log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

btn_limpar = tk.Button(log_frame, text="Limpar Log", command=limpar_log)
btn_limpar.pack(anchor="ne", padx=5, pady=5)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(log_frame, height=10, state="disabled", wrap="word", yscrollcommand=scrollbar.set)
log_text.pack(fill="both", expand=True)
scrollbar.config(command=log_text.yview)

# Salvar configurações ao fechar
janela.protocol("WM_DELETE_WINDOW", lambda: [salvar_configuracoes(), janela.destroy()])

janela.mainloop()
