---
name: provimento-213-2026
description: Use para diagnosticar, planejar e produzir evidências de adequação de cartórios ao Provimento CNJ 213/2026, incluindo checklist por classe da serventia, dossiê técnico, relatório simplificado, PCN/PRD, política de segurança, inventário de ativos, backup, logs, MFA, LGPD, interoperabilidade e parecer técnico no padrão Bikon/Kowalski.
---

# Provimento CNJ 213/2026, cartórios

Use esta skill quando o pedido envolver **Provimento 213/2026**, **cartório**, **serventia extrajudicial**, adequação técnica, dossiê técnico, Justiça Aberta, PCN, PRD, RTO, RPO, backup, logs, MFA, LGPD ou parecer técnico de conformidade para cartórios.

## Papel da skill

Produzir material técnico e operacional para a Bikon atender cartórios. Não emitir parecer jurídico, não prometer conformidade legal plena e não assinar como advogado.

Entregar sempre como apoio técnico: diagnóstico, plano de adequação, evidências, relatório, checklist, dossiê e recomendações práticas.

## Fontes e caminhos

- Workspace operacional: `/data/.openclaw/workspace-kowalski/provimento-213-2026`
- Provimento original baixado: `/data/.openclaw/workspace-kowalski/provimento-213-2026/referencias/provimento-213-2026-cnj.pdf`
- Texto extraído: `/data/.openclaw/workspace-kowalski/provimento-213-2026/referencias/provimento-213-2026-cnj.txt`
- Checklists: `/data/.openclaw/workspace-kowalski/provimento-213-2026/checklists`
- Modelos: `/data/.openclaw/workspace-kowalski/provimento-213-2026/modelos`
- Relatórios por cliente: `/data/.openclaw/workspace-kowalski/provimento-213-2026/relatorios`
- Modelo visual oficial Bikon para parecer técnico: `/data/.openclaw/workspace-kowalski/identidade-visual/modelos-aprovados/parecer-tecnico/modelo-padrao-parecer-tecnico-bikon.html`

Referências internas desta skill:

- `references/resumo-operacional.md`: requisitos, prazos, RTO/RPO e etapas.
- `references/checklist-evidencias.md`: checklist prático por etapa com evidências esperadas.
- `references/carteira-cartorios-cns-20260714.md`: carteira CNS recebida do Herald OS em 2026-07-14, com separação entre carteira Prov.213 ativa, contrato encerrado e cartório fora do escopo completo.

## Carteira CNS e escopo operacional

Antes de produzir diagnóstico, relatório, dossiê ou plano por cartório, leia `references/carteira-cartorios-cns-20260714.md` quando o pedido envolver cliente conhecido da Bikon, ARX Backup, NinjaOne, Bitdefender ou carteira Prov.213.

Use a referência para:

1. Identificar os 6 cartórios da carteira formal de adequação Prov.213.
2. Evitar misturar cartório ativo da Bikon com cartório fora da carteira ativa.
3. Registrar CNS, fonte interna, classe, prazo e status documental quando o dado estiver listado.
4. Marcar RI Marabá com prorrogação não comprovada no acervo, não como deferida.
5. Tratar Cartório 2º Ofício Vila Velha como contrato encerrado, sem ação operacional ativa.
6. Tratar Cartório Camburi como fora da adequação completa Prov.213, cliente somente de ARX Backup conforme decisão do dono.

Regra: CNS da carteira é dado de handoff interno com fonte citada. Não inferir CNS ausente e não promover item fora da carteira ativa para cliente Prov.213 sem aprovação explícita do Hebert.

## Regras de segurança e escopo

- Nunca tratar o relatório como aconselhamento jurídico.
- Nunca dizer que o cartório está “juridicamente conforme”. Preferir: `aderente tecnicamente aos itens avaliados`, `com pendências`, `não evidenciado`.
- Não enviar relatório, e-mail ou mensagem para cliente externo sem aprovação explícita do Hebert/Puppet Master.
- Não alterar produção de cliente, firewall, backup, DNS, sistemas cartorários ou contratos sem autorização explícita.
- Não incluir senhas, tokens, chaves privadas, certificados, prints com credenciais ou dados pessoais desnecessários no relatório.
- Quando houver dados pessoais em evidências, mascarar o que não for necessário.

## Entrada esperada

Para diagnóstico por cartório, buscar ou solicitar:

1. Nome da serventia e responsável.
2. CNS confirmado ou pendência formal de CNS. Se o cartório estiver na carteira CNS 2026-07-14, usar o CNS listado com sua fonte interna e manter evidência citada.
3. Classe da serventia, Classe 1, 2 ou 3. Se não souber, marcar como `classe não informada` e não inventar.
4. Lista de sistemas usados, fornecedores e contratos.
5. Inventário de ativos, servidores, estações, rede, links, energia, certificados e backups.
6. Evidências de MFA, logs, backup, restauração, antivírus/EDR, firewall, SGBD e criptografia.
7. Situação de LGPD, DPO quando aplicável, registro de tratamento e política de segurança.
8. PCN/PRD existentes, se houver.
9. Últimos testes de backup/restauração e incidentes relevantes.

