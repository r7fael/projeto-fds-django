describe('HISTÓRIA 6: Quantidade de Pacientes no Andar', () => {
    beforeEach(() => {
        cy.login('enfermeiro@exemplo.com', 'senha123');
        cy.visit('/application/painel-enfermeiro/'); 
    });

    it('Cenário 1: Enfermeiro visualiza a quantidade de pacientes no andar', () => {
        cy.get('.link-menu').contains('Controle de Andares').click();
        cy.get('#andares-content').should('be.visible');
        cy.get('.card-resumo').should('contain.text', 'Quartos Ocupados:');
    });
});