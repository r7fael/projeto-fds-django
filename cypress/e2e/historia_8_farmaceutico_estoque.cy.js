describe('HISTÓRIA 8: Verificação de Estoque pelo Farmacêutico', () => {
    beforeEach(() => {
        cy.login('farmaceutico@exemplo.com', 'senha123');
        cy.visit('/application/painel-farmaceutico/'); // URL corrigida
    });

    it('Cenário 1: Farmacêutico verifica a disponibilidade de medicamentos', () => {
        cy.get('.menu li[data-section="medicamentos"]').click();
        cy.get('#search-input').type('Dipirona');
        cy.get('.medicamentos-table tbody tr').first().should('contain', 'Dipirona');
    });

    it('Cenário 2: Verificação de estoque com alertas de reposição', () => {
        cy.get('.menu li[data-section="medicamentos"]').click();
        cy.get('.medicamentos-table tbody tr td.stock-low').should('exist');
    });
});