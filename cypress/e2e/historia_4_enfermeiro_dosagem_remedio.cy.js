describe('HISTÓRIA 4: Verificação de Dosagem pelo Enfermeiro', () => {
    beforeEach(() => {
        cy.login('enfermeiro@exemplo.com', 'senha123');
        cy.visit('/application/painel-enfermeiro/'); 
    });

    it('Cenário 1: Enfermeiro verifica a dosagem correta do remédio', () => {
        cy.get('.link-menu').contains('Pacientes').click();
        cy.get('.cartao-paciente').first().within(() => {
            cy.get('.botao-dropdown').click();
            cy.get('.lista-medicamentos').should('contain.text', 'Dipirona');
        });
    });
});