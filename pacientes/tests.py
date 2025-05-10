import unittest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth import get_user_model
from pacientes.models import Paciente
import subprocess
import os
from datetime import date
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.common.exceptions import WebDriverException, TimeoutException


class TestePainelMedicoCompleto(unittest.TestCase):
    """
    Caso de teste para o fluxo de trabalho completo de um profissional médico no sistema.
    Isso inclui registro de usuário, login e outras ações potenciais.
    """

    def setUp(self):
        """
        Configura o ambiente de teste antes que cada método de teste seja executado.
        Isso inclui:
        - Configurar as opções do navegador Chrome.
        - Verificar se o servidor de desenvolvimento Django está em execução.
        - Inicializar o webdriver do Chrome.
        - Configurar uma espera explícita para o Selenium.
        """
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")

        # Configurações de conexão
        self.base_url = "http://localhost:8000"
        self.max_retries = 3

        # Verifica se o servidor está respondendo
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    break
            except (MaxRetryError, NewConnectionError, ConnectionError) as e:
                self.debug_print(f"Tentativa {attempt + 1} de conexão falhou: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                else:
                    raise ConnectionError(
                        f"Não foi possível conectar ao servidor após {self.max_retries} tentativas: {str(e)}"
                    )

        service = Service(ChromeDriverManager().install())
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except WebDriverException as e:
            self.debug_print(f"Erro ao inicializar o driver do Chrome: {e}")
            self.skipTest(f"Falha ao inicializar o driver do Chrome: {e}")  # Pula o teste se o driver não iniciar

        self.wait = WebDriverWait(self.driver, 15)

    def debug_print(self, message):
        """
        Imprime uma mensagem de depuração com um timestamp.

        Args:
            message (str): A mensagem a ser impressa.
        """
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] {message}")

    def preencher_campo(self, by, value, text, field_name):
        """
        Preenche um campo de formulário com o texto fornecido, lidando com possíveis exceções.

        Args:
            by (selenium.webdriver.common.by.By): O método para localizar o elemento (por exemplo, By.NAME).
            value (str): O valor para identificar o elemento (por exemplo, o nome do campo).
            text (str): O texto a ser inserido no campo.
            field_name (str): Um nome descritivo para o campo (para registro).

        Returns:
            bool: True se o campo foi preenchido com sucesso, False caso contrário.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            self.debug_print(f"Campo '{field_name}' preenchido: {text}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao preencher {field_name}: {str(e)}")
            return False

    def clicar_elemento(self, by, value, element_name):
        """
        Clica em um elemento, lidando com possíveis exceções.

        Args:
            by (selenium.webdriver.common.by.By): O método para localizar o elemento.
            value (str): O valor para identificar o elemento.
            element_name (str): Um nome descritivo para o elemento (para registro).

        Returns:
            bool: True se o elemento foi clicado com sucesso, False caso contrário.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            self.debug_print(f"Elemento clicado: {element_name}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao clicar em {element_name}: {str(e)}")
            return False

    def test_fluxo_completo_medico(self):
        """
        Caso de teste para simular o fluxo de trabalho completo de um médico:
        1.  Registrar um novo médico.
        2.  Fazer login como o novo médico.
        3.  Verificar o login bem-sucedido.
        """
        timestamp = int(time.time())
        dados_teste = {
            "email": f"medico_{timestamp}@teste.com",
            "senha": "Senha@Segura123",
            "crm": f"CRM/SP {timestamp % 100000}",
        }

        try:
            self.debug_print("\n=== INICIANDO CADASTRO ===")
            self.driver.get(f"{self.base_url}/users/cadastrar/")

            campos_cadastro = [
                (By.NAME, "email", dados_teste["email"], "E-mail"),
                (By.NAME, "nome_completo", "Dr. Teste Automatizado", "Nome Completo"),
                (By.NAME, "senha", dados_teste["senha"], "Senha"),
                (By.NAME, "confirmar_senha", dados_teste["senha"], "Confirmar Senha"),
                (By.NAME, "registro_profissional", dados_teste["crm"], "CRM"),
            ]

            for campo in campos_cadastro:
                if not self.preencher_campo(*campo):
                    self.fail(f"Falha ao preencher {campo[3]}")

            select = Select(
                self.wait.until(
                    EC.presence_of_element_located((By.NAME, "tipo_usuario"))
                )
            )
            select.select_by_value("medico")
            self.debug_print("Tipo 'Médico' selecionado")

            if not self.clicar_elemento(
                By.XPATH, "//button[contains(., 'Cadastrar')]", "Botão Cadastrar"
            ):
                self.fail("Falha ao submeter formulário")

            self.wait.until(lambda d: "login" in d.current_url.lower())
            self.debug_print("Cadastro realizado com sucesso")

            self.debug_print("\n=== INICIANDO LOGIN ===")
            self.driver.get(f"{self.base_url}/users/login/")

            if not self.preencher_campo(
                By.NAME, "email", dados_teste["email"], "E-mail Login"
            ):
                self.fail("Falha ao preencher email")
            if not self.preencher_campo(
                By.NAME, "password", dados_teste["senha"], "Senha Login"
            ):
                self.fail("Falha ao preencher senha")

            if not self.clicar_elemento(
                By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar"
            ):
                self.fail("Falha ao fazer login")

            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'Bem-vindo')]"))
            )
            self.debug_print("Login realizado com sucesso")

            self.debug_print(
                "\nTeste concluído com sucesso. Mantendo navegador aberto por 30 segundos..."
            )
            time.sleep(
                30
            )  # Considere remover isso. Os testes do Selenium devem ser o mais rápidos possível.

        except Exception as e:
            self.debug_print(f"\nERRO NO TESTE: {str(e)}")
            self.driver.save_screenshot("erro_teste_medico.png")
            raise  # Relança a exceção para marcar o teste como falho.

    def tearDown(self):
        """
        Limpa o ambiente de teste após a execução de cada método de teste.
        Isso inclui fechar o webdriver do Chrome. Use um `try...finally`
        para garantir que o driver seja fechado mesmo se uma asserção falhar.
        """
        if hasattr(self, "driver"):
            try:
                self.debug_print("Finalizando navegador...")
            finally:
                self.driver.quit()
                self.debug_print("Navegador finalizado")


