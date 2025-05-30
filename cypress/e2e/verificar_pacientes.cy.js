describe('Painel do Médico - Visualizar Histórico do Paciente com Paciente Atribuído', () => {
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

  const medicoAlvoBaseEmail = 'dr.alvo.hist@vitalhub.com';
  const medicoAlvoNomeCompleto = 'Dr. Alvo Para Historico';
  const medicoAlvoSenha = 'password123';
  const medicoAlvoRegistro = 'CRM33300SP';
  let emailMedicoAlvoCriado;

  const enfermeiroHelperBaseEmail = 'enf.helper.hist@vitalhub.com';
  const enfermeiroHelperNomeCompleto = 'Enfermeira Helper Para Historico';
  const enfermeiroHelperSenha = 'password123';
  const enfermeiroHelperRegistro = 'COREN44400SP';
  let emailEnfermeiroHelperCriado;

  const pacienteNomeParaHistorico = 'Paciente Exemplo Para Historico';
  let pacienteCpfUnicoParaHistorico;
  const pacienteDataNascimentoParaHistorico = '1998-07-12';

  beforeEach(() => {
    emailMedicoAlvoCriado = generateUniqueEmail(medicoAlvoBaseEmail);
    emailEnfermeiroHelperCriado = generateUniqueEmail(enfermeiroHelperBaseEmail);
    pacienteCpfUnicoParaHistorico = generateUniqueCpf();

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.url().should('include', '/users/cadastrar/');
    cy.get('input[name="email"]').type(emailMedicoAlvoCriado);
    cy.get('input[name="nome_completo"]').type(medicoAlvoNomeCompleto);
    cy.get('input[name="senha"]').type(medicoAlvoSenha);
    cy.get('input[name="confirmar_senha"]').type(medicoAlvoSenha);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(medicoAlvoRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.url().should('include', '/users/cadastrar/');
    cy.get('input[name="email"]').type(emailEnfermeiroHelperCriado);
    cy.get('input[name="nome_completo"]').type(enfermeiroHelperNomeCompleto);
    cy.get('input[name="senha"]').type(enfermeiroHelperSenha);
    cy.get('input[name="confirmar_senha"]').type(enfermeiroHelperSenha);
    cy.get('select[name="tipo_usuario"]').select('enfermeiro');
    cy.get('input[name="registro_profissional"]').type(enfermeiroHelperRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.get('input[name="email"]').type(emailEnfermeiroHelperCriado);
    cy.get('input[name="password"]').type(enfermeiroHelperSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Paciente')
      .click();
    cy.get('section#cadastro-content').should('be.visible');
    cy.get('h1#titulo-pagina').should('have.text', 'Cadastro');

    cy.get('section#cadastro-content input[name="nome_completo"]').type(pacienteNomeParaHistorico);
    cy.get('section#cadastro-content input[name="cpf"]').type(pacienteCpfUnicoParaHistorico);
    cy.get('section#cadastro-content input[name="data_nascimento"]').type(pacienteDataNascimentoParaHistorico);
    cy.get('section#cadastro-content select[name="medico_responsavel"]').select(medicoAlvoNomeCompleto);
    cy.get('section#cadastro-content button[type="submit"]').contains('Cadastrar').click();
    cy.get('div.mensagens .alerta.success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Paciente cadastrado com sucesso');

    cy.visit('/users/login/');
    cy.get('input[name="email"]').type(emailMedicoAlvoCriado);
    cy.get('input[name="password"]').type(medicoAlvoSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');
  });

  it('deve permitir ao médico navegar para seção pacientes e clicar em ver mais de um paciente atribuído', () => {
    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();

    cy.get('a.link-menu.ativo').should('contain.text', 'Pacientes');
    cy.get('section#pacientes-content').should('be.visible');
    cy.get('h1#titulo-pagina').should('have.text', 'Pacientes');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeParaHistorico)
      .should('be.visible');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeParaHistorico)
      .parents('.cartao-paciente')
      .find('.botao-dropdown')
      .click();
  });
});