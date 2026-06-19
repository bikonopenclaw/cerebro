# Grupos Telegram de faturamento

```yaml
categoria: automacao_operacional
fonte: sessões Telegram visíveis em 2026-06-17 e correção operacional em 2026-06-18/19
confiabilidade: alta
ultima_revisao: 2026-06-19
tags: [telegram, faturamento, bikon, fn-souza, nfse, boletos, remessa, darth-vader]
```

## Finalidade

Registrar os contextos operacionais de grupos Telegram usados para faturamento, evitando mistura de assuntos e preservando regras de segurança fiscal/financeira.

## Grupos ativos

### Faturamento Bikon

- Chat: `telegram:-5561224828`
- Contexto operacional local: `/data/.openclaw/workspace/contextos/telegram--5561224828-faturamento-bikon.md`
- Escopo: apenas faturamento da Bikon Tecnologia.
- Inclui: NFS-e, boletos, remessa/retorno bancário e conferência cadastral ligada diretamente ao faturamento da Bikon.
- Fora de escopo: faturamento de terceiros, comercial geral, marketing/conteúdo, suporte técnico, infraestrutura/site/checkout sem ligação direta com faturamento, financeiro gerencial amplo e conversa operacional aleatória.
- Roteamento: Puppet Master coordena; execução fiscal/financeira deve ser delegada ao Darth Vader quando necessário.

### Faturamento FN Souza

- Chat: `telegram:-5435011106`
- Contexto operacional local: `/data/.openclaw/workspace/contextos/telegram--5435011106-faturamento-fn-souza.md`
- Escopo: apenas criação/conferência de NFS-e, criação/conferência de boletos e geração/validação/conferência de arquivos de remessa da skill `faturamento-fn-souza`.
- Fora de escopo: comercial geral, suporte técnico, conteúdo/marketing, financeiro gerencial sem ligação direta com NFS-e/boleto/remessa FN Souza e conversa operacional aleatória.
- Roteamento: Puppet Master coordena; quando houver execução fiscal/financeira, acionar Darth Vader com a skill `faturamento-fn-souza`.

## Guardrails

- Não emitir NFS-e real sem aprovação explícita do Hebert.
- Não emitir boleto real sem aprovação explícita do Hebert.
- Não gerar remessa de produção sem aprovação explícita do Hebert e validação do layout bancário.
- Não enviar comunicação externa ou arquivo financeiro a cliente sem aprovação explícita.
- Preparos internos, rascunhos, conferências e validações podem ser executados sem impacto externo quando houver dados suficientes.
- Se faltar dado fiscal/financeiro, pedir apenas o mínimo necessário para desbloquear.
- Antes de postar, repostar, acionar agente, alterar configuração ou disparar qualquer execução fora da conversa atual, avisar Hebert e confirmar quando o impacto não estiver previamente autorizado.

## Relações

- Empresa: `BRAIN/20-EMPRESAS/BIKON/README.md`
- Automação fiscal: `BRAIN/70-AUTOMACOES/NOTAAS-NFSE.md`
- Boletos/malote: `BRAIN/70-AUTOMACOES/boletos-malote/README.md`
- Agente executor financeiro: Darth Vader
- Diretriz operacional: `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
