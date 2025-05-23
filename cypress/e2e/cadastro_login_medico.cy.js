describe('Fluxo de Cadastro e Login de Médico', () => {
  const uniqueEmail = `medico_${Date.now()}@teste.com`;
  const nomeCompleto = 'Dr. House Teste';
  const senha = 'senhaSuperSegura123';
  const crm = 'CRM12345SP';

  it('Deve permitir que um novo usuário médico se cadastre com sucesso', () => {

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
    cy.get('input[name="registro_profissional"]').type(crm);

    cy.get('button[type="submit"]').contains('Cadastrar').click();

    cy.url().should('include', '/users/login/');
    cy.get('h2').should('contain.text', 'Login');


  });

  it('Deve permitir que o médico recém-cadastrado faça login', () => {

    cy.visit('/users/login/'); 
    cy.get('h2').should('contain.text', 'Login');

    cy.get('input[name="email"]').type(uniqueEmail);
    cy.get('input[name="password"]').type(senha); 

    cy.get('button[type="submit"]').contains('Entrar').click();

    cy.url().should('not.include', '/users/login/');

    cy.url().should('not.contain', '/login'); 
    cy.log('Login realizado, mas a verificação de sucesso precisa ser mais específica para sua aplicação.');
  });
});