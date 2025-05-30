import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TesteFluxoCompleto(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.base_url = "http://127.0.0.1:8000"

    def debug_print(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] {message}")

    def preencher_campo(self, by, value, text, field_name):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.clear()
        element.send_keys(text)
        self.debug_print(f"Campo '{field_name}' preenchido: {text}")

    def clicar_elemento(self, by, value, element_name):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        self.debug_print(f"Elemento clicado: {element_name}")

    def cadastrar_usuario(self, email, senha, nome, registro, tipo):
        url_cadastro = f"{self.base_url}/users/cadastrar/"
        self.driver.get(url_cadastro)
        campos = [
            (By.NAME, "email", email, "E-mail"),
            (By.NAME, "nome_completo", nome, "Nome Completo"),
            (By.NAME, "senha", senha, "Senha"),
            (By.NAME, "confirmar_senha", senha, "Confirmar Senha"),
            (By.NAME, "registro_profissional", registro, "Registro Profissional")
        ]
        for campo in campos:
            self.preencher_campo(*campo)

        select_element = self.wait.until(EC.element_to_be_clickable((By.NAME, "tipo_usuario")))
        Select(select_element).select_by_value(tipo)
        self.debug_print(f"Tipo '{tipo.capitalize()}' selecionado")

        self.clicar_elemento(By.XPATH, "//button[contains(., 'Cadastrar')]", "Botão Cadastrar")
        self.wait.until(EC.url_contains("login"))
        self.debug_print(f"Cadastro de {tipo} realizado com sucesso")

    def login_usuario(self, email, senha):
        url_login = f"{self.base_url}/users/login/"
        self.driver.get(url_login)
        self.preencher_campo(By.NAME, "email", email, "E-mail Login")
        self.preencher_campo(By.NAME, "password", senha, "Senha Login")
        self.clicar_elemento(By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Bem-vindo')]")))
        self.debug_print("Login realizado com sucesso")

    def cadastrar_paciente(self, nome, cpf, data_nascimento):
        self.debug_print("\n=== INICIANDO CADASTRO DE PACIENTE ===")
        url_paciente = f"{self.base_url}/pacientes/cadastrar/"
        self.driver.get(url_paciente)

        campos = [
            (By.NAME, "nome_completo", nome, "Nome Completo"),
            (By.NAME, "cpf", cpf, "CPF"),
            (By.NAME, "data_nascimento", data_nascimento, "Data de Nascimento")
        ]
        for campo in campos:
            self.preencher_campo(*campo)

        select_element = self.wait.until(EC.element_to_be_clickable((By.NAME, "medico_responsavel")))
        select = Select(select_element)
        if len(select.options) > 1:
            select.select_by_index(1)
            self.debug_print(f"Médico selecionado: {select.options[1].text}")
        else:
            self.fail("Nenhum médico disponível para seleção")

        self.clicar_elemento(By.XPATH, "//button[contains(., 'Cadastrar')]", "Botão Cadastrar Paciente")
        self.debug_print("Aguardando redirecionamento para lista de pacientes...")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        self.debug_print("Tabela de pacientes encontrada!")

        rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
        self.debug_print(f"Encontradas {len(rows)} linhas na tabela.")
        paciente_encontrado = False
        for idx, row in enumerate(rows, start=1):
            cols = row.find_elements(By.TAG_NAME, "td")
            col_texts = [col.text for col in cols]
            self.debug_print(f"Linha {idx}: {col_texts}")
            if any(nome.lower() in col.text.lower() for col in cols):
                paciente_encontrado = True
                self.debug_print(f"✅ Paciente encontrado na linha {idx}: {col_texts}")
                break

        if not paciente_encontrado:
            self.fail("❌ Paciente não encontrado na tabela após cadastro")

    def test_fluxo_completo(self):
        timestamp = int(time.time())
        senha = "Senha@Segura123"

        medico_email = f"medico_{timestamp}@teste.com"
        medico_crm = f"CRM/SP {timestamp % 100000}"
        self.cadastrar_usuario(medico_email, senha, "Dr. Teste", medico_crm, "medico")
        self.login_usuario(medico_email, senha)

        enfermeiro_email = f"enfermeiro_{timestamp}@teste.com"
        enfermeiro_corenn = f"COREN/SP {timestamp % 100000}"
        self.cadastrar_usuario(enfermeiro_email, senha, "Enf. Teste", enfermeiro_corenn, "enfermeiro")
        self.login_usuario(enfermeiro_email, senha)

        paciente_nome = "Paciente Teste"
        paciente_cpf = f"{timestamp % 100000000000:011d}"
        paciente_data_nascimento = "2000-01-01"
        self.cadastrar_paciente(paciente_nome, paciente_cpf, paciente_data_nascimento)

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.debug_print("Finalizando navegador...")
            self.driver.quit()
            self.debug_print("Navegador finalizado")

if __name__ == "__main__":
    unittest.main()
