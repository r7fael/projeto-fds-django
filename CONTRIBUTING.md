# Contribuindo com o VitalHub 💙💚

Obrigado por se interessar em contribuir com o **VitalHub**!
Este é um projeto desenvolvido com **Django** e tem como objetivo aplicar boas práticas de autenticação de usuários e renderização de templates com fundo artístico azul/verde. Abaixo você encontrará todas as orientações necessárias para colaborar com qualidade e segurança.

---

## 🧰 Pré-requisitos

Certifique-se de ter os seguintes itens instalados e configurados na sua máquina antes de começar:

* **Python 3.10** ou superior
* **Django 5.x**
* **Git**
* **SQLite** (banco de dados usado no projeto)

### Criar ambiente virtual:

```bash
python -m venv venv
```

### Ativar o ambiente virtual:

* No Windows:

  ```bash
  venv\Scripts\activate
  ```
* No Linux/macOS:

  ```bash
  source venv/bin/activate
  ```

### Instalar as dependências:

```bash
pip install -r requirements.txt
```

### Aplicar as migrações do banco de dados:

```bash
python manage.py migrate
```

### Rodar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

---

## 🧑‍💻 Como contribuir

1. **Faça um fork** deste repositório no GitHub.
2. **Clone o fork para sua máquina local**:

   ```bash
   git clone https://github.com/seu-usuario/vitalhub.git
   cd vitalhub
   ```
3. **Crie uma branch nova** para sua contribuição:

   ```bash
   git checkout -b minha-feature
   ```
4. **Faça suas alterações**, testando localmente.
5. **Adicione e commite suas mudanças**:

   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
6. **Envie sua branch para o seu fork**:

   ```bash
   git push origin minha-feature
   ```
7. **Abra um Pull Request (PR)** no repositório original com um título claro e uma descrição explicativa.

---

## 🧼 Padrões de código

Por favor, siga estas boas práticas ao escrever código:

* Respeite o estilo **PEP8** para Python.
* Use nomes de variáveis e funções **claros e descritivos**.
* **Adicione comentários** em trechos complexos ou que possam gerar dúvidas.
* Mantenha a **estrutura de pastas do Django**.
* Os templates HTML devem seguir o visual com **fundo artístico azul/verde** padrão do projeto.
* Sempre que possível, adicione **testes** ou verifique se funcionalidades existentes continuam funcionando.

---

## 🐞 Abertura de issues

Se quiser relatar um erro ou sugerir melhorias:

* Abra uma **issue** com título claro e objetivo.
* Descreva o problema ou sugestão com detalhes.
* Se for bug, inclua:

  * Passos para reproduzir o erro
  * Prints ou mensagens de erro
  * Informações do ambiente (navegador, sistema operacional, etc.)

---

## 🔀 Pull Requests

* Envie PRs para a **branch `main`**.
* Descreva o que foi feito, por que foi feito e como testar.
* Relacione a **issue** correspondente (se houver) usando `Closes #número-da-issue`.
* Evite misturar funcionalidades diferentes em um único PR.
* PRs que não seguirem essas orientações podem ser solicitados para ajustes.

---

## 💬 Contato

Tem dúvidas antes de começar?
Abra uma **issue com a tag `pergunta`** ou entre em contato diretamente com os mantenedores do projeto.

---

Muito obrigado por contribuir com o **VitalHub**! 💙💚
Sua colaboração faz toda a diferença. 🚀