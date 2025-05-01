from django.test import TestCase
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
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
    
        # chrome_options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)  
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
            return False

    def verificar_sessao_ativa(self):
        """Verifica se a sessão do navegador ainda está ativa"""
        try:
            self.driver.title 
            return True
        except:
            return False

    def test_fluxo_completo_medico(self):
        """Teste completo do cadastro até a navegação no painel"""
       
        timestamp = int(time.time())
        dados_teste = {
            "email": f"medico_{timestamp}@teste.com",
            "senha": "Senha@Segura123",
            "crm": f"CRM/SP {timestamp % 100000}"
        }

        try:
            self.debug_print("\n=== INICIANDO CADASTRO ===")
            self.driver.get(f"{self.base_url}/users/cadastrar/")

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

            select = Select(self.wait.until(
                EC.presence_of_element_located((By.NAME, "tipo_usuario"))
            ))
            select.select_by_value("medico")
            self.debug_print("Tipo 'Médico' selecionado")

            self.assertTrue(
                self.clicar_elemento(By.XPATH, "//button[contains(., 'Cadastrar')]", "Botão Cadastrar"),
                "Falha ao submeter formulário"
            )

            self.wait.until(
                lambda d: "login" in d.current_url.lower() or 
                         any(text in d.page_source.lower() for text in ["sucesso", "cadastrado"])
            )
            self.debug_print("Cadastro realizado com sucesso")

            self.debug_print("\n=== INICIANDO LOGIN ===")
            self.driver.get(f"{self.base_url}/users/login/")

            self.assertTrue(
                self.preencher_campo(By.NAME, "email", dados_teste["email"], "E-mail Login"),
                "Falha ao preencher e-mail"
            )
            self.assertTrue(
                self.preencher_campo(By.NAME, "password", dados_teste["senha"], "Senha Login"),
                "Falha ao preencher senha"
            )

            self.assertTrue(
                self.clicar_elemento(By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar"),
                "Falha ao tentar login"
            )

            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Bem-vindo')]"))
            )
            self.debug_print("Login realizado com sucesso e redirecionado para o painel")

            self.debug_print("\nNAVEGAÇÃO NA HOME COMPLETA. O TESTE CONTINUARÁ ATÉ O FIM.")

            self.debug_print("\nPausando o teste para manter o navegador aberto.")
            time.sleep(60)  

        except Exception as e:
            if not self.verificar_sessao_ativa():
                self.debug_print("Sessão do navegador desconectada. Teste abortado.")
            self.debug_print(f"\nERRO NO TESTE: {str(e)}")
            raise

    def tearDown(self):
        """Finaliza o navegador após o teste"""
        if hasattr(self, 'driver'):
            self.debug_print("Finalizando navegador...")
            self.driver.quit()
            self.debug_print("Navegador finalizado")

class TesteRegistroObservacoesEnfermeiro(unittest.TestCase):
    
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # chrome_options.add_argument("--headless")  # Descomente para modo headless

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.base_url = "http://localhost:8000"
        
        # Criar dados de teste (simulando um paciente existente)
        self.paciente_id = 1  # Substitua pela lógica para criar um paciente real

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
            return False

    def login_enfermeiro(self, email="enfermeiro@teste.com", senha="Senha@123"):
        """Realiza login como enfermeiro"""
        self.driver.get(f"{self.base_url}/users/login/")
        self.preencher_campo(By.NAME, "email", email, "E-mail")
        self.preencher_campo(By.NAME, "password", senha, "Senha")
        self.clicar_elemento(By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar")
        self.wait.until(EC.url_contains("painel"))

    def test_cenario1_registro_observacoes_simples(self):
        """Cenário 1: Registro simples de observações"""
        try:
            self.debug_print("\n=== INICIANDO CENÁRIO 1: REGISTRO SIMPLES ===")
            
            # Login como enfermeiro
            self.login_enfermeiro()
            
            # Navegar para página do paciente
            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/")
            self.wait.until(EC.presence_of_element_located((By.ID, "observacoes-textarea")))
            
            # Preencher observações
            observacao = "Paciente apresentou melhora nos sintomas. Pressão arterial 12x8."
            self.assertTrue(
                self.preencher_campo(By.ID, "observacoes-textarea", observacao, "Campo de Observações"),
                "Falha ao preencher observações"
            )
            
            # Salvar
            self.assertTrue(
                self.clicar_elemento(By.ID, "salvar-observacoes", "Botão Salvar"),
                "Falha ao clicar em salvar"
            )
            
            # Verificar mensagem de sucesso
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
            mensagem = self.driver.find_element(By.CLASS_NAME, "alert-success").text
            self.assertIn("Observações salvas com sucesso", mensagem)
            self.debug_print("Observações registradas com sucesso")
            
        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            raise

    def test_cenario2_sugestao_termos_medicos(self):
        """Cenário 2: Sugestão de termos médicos"""
        try:
            self.debug_print("\n=== INICIANDO CENÁRIO 2: SUGESTÃO DE TERMOS ===")
            
            # Login como enfermeiro
            self.login_enfermeiro()
            
            # Navegar para página do paciente
            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/")
            textarea = self.wait.until(EC.presence_of_element_located((By.ID, "observacoes-textarea")))
            
            # Digitar para acionar sugestões
            textarea.send_keys("feb")
            time.sleep(1)  # Espera para sugestões aparecerem
            
            # Verificar sugestões
            sugestoes = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sugestao-termo"))
            )
            self.assertGreater(len(sugestoes), 0, "Nenhuma sugestão apareceu")
            
            # Verificar conteúdo das sugestões
            termos_esperados = ["febre", "febril", "afebril"]
            for sugestao in sugestoes:
                self.assertIn(sugestao.text.lower(), termos_esperados)
            
            self.debug_print(f"Sugestões encontradas: {[s.text for s in sugestoes]}")
            
            # Selecionar uma sugestão
            sugestoes[0].click()
            self.assertIn("febre", textarea.get_attribute("value"))
            self.debug_print("Sugestão selecionada com sucesso")
            
        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            raise

    def test_cenario3_falha_registro_observacoes(self):
        """Cenário 3: Falha no registro"""
        try:
            self.debug_print("\n=== INICIANDO CENÁRIO 3: FALHA NO REGISTRO ===")
            
            # Login como enfermeiro
            self.login_enfermeiro()
            
            # Navegar para página do paciente
            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/")
            self.wait.until(EC.presence_of_element_located((By.ID, "observacoes-textarea")))
            
            # Simular falha (removendo o botão via JavaScript)
            self.driver.execute_script("""
                document.getElementById('salvar-observacoes').remove();
                var form = document.querySelector('form');
                form.action = '/url-invalida';
            """)
            
            # Tentar salvar observações
            self.preencher_campo(By.ID, "observacoes-textarea", "Observação de teste", "Campo de Observações")
            self.clicar_elemento(By.CSS_SELECTOR, "form button[type='submit']", "Botão Salvar")
            
            # Verificar mensagem de erro
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
            mensagem = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
            self.assertIn("Não foi possível salvar as observações", mensagem)
            self.assertIn("suporte técnico", mensagem.lower())
            self.debug_print("Mensagem de erro exibida corretamente")
            
        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            raise

    def tearDown(self):
        """Finaliza o navegador após o teste"""
        if hasattr(self, 'driver'):
            self.debug_print("Finalizando navegador...")
            self.driver.quit()
            self.debug_print("Navegador finalizado")

if __name__ == "__main__":
    unittest.main()