class TesteRegistroObservacoesEnfermeiro(unittest.TestCase):
    

    @classmethod
    def setUpClass(cls):
        """
        Configura o ambiente de teste uma vez para toda a classe. Isso é mais eficiente
        para tarefas que não mudam entre os métodos de teste. Isso inclui:
        - Configurar as opções do navegador Chrome.
        - Iniciar o servidor de desenvolvimento Django.  <-- IMPORTANTE
        - Criar um usuário enfermeiro de teste e um paciente de teste.
        """
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")

        # Iniciar o servidor de desenvolvimento Django. Este é o passo crucial.
        cls.server_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd(),  # Define o diretório atual como o diretório de trabalho
        )
        time.sleep(5)  # Dá ao servidor alguns segundos para iniciar. Ajuste conforme necessário.
        cls.base_url = "http://localhost:8000"
        # Verifica conexão com o servidor
        for attempt in range(3):  # Tenta 3 vezes
            try:
                response = requests.get(cls.base_url, timeout=5)
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError as e:
                print(f"Failed to connect to server on attempt {attempt + 1}: {e}")
                if attempt < 2:
                    time.sleep(5)  # Espera 5 segundos antes de tentar novamente
                else:
                    raise  # Re-raise the exception after 3 attempts

        service = Service(ChromeDriverManager().install())
        try:
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        except WebDriverException as e:
            print(f"Error initializing chrome driver: {e}")
            raise
        cls.wait = WebDriverWait(cls.driver, 15)

        # Criar usuário enfermeiro e paciente de teste
        User = get_user_model()
        cls.email_enfermeiro = "enfermeiroteste@teste.com"
        cls.senha_enfermeiro = "Senha@123"
        cls.coren = "COREN/SP 123456"

        User.objects.filter(email=cls.email_enfermeiro).delete()

        cls.enfermeiro = User.objects.create(
            email=cls.email_enfermeiro,
            nome_completo="Enfermeiro Teste",
        )
        cls.enfermeiro.set_password(cls.senha_enfermeiro)
        cls.enfermeiro.save()

        cls.paciente = Paciente.objects.create(data_nascimento=date(2000, 1, 1))
        cls.paciente_id = cls.paciente.id

    def debug_print(self, message):
        """Imprime uma mensagem de depuração com um timestamp."""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{timestamp}] {message}")

    def login_enfermeiro(self):
        """
        Faz login do usuário enfermeiro. Retorna True em caso de sucesso, False em caso de falha.
        """
        try:
            self.driver.get(f"{self.base_url}/users/login/")
            if not self.preencher_campo(
                By.NAME, "email", self.email_enfermeiro, "E-mail Login"
            ):
                return False
            if not self.preencher_campo(
                By.NAME, "password", self.senha_enfermeiro, "Senha Login"
            ):
                return False
            if not self.clicar_elemento(
                By.XPATH, "//button[contains(., 'Entrar')]", "Botão Entrar"
            ):
                return False
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(., 'Bem-vindo')]")
                )
            )
            return True
        except TimeoutException as e:
            self.debug_print(f"Timeout durante o login do enfermeiro: {e}")
            return False
        except Exception as e:
            self.debug_print(f"Falha no login do enfermeiro: {str(e)}")
            return False

    def preencher_campo(self, by, value, text, field_name):
        """Preenche um campo de formulário com o texto fornecido."""
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, value)))
            element.clear()
            element.send_keys(text)
            self.debug_print(f"Campo '{field_name}' preenchido: {text}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao preencher {field_name}: {str(e)}")
            return False

    def clicar_elemento(self, by, value, element_name):
        """Clica em um elemento."""
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            self.debug_print(f"Elemento clicado: {element_name}")
            return True
        except Exception as e:
            self.debug_print(f"Falha ao clicar em {element_name}: {str(e)}")
            return False

    def test_cenario1_registro_observacoes_simples(self):
        """
        Caso de teste para verificar o registro bem-sucedido de observações simples.
        """
        try:
            self.debug_print("\n=== CENÁRIO 1: REGISTRO SIMPLES ===")
            if not self.login_enfermeiro():
                self.fail("Falha no login")

            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/observacoes/")
            self.wait.until(EC.presence_of_element_located((By.ID, "form-observacoes")))

            textarea = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea[name='observacoes']")
                )
            )
            observacao = (
                "Paciente apresentou melhora nos sintomas. Pressão arterial 12x8."
            )
            textarea.clear()
            textarea.send_keys(observacao)
            self.debug_print("Observações preenchidas")

            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            ).click()
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            self.debug_print("Observações registradas com sucesso")

        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            self.driver.save_screenshot("erro_cenario1.png")
            raise

    def test_cenario2_sugestao_termos_medicos(self):
        """
        Caso de teste para verificar o recurso de sugestão de termos.
        """
        try:
            self.debug_print("\n=== INICIANDO CENÁRIO 2: SUGESTÃO DE TERMOS ===")

            if not self.login_enfermeiro():
                self.fail("Falha no login - verifique os logs")

            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/")

            textarea = self.wait.until(
                EC.presence_of_element_located((By.ID, "observacoes-textarea"))
            )
            textarea.send_keys("feb")
            time.sleep(1)

            sugestoes = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".sugestao-termo")
                )
            )
            self.assertGreater(len(sugestoes), 0, "Nenhuma sugestão apareceu")

            termos_esperados = ["febre", "febril", "afebril"]
            for sugestao in sugestoes:
                self.assertIn(sugestao.text.lower(), termos_esperados)

            sugestoes[0].click()
            self.assertIn("febre", textarea.get_attribute("value"))
            self.debug_print("Sugestão selecionada com sucesso")

        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            raise

    def test_cenario3_falha_registro_observacoes(self):
        """
        Caso de teste para verificar o tratamento de erros quando o registro de observações falha.
        """
        try:
            self.debug_print("\n=== INICIANDO CENÁRIO 3: FALHA NO REGISTRO ===")

            if not self.login_enfermeiro():
                self.fail("Falha no login - verifique os logs")

            self.driver.get(f"{self.base_url}/pacientes/{self.paciente_id}/")
            self.wait.until(
                EC.presence_of_element_located((By.ID, "observacoes-textarea"))
            )

            self.driver.execute_script(
                """
                document.getElementById('salvar-observacoes').remove();
                var form = document.querySelector('form');
                form.action = '/url-invalida';
            """
            )

            self.preencher_campo(
                By.ID, "observacoes-textarea", "Observação de teste", "Campo de Observações"
            )
            self.clicar_elemento(
                By.CSS_SELECTOR, "form button[type='submit']", "Botão Salvar"
            )

            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            mensagem = self.driver.find_element(By.CLASS_NAME, "alert-danger").text
            self.assertIn("Não foi possível salvar as observações", mensagem)
            self.assertIn("suporte técnico", mensagem.lower())
            self.debug_print("Mensagem de erro exibida corretamente")

        except Exception as e:
            self.debug_print(f"ERRO NO TESTE: {str(e)}")
            raise

    def tearDown(self):
        """
        Limpa após cada método de teste.
        """
        if hasattr(self, "driver"):
            try:
                self.debug_print("Finalizando navegador...")
            finally:
                self.driver.quit()
                self.debug_print("Navegador finalizado")

    @classmethod
    def tearDownClass(cls):
        """
        Limpa o ambiente de teste uma vez após toda a classe. Isso inclui:
        - Fechar o webdriver.
        - Parar o servidor de desenvolvimento Django. <-- IMPORTANTE
        - Excluir o usuário e o paciente de teste.
        """
        import subprocess

        if hasattr(cls, "driver"):
            cls.driver.quit()
        if hasattr(cls, "server_process"):
            cls.server_process.terminate()
            cls.server_process.wait()
        try:
            User = get_user_model()
            Paciente = Paciente
            User.objects.filter(email=cls.email_enfermeiro).delete()
            Paciente.objects.filter(id=cls.paciente_id).delete()
        except Exception as e:
            print(f"Error in tearDownClass: {e}")
