describe('Enfermeiro - Verificar Dosagem de Medicação Prescrita', () => {
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

  const medicoPrescritorBaseEmail = 'dr.prescritor.dosagem@vitalhub.com';
  const medicoPrescritorNomeCompleto = 'Dr. Prescritor Dosagem Teste';
  const medicoPrescritorSenha = 'password123';
  const medicoPrescritorRegistro = 'CRM55500SP';
  let emailMedicoPrescritorCriado;

  const enfermeiroPrincipalBaseEmail = 'enf.principal.dosagem@vitalhub.com';
  const enfermeiroPrincipalNomeCompleto = 'Enfermeiro Principal Dosagem Teste';
  const enfermeiroPrincipalSenha = 'password123';
  const enfermeiroPrincipalRegistro = 'COREN66600SP';
  let emailEnfermeiroPrincipalCriado;

  const pacienteAlvoNome = 'Joana Paciente Dosagem Teste';
  let pacienteAlvoCpfUnico;
  const pacienteAlvoDataNascimento = '1988-02-10';

  const nomeMedicamento = 'Paracetamol';
  const dosagemMedicamento = '750mg de 6 em 6 horas';
  const observacaoPrescricao = `Prescrito ${nomeMedicamento} ${dosagemMedicamento} em caso de dor ou febre.`;
  const tipoObservacaoPrescricao = 'Prescrição Médica';

  beforeEach(() => {
    emailMedicoPrescritorCriado = generateUniqueEmail(medicoPrescritorBaseEmail);
    emailEnfermeiroPrincipalCriado = generateUniqueEmail(enfermeiroPrincipalBaseEmail);
    pacienteAlvoCpfUnico = generateUniqueCpf();

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.get('input[name="email"]').type(emailMedicoPrescritorCriado);
    cy.get('input[name="nome_completo"]').type(medicoPrescritorNomeCompleto);
    cy.get('input[name="senha"]').type(medicoPrescritorSenha);
    cy.get('input[name="confirmar_senha"]').type(medicoPrescritorSenha);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(medicoPrescritorRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.get('input[name="email"]').type(emailEnfermeiroPrincipalCriado);
    cy.get('input[name="nome_completo"]').type(enfermeiroPrincipalNomeCompleto);
    cy.get('input[name="senha"]').type(enfermeiroPrincipalSenha);
    cy.get('input[name="confirmar_senha"]').type(enfermeiroPrincipalSenha);
    cy.get('select[name="tipo_usuario"]').select('enfermeiro');
    cy.get('input[name="registro_profissional"]').type(enfermeiroPrincipalRegistro);
    cy.get('button[type="submit"]').contains('Cadastrar').click();
    cy.url().should('include', '/users/login/');

    cy.get('input[name="email"]').type(emailEnfermeiroPrincipalCriado);
    cy.get('input[name="password"]').type(enfermeiroPrincipalSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Cadastrar Paciente')
      .click();
    cy.get('section#cadastro-content').should('be.visible');

    cy.get('section#cadastro-content input[name="nome_completo"]').type(pacienteAlvoNome);
    cy.get('section#cadastro-content input[name="cpf"]').type(pacienteAlvoCpfUnico);
    cy.get('section#cadastro-content input[name="data_nascimento"]').type(pacienteAlvoDataNascimento);
    cy.get('section#cadastro-content select[name="medico_responsavel"]').select(medicoPrescritorNomeCompleto);
    cy.get('section#cadastro-content button[type="submit"]').contains('Cadastrar').click();
    cy.get('div.mensagens .alerta.success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Paciente cadastrado com sucesso');

    cy.visit('/users/login/');
    cy.get('input[name="email"]').type(emailMedicoPrescritorCriado);
    cy.get('input[name="password"]').type(medicoPrescritorSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();
    cy.get('section#pacientes-content').should('be.visible');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteAlvoNome)
      .parents('.cartao-paciente')
      .find('.botao-dropdown')
      .click();

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteAlvoNome)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('textarea[name="medicamentos"]').clear().type(observacaoPrescricao);
        cy.get('button.botao-salvar').contains('Salvar').click();
      });
  });

  it('deve permitir ao enfermeiro visualizar a dosagem correta do remédio para o paciente', () => {
    cy.visit('/users/login/');
    cy.get('input[name="email"]').type(emailEnfermeiroPrincipalCriado);
    cy.get('input[name="password"]').type(enfermeiroPrincipalSenha);
    cy.get('button[type="submit"]').contains('Entrar').click();
    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');

    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();
    cy.get('section#pacientes-content').should('be.visible');

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteAlvoNome)
      .parents('.cartao-paciente')
      .find('.botao-dropdown')
      .click();

    cy.contains('section#pacientes-content .cartao-paciente .nome-paciente', pacienteAlvoNome)
      .parents('.cartao-paciente')
      .within(() => {
        cy.get('div.secao-medicamentos div.lista-medicamentos')
            .should('contain.text', nomeMedicamento)
            .and('contain.text', dosagemMedicamento);

      });
  });
});