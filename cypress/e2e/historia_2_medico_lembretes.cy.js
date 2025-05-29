describe('HISTÓRIA 2: Lembretes de Acompanhamento para Médico', () => {
    beforeEach(() => {
        cy.login('medico@exemplo.com', 'senha123');
        cy.visit('/application/painel-medico/'); 
    });

    it('Cenário 1: Médico recebe lembretes sobre pacientes que precisam de acompanhamento', () => {
        cy.get('#home-content').should('be.visible');
        cy.get('.lista-resumo-notificacoes .item-resumo')
          .contains('paciente(s) precisam de retorno')
          .should('be.visible');
    });
});