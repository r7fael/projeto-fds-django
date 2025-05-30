describe('Enfermeiro - Registrar Observação do Paciente', () => {
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

  const medicoResponsavelBaseEmail = 'dr.resp.obs@vitalhub.com';
  const medicoResponsavelNomeCompleto = 'Dr. Responsavel Observacao';
  const medicoResponsavelSenha = 'password123';
  const medicoResponsavelRegistro = 'CRM77700SP';
  let emailMedicoResponsavelCriado;

  const enfermeiroObservadorBaseEmail = 'enf.obs.pac@vitalhub.com';
  const enfermeiroObservadorNomeCompleto = 'Enfermeiro Observador Paciente';
  const enfermeiroObservadorSenha = 'password123';
  const enfermeiroObservadorRegistro = 'COREN88800SP';
  let emailEnfermeiroObservadorCriado;

  const pacienteParaObservacaoNome = 'Mario Andrade Observacao';
  let pacienteParaObservacaoCpfUnico;
  const pacienteParaObservacaoDataNascimento = '1975-11-30';

  const tipoObservacaoTexto = 'Geral';
  const textoDaObservacao = 'Paciente apresentou PA: 120/80 mmHg, FC: 75 bpm, Temp: 36.5°C. Refere bem-estar.';

  beforeEach(() => {
    emailMedicoResponsavelCriado = generateUniqueEmail(medicoResponsavelBaseEmail);
    emailEnfermeiroObservadorCriado = generateUniqueEmail(enfermeiroObservadorBaseEmail);
    pacienteParaObservacaoCpfUnico = generateUniqueCpf();

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.get('input[name="email"]').type(emailMedicoResponsavelCriado);
    cy.get('input[name="nome_completo"]').type(medicoResponsavelNomeCompleto);
    cy.get('input[name="senha"]').type(medicoResponsavelSenha);
    cy.get('input[name="confirmar_senha"]').type(medicoResponsavelSenha);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(medicoResponsavelRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.get('input[name="email"]').type(emailEnfermeiroObservadorCriado);
    cy.get('input[name="nome_completo"]').type(enfermeiroObservadorNomeCompleto);
    cy.get('input[name="senha"]').type(enfermeiroObservadorSenha);
    cy.get('input[name="confirmar_senha"]').type(enfermeiroObservadorSenha);
    cy.get('select[name="tipo_usuario"]').select('enfermeiro');
    cy.get('input[name="registro_profissional"]').type(enfermeiroObservadorRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.get('input[name="email"]').type(emailEnfermeiroObservadorCriado);
    cy.get('input[name="password"]').type(enfermeiroObservadorSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Paciente')
      .click();
    cy.get('section#cadastro-content').should('be.visible');

    cy.get('section#cadastro-content input[name="nome_completo"]').type(pacienteParaObservacaoNome);
    cy.get('section#cadastro-content input[name="cpf"]').type(pacienteParaObservacaoCpfUnico);
    cy.get('section#cadastro-content input[name="data_nascimento"]').type(pacienteParaObservacaoDataNascimento);
    cy.get('section#cadastro-content select[name="medico_responsavel"]').select(medicoResponsavelNomeCompleto);
    cy.get('section#cadastro-content button[type="submit"]').contains('Cadastrar').click();
    cy.get('div.mensagens .alerta.success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Paciente cadastrado com sucesso');
  });

  it('deve permitir ao enfermeiro registrar uma observação para o paciente e visualizá-la', () => {
    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();
    cy.get('section#pacientes-content').should('be.visible');
    cy.get('h1#titulo-pagina').should('have.text', 'Pacientes');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteParaObservacaoNome)
      .parents('.cartao-paciente')
      .find('button.botao-dropdown')
      .click();

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteParaObservacaoNome)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('select[name="tipo"]').select(tipoObservacaoTexto);
        cy.get('textarea[name="observacao"]').type(textoDaObservacao);
        cy.get('button.botao-adicionar-observacao').click();
      });

    cy.get('div.mensagens .alerta.success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Observação adicionada com sucesso');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteParaObservacaoNome)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('.observacao-item').first().as('primeiraObservacao');
        cy.get('@primeiraObservacao').find('.observacao-tipo').should('contain.text', tipoObservacaoTexto);
        cy.get('@primeiraObservacao').find('.observacao-texto').should('contain.text', textoDaObservacao);
      });
  });
});