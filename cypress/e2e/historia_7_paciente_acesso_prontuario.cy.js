describe('HISTÓRIA 7: Acesso do Paciente ao Prontuário', () => {
    it('Cenário 1: Paciente acessa seu prontuário eletrônico', () => {
        cy.visit('/');
        cy.get('a.btn-paciente').contains('Sou Paciente').click();
        cy.get('input[name="cpf"]').type('896.172.744-34');
        cy.get('input[name="data_nascimento"]').type('2000-05-22');
        cy.get('button[type="submit"]').click();
        cy.url().should('include', '/prontuario/');
        cy.get('h2').contains('Dados do Paciente').should('be.visible');
        cy.get('.medicamentos-info').should('be.visible');
    });
});