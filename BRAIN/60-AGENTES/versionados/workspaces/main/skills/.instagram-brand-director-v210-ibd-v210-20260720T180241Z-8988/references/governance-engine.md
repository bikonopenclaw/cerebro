# Governance Engine

O engine recebe ator, request, registry, governança e approval opcional. Retorna decisão determinística \`allow|deny\` e razões.

## Ordem dos gates

1. request válido e hash canônico;
2. ator conhecido e habilitado;
3. ação permitida ao ator;
4. provider kind e ID conhecidos;
5. provider habilitado;
6. adapter local presente quando exigido;
7. event stream íntegro;
8. owner binding configurado para mutação externa;
9. approval válido e vinculado ao provider, ação, destino, versão e payload;
10. lock liberável somente para a execução criada.

Qualquer falha encerra em deny. Não existe warn-then-run.

Skipper, Rico e Private começam desabilitados. Quando habilitados, apenas assistem. Skipper não substitui Robotnik; Rico não emite brand QA; Private não aceita risco residual; nenhum deles aprova ação externa.
