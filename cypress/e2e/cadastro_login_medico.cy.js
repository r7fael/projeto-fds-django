describe('Fluxo de Cadastro e Login de Médico', () => {

  it('deve cadastrar um novo médico e permitir que ele faça login em seguida', () => {
    const timestamp = Date.now();
    const uniqueEmail = `medico_${timestamp}@teste.com`;
    const nomeCompleto = 'Dr. House Teste';
    const senha = 'senhaSuperSegura123';
    const uniqueCrm = `CRM${timestamp.toString().slice(-6)}`;

    cy.visit('/');
    cy.contains('h1', 'VitalHub').should('be.visible');
    cy.contains('a.btn', 'Cadastro Profissionais').click();
    cy.url().should('include', '/users/cadastrar/');
    cy.get('h2').should('contain.text', 'Cadastro de Usuário');

    cy.get('input[name="email"]').type(uniqueEmail);
    cy.get('input[name="nome_completo"]').type(nomeCompleto);
    cy.get('input[name="senha"]').type(senha);
    cy.get('input[name="confirmar_senha"]').type(senha);
    cy.get('select[name="tipo_usuario"]').select('medico');
    cy.get('input[name="registro_profissional"]').type(uniqueCrm);
    cy.get('button[type="submit"]').contains('Cadastrar').click();

    cy.url().should('include', '/users/login/');
    cy.get('h2').should('contain.text', 'Login');
    cy.get('input[name="email"]').type(uniqueEmail);
    cy.get('input[name="password"]').type(senha); 
    cy.get('button[type="submit"]').contains('Entrar').click();

    cy.url().should('include', '/application/painel-medico/');
    cy.get('h1').should('contain.text', `Bem-vindo(a), ${nomeCompleto}`);
  });

});