## Workflow padrão

1. Confirmar se a serventia está na carteira CNS e escopo Prov.213 ativo.
2. Classificar a serventia por classe ou marcar classe pendente.
3. Ler `references/resumo-operacional.md` e, quando precisar checklist granular, `references/checklist-evidencias.md`.
4. Montar matriz com colunas: `etapa`, `item`, `exigência`, `status`, `evidência`, `risco`, `ação recomendada`, `responsável`, `prazo sugerido`.
5. Separar status em:
   - `Atendido`: evidência suficiente e verificável.
   - `Parcial`: há controle, mas falta formalização, teste, prova ou cobertura.
   - `Pendente`: não implementado ou não demonstrado.
   - `Não avaliado`: falta acesso, dado ou evidência.
   - `Não aplicável`: justificar objetivamente.
6. Criar diagnóstico executivo com semáforo:
   - `OK`: itens críticos demonstrados e pendências sem impacto imediato.
   - `Atenção`: pendências relevantes, mas com mitigação parcial.
   - `Crítico`: falta backup/restauração, MFA administrativo, logs, PCN/PRD, proteção básica ou risco claro de indisponibilidade/perda de dados.
7. Produzir plano de adequação por fases, respeitando as Etapas 1 a 5 do Anexo IV.
8. Gerar dossiê ou relatório simplificado conforme classe:
   - Classe 1: relatório simplificado e guarda de contratos, notas fiscais e evidências por 5 anos.
   - Classes 2 e 3: dossiê técnico com evidências, hashes/lista assinável e controle auditável.
9. Se for parecer externo, usar o modelo visual oficial Bikon/Kowalski de parecer técnico.

## Prazos normativos úteis

Contados da entrada em vigor do Provimento:

- Implementação inicial, Etapas 1 e 2:
  - Classe 3: 90 dias.
  - Classe 2: 150 dias.
  - Classe 1: 210 dias.
- Implementação integral, Etapas 1 a 5:
  - Classe 3: até 24 meses.
  - Classe 2: até 30 meses.
  - Classe 1: até 36 meses.
- Prorrogação excepcional: uma vez, até 90 dias, mediante plano formal e medidas compensatórias mínimas.

## RTO, RPO e backup

Parâmetros mínimos do Provimento:

- RPO:
  - Classe 3: máximo 4 horas.
  - Classe 2: máximo 12 horas.
  - Classe 1: máximo 24 horas.
- RTO:
  - Classe 3: máximo 8 horas.
  - Classe 2: máximo 24 horas.
  - Classe 1: máximo 24 horas, admitida restauração simplificada documentada.
- Backup completo:
  - Classe 3: intervalo máximo 24 horas.
  - Classe 2: intervalo máximo 48 horas.
  - Classe 1: intervalo máximo 72 horas, desde que cumpra o RPO aplicável.
- Backup deve ter no mínimo dois ambientes tecnicamente independentes ou arquitetura em nuvem que demonstre redundância geográfica, retenção imutável, segregação de acesso, logs auditáveis e restauração viável.

## Entregáveis padrão

Conforme pedido, produzir um ou mais:

- diagnóstico inicial de aderência
- checklist preenchido
- matriz de riscos e pendências
- plano de adequação 30, 60, 90 dias
- inventário de ativos e fornecedores
- Política de Segurança da Informação mínima
- PCN/PRD técnico
- dossiê técnico por etapa
- relatório simplificado para Classe 1
- parecer técnico Bikon/Kowalski
- rascunho de e-mail para cliente, aguardando aprovação

## Linguagem Bikon

Português BR direto, técnico sem juridiquês e sem alarmismo barato.

Trocar linguagem vaga por ação concreta:

- Ruim: `regularizar segurança da informação`.
- Bom: `ativar MFA nos acessos administrativos, eliminar contas compartilhadas e anexar prints/configurações ao dossiê da Etapa 1`.

Não usar travessão em copy pública.

## Gatilhos de alerta para Puppet Master

Avisar Puppet Master antes de seguir se encontrar:

- cartório sem backup testado
- backup sem cópia externa ou sem proteção contra ransomware
- ausência de MFA em acesso administrativo
- credenciais compartilhadas em sistema cartorário
- logs inexistentes ou apagáveis por usuário comum
- fornecedor sem cláusula de reversibilidade/portabilidade
- risco de prazo normativo vencido ou vencendo nos próximos 30 dias
- pedido de enviar material direto ao cliente externo
