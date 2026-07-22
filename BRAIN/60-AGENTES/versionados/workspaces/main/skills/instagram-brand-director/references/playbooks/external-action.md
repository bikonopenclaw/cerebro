# Playbook: ação externa

1. Congelar payload e calcular hash.
2. Apresentar ação, destino, provider, custo, dados e horário.
3. Registrar OK do proprietário por evento confiável.
4. Governance Engine precisa retornar allow.
5. Reservar approval com execution ID.
6. Persistir evento executing imediatamente antes da chamada.
7. Executar uma vez.
8. Persistir resultado succeeded, failed ou indeterminate.
9. Reativar lock.
10. Se indeterminate, consultar o mesmo remote ID. Não repetir mutação.
