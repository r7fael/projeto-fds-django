describe('Paciente - Acesso ao Prontuário Eletrônico', () => {
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

  let emailMedicoCriado, medicoNomeCompleto, medicoSenha, medicoRegistro;
  let emailEnfermeiroCriado, enfermeiroNomeCompleto, enfermeiroSenha, enfermeiroRegistro;
  let pacienteNomeCriado, pacienteCpfCriado, pacienteDataNascimentoCriada;
  let textoMedicacaoPeloMedico, tipoObservacaoPeloProfissional, textoObservacaoPeloProfissional;
  let dataConsulta, descricaoConsulta;

  beforeEach(() => {
    medicoNomeCompleto = 'Dr. House Prontuario';
    medicoSenha = 'password123';
    medicoRegistro = 'CRM99900SP';
    emailMedicoCriado = generateUniqueEmail('dr.house.prontuario@vitalhub.com');

    enfermeiroNomeCompleto = 'Enf. Florence Prontuario';
    enfermeiroSenha = 'password123';
    enfermeiroRegistro = 'COREN99900SP';
    emailEnfermeiroCriado = generateUniqueEmail('enf.florence.prontuario@vitalhub.com');

    pacienteNomeCriado = 'Carlos Daniel Paciente Prontuario';
    pacienteCpfCriado = generateUniqueCpf();
    pacienteDataNascimentoCriada = '1980-05-15';

    textoMedicacaoPeloMedico = 'Amoxicilina 500mg - 1 cápsula a cada 8 horas por 7 dias.';
    tipoObservacaoPeloProfissional = 'Evolução';
    textoObservacaoPeloProfissional = 'Paciente refere melhora progressiva do quadro geral. Afebril.';
    dataConsulta = new Date().toISOString().split('T')[0];
    descricaoConsulta = 'Consulta de rotina e acompanhamento.';

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.get('input[name="email"]').type(emailMedicoCriado);
    cy.get('input[name="nome_completo"]').type(medicoNomeCompleto);
    cy.get('input[name="senha"]').type(medicoSenha);
    cy.get('input[name="confirmar_senha"]').type(medicoSenha);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(medicoRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
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

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Paciente')
      .click();
    cy.get('section#cadastro-content input[name="nome_completo"]').type(pacienteNomeCriado);
    cy.get('section#cadastro-content input[name="cpf"]').type(pacienteCpfCriado);
    cy.get('section#cadastro-content input[name="data_nascimento"]').type(pacienteDataNascimentoCriada);
    cy.get('section#cadastro-content select[name="medico_responsavel"]').select(medicoNomeCompleto);
    cy.get('section#cadastro-content button[type="submit"]').contains('Cadastrar').click();
    cy.get('div.mensagens .alerta.success').should('contain.text', 'Paciente cadastrado com sucesso');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Consulta')
      .click();
    cy.get('section#consultas-content select[name="paciente"]').select(pacienteNomeCriado);
    cy.get('section#consultas-content select[name="medico"]').select(medicoNomeCompleto);
    cy.get('section#consultas-content input[name="data"]').type(dataConsulta);
    cy.get('section#consultas-content textarea[name="descricao"]').type(descricaoConsulta);
    cy.get('section#consultas-content button[type="submit"]').contains('Cadastrar Consulta').click();

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();
    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeCriado)
      .parents('.cartao-paciente')
      .find('button.botao-dropdown')
      .click();
    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeCriado)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('select[name="tipo"]').select(tipoObservacaoPeloProfissional);
        cy.get('textarea[name="observacao"]').type(textoObservacaoPeloProfissional);
        cy.get('button.botao-adicionar-observacao').click();
      });
    cy.get('div.mensagens .alerta.success').should('contain.text', 'Observação adicionada com sucesso');

    cy.visit('/users/login/');
    cy.get('input[name="email"]').type(emailMedicoCriado);
    cy.get('input[name="password"]').type(medicoSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();
    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeCriado)
      .parents('.cartao-paciente')
      .find('button.botao-dropdown')
      .click();
    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteNomeCriado)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('textarea[name="medicamentos"]').clear().type(textoMedicacaoPeloMedico);
        cy.get('button.botao-salvar').contains('Salvar').click();
      });
  });

  it('deve permitir ao paciente acessar seu prontuário e verificar informações', () => {
    cy.visit('/');
    cy.contains('a.btn.btn-paciente', 'Sou Paciente (Consultar Prontuário)').click();

    cy.get('input[name="cpf"]').type(pacienteCpfCriado);
    cy.get('input[name="data_nascimento"]').type(pacienteDataNascimentoCriada);
    cy.get('button.btn-submit').contains('Consultar').click();

    cy.contains('h1', 'VitalHub - Resumo do Prontuário');
    cy.get('.info-grid').should('contain.text', pacienteNomeCriado);

    cy.contains('h2.section-title', 'Medicamentos Prescritos')
      .next('.medicamentos-info')
      .should('contain.text', textoMedicacaoPeloMedico);

    cy.contains('h2.section-title', 'Últimas Observações de Saúde')
      .next('ul.observacoes-list')
      .find('.observacao-item')
      .first()
      .should('contain.text', textoObservacaoPeloProfissional)
      .and('contain.text', tipoObservacaoPeloProfissional);
  });
});