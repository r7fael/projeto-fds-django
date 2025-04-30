import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestePainelMedicoCompleto(unittest.TestCase):

    def setUp(self):
        # Configuração do navegador
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Descomente para modo headless após testes
        # chrome_options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "http://localhost:8000"

    def debug_print(self, message):
        """Registra mensagens com timestamp"""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] {message}")

    def preencher_campo(self, by, value, text, field_name):
        """Preenche campo com tratamento robusto"""
        try:
            element = self.wait.until(
                EC.visibility_of_element_located((by, value))
            )
            element.clear()
            element.send_keys(text)
            self.debug_print(f"Campo '{field_name}' preenchido: {text}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao preencher {field_name}: {str(e)}")
            self.driver.save_screenshot(f"erro_{field_name}.png")
            return False

    def clicar_elemento(self, by, value, element_name):
        """Clica em elemento com verificações"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            self.debug_print(f"Elemento clicado: {element_name}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao clicar em {element_name}: {str(e)}")
            self.driver.save_screenshot(f"erro_clique_{element_name}.png")
            return False

    def test_fluxo_completo_medico(self):
        """Teste completo do cadastro até a navegação no painel"""
        # Dados de teste dinâmicos
        timestamp = int(time.time())
        dados_teste = {
            "email": f"medico_{timestamp}@teste.com",
            "senha": "Senha@Segura123",
            "crm": f"CRM/SP {timestamp % 100000}"
        }

        try:
            # === ETAPA 1: CADASTRO ===
            self.debug_print("\n=== INICIANDO CADASTRO ===")
            self.driver.get(f"{self.base_url}/users/cadastrar/")
            self.driver.save_screenshot("1_tela_cadastro.png")

            # Preenche formulário
            campos_cadastro = [
                (By.NAME, "email", dados_teste["email"], "E-mail"),
                (By.NAME, "nome_completo", "Dr. Teste Automatizado", "Nome Completo"),
                (By.NAME, "senha", dados_teste["senha"], "Senha"),
                (By.NAME, "confirmar_senha", dados_teste["senha"], "Confirmar Senha"),
                (By.NAME, "registro_profissional", dados_teste["crm"], "CRM")
            ]

            for campo in campos_cadastro:
                self.assertTrue(
                    self.preencher_campo(*campo),
                    f"Falha ao preencher {campo[3]}"
                )

            # Seleciona tipo médico
            select = Select(self.wait.until(
                EC.presence_of_element_located((By.NAME, "tipo_usuario"))
            ))
            select.select_by_value("medico")
            self.debug_print("Tipo 'Médico' selecionado")

            # Submete formulário
            self.assertTrue(
                self.clicar_elemento(By.XPATH, "//button[contains(., 'Cadastrar')]", "Botão Cadastrar"),
                "Falha ao submeter formulário"
            )

            # Verifica redirecionamento
            self.wait.until(
                lambda d: "login" in d.current_url.lower() or 
                         any(text in d.page_source.lower() for text in ["sucesso", "cadastrado"] )
            )
            self.driver.save_screenshot("2_pos_cadastro.png")
            self.debug_print("Cadastro realizado com sucesso")

            # === ETAPA 2: LOGIN ===
            self.debug_print("\n=== INICIANDO LOGIN ===")
            self.driver.get(f"{self.base_url}/users/login/")
            self.driver.save_screenshot("3_tela_login.png")

            # Preenche credenciais
            self.assertTrue(
                self.preencher_campo(By.NAME, "email", dados_teste["email"], "E-mail Login"),
                "Falha ao preencher e-mail"
            )
            self.assertTrue(
                self.preencher_campo(By.NAME, "password", dados_teste["senha"], "Senha Login"),
                "Falha ao preencher senha"
            )
            self.driver.save_screenshot("4_credenciais_preenchidas.png")

            # Submete login
            self.assertTrue(
                self.clicar_elemento(By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar"),
                "Falha ao tentar login"
            )

            # Verifica redirecionamento para o painel
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Bem-vindo')]"))
            )
            self.driver.save_screenshot("5_painel_principal.png")
            self.debug_print("Login realizado com sucesso")

            # === ETAPA 3: NAVEGAÇÃO NO PAINEL ===
            self.debug_print("\n=== NAVEGANDO NO PAINEL ===")

            # Menu Consultas
            self.assertTrue(
                self.clicar_elemento(
                    By.XPATH,
                    "//a[contains(., 'Consultas') or contains(@href, 'consultas')]",
                    "Menu Consultas"
                ),
                "Falha ao acessar Consultas"
            )
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Consultas')]"))
            )
            self.driver.save_screenshot("6_tela_consultas.png")
            self.debug_print("Navegação para Consultas OK")

            # Menu Pacientes
            self.assertTrue(
                self.clicar_elemento(
                    By.XPATH,
                    "//a[contains(., 'Pacientes') or contains(@href, 'pacientes')]",
                    "Menu Pacientes"
                ),
                "Falha ao acessar Pacientes"
            )
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Pacientes')]"))
            )
            self.driver.save_screenshot("7_tela_pacientes.png")
            self.debug_print("Navegação para Pacientes OK")

            # Voltar para Home
            self.assertTrue(
                self.clicar_elemento(
                    By.XPATH,
                    "//a[contains(., 'Home') or contains(@href, 'dashboard')]",
                    "Menu Home"
                ),
                "Falha ao voltar para Home"
            )
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Bem-vindo')]"))
            )
            self.driver.save_screenshot("8_volta_home.png")
            self.debug_print("Retorno ao Dashboard OK")

            self.debug_print("\nFLUXO COMPLETO CONCLUÍDO COM SUCESSO")

        except Exception as e:
            self.driver.save_screenshot("erro_fatal.png")
            self.debug_print(f"\nERRO NO TESTE: {str(e)}")
            raise

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
            self.debug_print("Navegador finalizado")

if __name__ == "__main__":
    unittest.main()
