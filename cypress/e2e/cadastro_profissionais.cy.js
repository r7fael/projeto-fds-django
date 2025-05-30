describe('Cadastro de Profissionais Essenciais', () => {
  const generateUniqueEmail = (baseEmail) => {
    const timestamp = Date.now();
    return `${baseEmail.split('@')[0]}+${timestamp}@${baseEmail.split('@')[1]}`;
  };

  const profissionais = [
    {
      tipo: 'medico',
      nomeCompleto: 'Dr. House Teste',
      emailBase: 'dr.house.teste@vitalhub.com',
      senha: 'password123',
      confirmarSenha: 'password123',
      registroProfissional: 'CRM12345SP',
      urlEsperadaPosCadastro: '/users/login/', 
      mensagemSucessoEsperada: 'Login', 
    },
    {
      tipo: 'enfermeiro',
      nomeCompleto: 'Enf. Florence Teste',
      emailBase: 'enf.florence.teste@vitalhub.com',
      senha: 'password123',
      confirmarSenha: 'password123',
      registroProfissional: 'COREN67890RJ',
      urlEsperadaPosCadastro: '/users/login/',
      mensagemSucessoEsperada: 'Login',
    },
    {
      tipo: 'farmaceutico',
      nomeCompleto: 'Farm. Walter Teste',
      emailBase: 'farm.walter.teste@vitalhub.com',
      senha: 'password123',
      confirmarSenha: 'password123',
      registroProfissional: 'CRF11223MG',
      urlEsperadaPosCadastro: '/users/login/',
      mensagemSucessoEsperada: 'Login',
    },
  ];

  profissionais.forEach((profissional) => {
    it(`Deve cadastrar um ${profissional.tipo} com sucesso`, () => {
      const emailUnico = generateUniqueEmail(profissional.emailBase);

      cy.visit('/');
      cy.contains('a.btn', 'Cadastro Profissionais').click();

      cy.url().should('include', '/users/cadastrar/'); 
      cy.contains('h2', 'Cadastro de Usuário').should('be.visible');

      cy.get('input[name="email"]').type(emailUnico);
      cy.get('input[name="nome_completo"]').type(profissional.nomeCompleto);
      cy.get('input[name="senha"]').type(profissional.senha);
      cy.get('input[name="confirmar_senha"]').type(profissional.confirmarSenha);
      cy.get('select[name="tipo_usuario"]').select(profissional.tipo);
      cy.get('input[name="registro_profissional"]').type(profissional.registroProfissional);

      cy.get('button[type="submit"]').contains('Cadastrar').click();


      cy.url().should('include', profissional.urlEsperadaPosCadastro);
      if (profissional.mensagemSucessoEsperada) {
        cy.contains('h2', profissional.mensagemSucessoEsperada).should('be.visible');
      }

      cy.get('.messages li').should('not.exist');
    });
  });
});