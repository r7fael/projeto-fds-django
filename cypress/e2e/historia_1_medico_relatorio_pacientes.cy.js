describe('HISTÓRIA 1: Relatório de Pacientes do Médico', () => {
    beforeEach(() => {
        cy.login('medico@exemplo.com', 'senha123');
    });

    it('Cenário 1: Visualizar a lista de pacientes tratados', () => {
        cy.visit('/application/painel-medico/');
        cy.get('.link-menu').contains('Pacientes').click();
        cy.get('#pacientes-content').should('be.visible');
        cy.get('.cartao-paciente').should('have.length.greaterThan', 0);
    });

    it('Cenário 3: Mensagem para o caso de nenhum paciente tratado', () => {
        cy.intercept('GET', '/application/painel-medico/', {
            fixture: 'painel_medico_sem_pacientes.html'
        }).as('getPainelVazio');

        cy.visit('/application/painel-medico/');

        cy.wait('@getPainelVazio');

        cy.get('.link-menu').contains('Pacientes').click();
        
        cy.get('.sem-resultados').should('contain.text', 'Nenhum paciente cadastrado');
    });
});