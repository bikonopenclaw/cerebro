---
name: faturamento-fn-souza
description: Use para rotinas de faturamento, NFS-e, boletos, remessas, conferências cadastrais e controles financeiros específicos do cliente FN Souza. Estrutura inicial aguardando regras detalhadas do Hebert.
---

# Faturamento FN Souza

Skill específica para o Darth Vader operar o fluxo de faturamento do cliente FN Souza.

## Status

Estrutura criada. Aguardando o Hebert passar os detalhes operacionais antes de executar qualquer rotina real.

## Escopo previsto

Usar esta skill quando o pedido envolver FN Souza e qualquer item abaixo:

- emissão ou preparação de NFS-e;
- emissão ou preparação de boleto;
- geração, conferência ou validação de remessa bancária;
- leitura/conferência de retorno bancário;
- conferência cadastral para faturamento;
- organização de documentos, pacotes, rascunhos e pendências financeiras do cliente.

## Regras temporárias

Enquanto a configuração detalhada não for preenchida:

1. Não emitir NFS-e real.
2. Não emitir boleto real.
3. Não enviar comunicação externa para cliente.
4. Não gerar remessa de produção.
5. Pode preparar rascunhos, estrutura de arquivos e lista de pendências internas.
6. Sempre consultar o cadastro mestre de clientes ativos antes de usar dados fiscais:
   `/data/.openclaw/workspace-darth-vader/cadastros/clientes/clientes_ativos.json`
7. Se a informação do FN Souza não existir ou estiver incompleta no cadastro, registrar pendência e pedir dados ao Hebert.

## Integrações relacionadas

Quando necessário, usar também:

- Skill geral de NFS-e/boleto/remessa: `/data/.openclaw/agents/darth-vader/agent/skills/emitir-nfse-boleto-remessa/SKILL.md`
- Skill técnica de boletos Cresol: `/data/.openclaw/agents/darth-vader/agent/skills/boletos-cresol/SKILL.md`
- Cadastro de clientes: `/data/.openclaw/workspace-darth-vader/cadastros/clientes/`

## Estrutura da skill

- `references/`: regras específicas do cliente, quando Hebert enviar.
- `scripts/`: automações específicas futuras.
- `assets/`: modelos, logos ou arquivos fixos futuros.

## Próxima configuração pendente

Preencher quando Hebert enviar:

- razão social e CPF/CNPJ correto do cliente;
- município emissor ou prefeitura usada;
- descrição padrão do serviço;
- valor recorrente ou regra de cálculo;
- vencimento padrão;
- dados bancários/carteira para boleto;
- e-mails financeiros;
- frequência de faturamento;
- modelo de mensagem/rascunho;
- exceções e cuidados específicos.
