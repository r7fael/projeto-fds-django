# pacientes/tests.py
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestEnfermeiroPaciente(StaticLiveServerTestCase):  # Nome simplificado
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_cadastro_fluxo_completo(self):
        try:
            print("\n=== INICIANDO TESTE ===")
            self.driver.get(f"{self.live_server_url}/")
            time.sleep(2)  # Apenas para visualização
            print("Página inicial carregada com sucesso")
        except Exception as e:
            print(f"ERRO: {str(e)}")
            raise