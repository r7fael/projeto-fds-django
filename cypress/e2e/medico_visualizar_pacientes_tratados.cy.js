describe('Painel do Médico - Visualizar Pacientes Tratados', () => {
  const generateUniqueEmail = (baseEmail) => {
    const timestamp = Date.now();
    return `${baseEmail.split('@')[0]}+${timestamp}@${baseEmail.split('@')[1]}`;
  };

  const medicoBaseEmailParaEsteTeste = 'dr.house.painel.teste@vitalhub.com';
  const medicoNomeCompletoParaEsteTeste = 'Dr. House Painel Test';
  const medicoSenhaParaEsteTeste = 'password123';
  const medicoRegistroParaEsteTeste = 'CRM77777SP';
  let emailMedicoCriadoParaTeste;

  beforeEach(() => {
    emailMedicoCriadoParaTeste = generateUniqueEmail(medicoBaseEmailParaEsteTeste);

    cy.visit('/');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.url().should('include', '/users/cadastrar/');

    cy.get('input[name="email"]').type(emailMedicoCriadoParaTeste);
    cy.get('input[name="nome_completo"]').type(medicoNomeCompletoParaEsteTeste);
    cy.get('input[name="senha"]').type(medicoSenhaParaEsteTeste);
    cy.get('input[name="confirmar_senha"]').type(medicoSenhaParaEsteTeste);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(medicoRegistroParaEsteTeste);
    cy.get('button[type="submit"]').contains('Cadastrar').click();

    cy.url().should('include', '/users/login/');

    cy.get('input[name="email"]').type(emailMedicoCriadoParaTeste);
    cy.get('input[name="password"]').type(medicoSenhaParaEsteTeste);
    cy.get('button[type="submit"]').contains('Entrar').click();

    cy.get('h1.titulo-pagina').should('contain.text', 'Bem-vindo(a)');
  });

  it('Deve permitir ao médico visualizar o número de pacientes tratados durante o plantão na seção Pacientes', () => {
    cy.get('aside.coluna-menu-lateral .lista-navegacao .item-menu a')
      .contains('Pacientes')
      .click();

    cy.get('a.link-menu.ativo').should('contain.text', 'Pacientes');
    cy.get('section#pacientes-content').should('be.visible');
    cy.get('section#home-content').should('not.be.visible');
    cy.get('h1#titulo-pagina').should('have.text', 'Pacientes');
  });
});