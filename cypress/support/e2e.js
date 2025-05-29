// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/users/login/'); 
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password, { log: false });
    cy.get('button[type="submit"]').click();

    cy.url().should('not.include', '/login');
  });
});

Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/users/login/');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="password"]').type(password, { log: false });
    cy.get('button[type="submit"]').click();
    cy.url().should('not.include', '/login');
  });
});

Cypress.Commands.add('cadastrarProfissional', (email, nome, senha, tipoUsuario, registroProfissional) => {
  cy.visit('/users/cadastrar/');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="nome_completo"]').type(nome);
  cy.get('input[name="senha"]').type(senha);
  cy.get('input[name="confirmar_senha"]').type(senha);
  cy.get('select[name="tipo_usuario"]').select(tipoUsuario.toLowerCase());
  cy.get('input[name="registro_profissional"]').type(registroProfissional);
  cy.get('button[type="submit"]').contains('Cadastrar').click();
  cy.url().should('include', '/users/login/');
  cy.log(`${tipoUsuario} ${nome} cadastrado(a).`);
});

Cypress.Commands.add('cadastrarPaciente', (nomePaciente, cpf, dataNascimento, nomeMedicoResponsavel) => {
  cy.visit('/application/cadastrar-paciente/'); 
  cy.get('h2, h1').should(Cypress._.partialRight(Cypress.sinon.match.string, /cadastrar paciente/i))


  cy.get('input[name="nome_completo"]').type(nomePaciente);
  cy.get('input[name="cpf"]').type(cpf);
  cy.get('input[name="data_nascimento"]').type(dataNascimento);
  
  cy.get('select[name="medico_responsavel"]').select(nomeMedicoResponsavel);
  
  cy.get('button[type="submit"]').contains('Cadastrar', { matchCase: false }).click();

  cy.url().should('not.include', '/cadastrar-paciente'); 
  cy.log(`Paciente ${nomePaciente} cadastrado.`);
});