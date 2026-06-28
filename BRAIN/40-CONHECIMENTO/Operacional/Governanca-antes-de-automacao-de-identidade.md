# Governança antes de automação de identidade

```yaml
categoria: operacional
tipo: aprendizado_permanente
fonte: consolidação semanal 2026-W26
confiabilidade: alta
ultima_revisao: 2026-06-28
tags: [identidade, entra-id, ad-local, auditoria, governanca, rmm]
```

## Princípio

Antes de automatizar identidade entre diretórios internos e ambientes de clientes, é necessário separar inventário, aprovação, matriz de permissões, regras de ação e trilha de auditoria.

## Aplicação prática

- Começar com fase somente-auditoria.
- Comparar usuários aprovados no Entra ID BIKON com contas/grupos encontrados nos ADs locais dos clientes.
- Reportar divergências antes de qualquer correção.
- Não criar, desativar, remover grupo ou alterar privilégio sem aprovação explícita.
- Ignorar contas não marcadas como gerenciadas pela BIKON, salvo quando houver evidência relevante para relatório.
- Evitar registrar no Brain dumps de AD, inventários brutos, hashes, senhas ou dados sensíveis completos.

## Motivo

Automação de identidade tem alto risco operacional. Uma correção indevida pode remover acesso legítimo, conceder privilégio excessivo ou interferir em contas que pertencem ao cliente.

## Relações

- `BRAIN/70-AUTOMACOES/MATRIZ-ACESSO-BIKON-AD-CLIENTES.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Confirmacao-antes-de-acoes-com-impacto.md`
- `BRAIN/40-CONHECIMENTO/Operacional/Segredos-fora-do-Brain-e-Git.md`
