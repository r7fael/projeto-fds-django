describe('Setup Inicial de Usuários de Teste', () => {
  before(() => {
    cy.log('Iniciando cadastro de Médico...');
    cy.cadastrarProfissional(
      'medico@exemplo.com',
      'Pedro Garcez',
      'senha123',
      'Médico',
      'CRM/PE 123456'
    );

    cy.log('Iniciando cadastro de Enfermeiro...');
    cy.cadastrarProfissional(
      'enfermeiro@exemplo.com',
      'Clarissa Oliveira',
      'senha123',
      'Enfermeiro',
      'Coren-PE 1234567-TEC'
    );

    cy.log('Iniciando cadastro de Farmacêutico...');
    cy.cadastrarProfissional(
      'farmaceutico@exemplo.com',
      'Rafael Padilha',
      'senha123',
      'Farmacêutico',
      '12345 PE'
    );

    cy.log('Logando como Enfermeiro para cadastrar paciente...');
    cy.login('enfermeiro@exemplo.com', 'senha123'); 
    
    cy.cadastrarPaciente(
      'Daniel Alves',
      '108.457.789-49',
      '2006-03-10',
      'Pedro Garcez'
    );
  });

  it('Verifica se o setup de usuários foi concluído', () => {
    cy.log('Setup de usuários concluído com sucesso!');
    expect(true).to.equal(true);
  });
});