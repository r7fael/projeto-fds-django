describe('Enfermeiro - Cadastro de Paciente', () => {
  const generateUniqueEmail = (baseEmail) => {
    const timestamp = Date.now();
    return `${baseEmail.split('@')[0]}+${timestamp}@${baseEmail.split('@')[1]}`;
  };

  const generateUniqueCpf = () => {
    let cpf = '';
    for (let i = 0; i < 11; i++) {
      cpf += Math.floor(Math.random() * 10);
    }
    return cpf;
  };

  const enfermeiroBaseEmail = 'enf.cadastro.paciente.v2@vitalhub.com';
  const enfermeiroNomeCompleto = 'Enfermeira Teste Cadastro Paciente v2';
  const enfermeiroSenha = 'password123';
  const enfermeiroRegistro = 'COREN12345SP';
  let emailEnfermeiroCriado;

  const pacienteNome = 'Carlos Almeida Paciente Teste';
  let pacienteCpfUnico;
  const pacienteDataNascimento = '1992-08-25';

  beforeEach(() => {
    emailEnfermeiroCriado = generateUniqueEmail(enfermeiroBaseEmail);
    pacienteCpfUnico = generateUniqueCpf();

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.url().should('include', '/users/cadastrar/');

    cy.get('input[name="email"]').type(emailEnfermeiroCriado);
    cy.get('input[name="nome_completo"]').type(enfermeiroNomeCompleto);
    cy.get('input[name="senha"]').type(enfermeiroSenha);
    cy.get('input[name="confirmar_senha"]').type(enfermeiroSenha);
    cy.get('select[name="tipo_usuario"]').select('enfermeiro');
    cy.get('input[name="registro_profissional"]').type(enfermeiroRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();

    cy.url().should('include', '/users/login/');

    cy.get('input[name="email"]').type(emailEnfermeiroCriado);
    cy.get('input[name="password"]').type(enfermeiroSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();

    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');
  });

  it('deve permitir ao enfermeiro cadastrar um novo paciente', () => {
    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Paciente')
      .click();

    cy.get('a.link-menu.ativo').should('contain.text', 'Cadastrar Paciente');
    cy.get('section#cadastro-content').should('be.visible');
    cy.get('h1#titulo-pagina').should('have.text', 'Cadastro');

    cy.get('section#cadastro-content input[name="nome_completo"]').type(pacienteNome);
    cy.get('section#cadastro-content input[name="cpf"]').type(pacienteCpfUnico);
    cy.get('section#cadastro-content input[name="data_nascimento"]').type(pacienteDataNascimento);

    cy.get('section#cadastro-content select[name="medico_responsavel"]')
      .find('option')
      .not('[value=""]')
      .first()
      .then(firstValidOption => {
        cy.get('section#cadastro-content select[name="medico_responsavel"]').select(firstValidOption.val());
      });

    cy.get('section#cadastro-content button[type="submit"]').contains('Cadastrar').click();

    cy.get('div.mensagens .alerta.success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Paciente cadastrado com sucesso');
  });
});