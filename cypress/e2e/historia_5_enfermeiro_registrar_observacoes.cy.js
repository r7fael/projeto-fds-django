describe('HISTÓRIA 5: Registro de Observações pelo Enfermeiro', () => {
    beforeEach(() => {
        cy.login('enfermeiro@exemplo.com', 'senha123');
        cy.visit('/application/painel-enfermeiro/'); 
    });

    it('Cenário 1: Enfermeiro registra observações', () => {
        cy.get('.link-menu').contains('Pacientes').click();
        cy.get('.cartao-paciente').first().within(() => {
            cy.get('.botao-dropdown').click();
              cy.get('select[name="tipo"]').select('Geral');
            cy.get('textarea[name="observacao"]').type('Paciente estável, pressão 12/8.');
            cy.get('.botao-adicionar-observacao').click();
        });
        cy.get('.alerta.success').should('contain.text', 'Observação adicionada com sucesso!');
    });
});