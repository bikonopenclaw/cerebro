# MEMORY.md

Memória institucional consolidada do Brain.

## Diretrizes permanentes

- O Agente Principal administra o Brain.
- O Brain é patrimônio intelectual acumulado.
- O Brain é a fonte de verdade para classificar e armazenar memórias importantes; memória operacional do OpenClaw é apoio de busca/recall, não substitui curadoria do Brain.
- Registrar apenas informação com utilidade futura.
- Evitar duplicidade antes de criar novos registros.
- Relacionar pessoas, empresas, projetos e conhecimento sempre que possível.
- Consolidar periodicamente, sem atrapalhar a execução do dia.
- Antes de ações que enviem, alterem, criem ou executem algo fora da conversa atual, avisar Hebert e confirmar quando o impacto não estiver previamente autorizado; rotinas silenciosas já autorizadas seguem suas próprias restrições.
- Para NFS-e da Bikon, usar todos os dados disponíveis do cadastro mestre no tomador; se houver endereço, incluir endereço completo. Se o endereço estiver ausente ou ambíguo, tratar como pendência antes da emissão.
- Para e-mails de NFS-e da Bikon, usar `fatura@bikontecnologia.com.br`, template HTML padrão Bikon e anexar DANFSe PDF, XML e boleto PDF quando houver boleto.
- Em lotes de NFS-e, se houver duas ou mais notas para o mesmo ID/documento de cliente, agrupar em um único e-mail por cliente com todos os documentos e boletos anexados.
- Áudios devem ser transcritos primeiro pela instância local faster-whisper; API externa só quando Hebert pedir ou quando a rota local falhar de forma não recuperável.
- Manter API keys, tokens, senhas, `.env`, inventários sensíveis e respostas detalhadas de APIs fora do Brain/Git; registrar apenas arquitetura, escopo, guardrails e métricas agregadas quando útil.
- Canais operacionais devem ter escopo, fora de escopo, roteamento e guardrails explícitos para evitar mistura de assuntos e execução no contexto errado.
- Quando Hebert pedir correção pontual em arte/design/arquivo, preservar a base aprovada e alterar apenas o elemento solicitado, salvo pedido explícito de redesenho amplo.
- Separar teste, rascunho e produção em automações externas: dry-run e preparo interno podem avançar, mas envio, publicação, emissão, remessa ou alteração real exigem confirmação quando houver impacto externo.
- Em testes com dados reais, usar destinatário explícito e impedir lookup automático que possa enviar informação a terceiros.
- Em governança de identidade BIKON ↔ AD local de clientes, começar por auditoria e matriz aprovada; não criar, desativar ou alterar contas/grupos sem validação humana.
- Retorno bancário CNAB400 serve para parser/conciliação quando sanitizado, mas não valida remessa, nosso número, documento ou sequencial.
- Relatórios externos devem ser revisados visualmente antes da entrega, removendo metadados de navegador, cabeçalhos/rodapés automáticos e aparência de HTML impresso.
- Em canais operacionais, grupo permitido e remetente autorizado são dimensões diferentes; `groupAllowFrom` deve representar remetente autorizado.

## Padrões consolidados mensalmente

- Padrão mensal de junho/2026: segurança operacional antes de escala; automações podem preparar e validar, mas impactos fiscais, bancários, comunicacionais, publicações e alterações de identidade exigem confirmação explícita quando não autorizados previamente.
