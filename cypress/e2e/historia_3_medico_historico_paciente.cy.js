describe('HISTÓRIA 3: Histórico do Paciente', () => {
    beforeEach(() => {
        cy.login('medico@exemplo.com', 'senha123');
        cy.visit('/application/painel-medico/'); 
    });

    it('Cenário 1: Médico visualiza detalhes e medicamentos de um paciente', () => {
        cy.get('.link-menu').contains('Pacientes').click();
        cy.get('.cartao-paciente').first().within(() => {
            cy.get('.botao-dropdown').click();
            cy.get('.dropdown-info').should('be.visible').and('contain.text', 'CPF:');
            cy.get('.secao-medicamentos').should('be.visible');
        });
    });
});