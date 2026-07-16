# Procedimento de revogacao

## Regras comuns

- Somente Hebert autoriza revogacao, rotacao, substituicao ou reativacao.
- Registrar motivo, fonte, horario UTC, responsavel e correlacao antes da acao.
- Nao apagar auditoria. Nao copiar segredo. Nao usar fallback.
- Remover o arquivo local ou bloquear o cliente nao revoga a credencial no provedor.
- Depois da revogacao, validar falha pela mesma rota aprovada e registrar evidencia
  sem resposta bruta ou segredo.

## NinjaOne

1. Hebert define a janela e os consumidores afetados pela credencial M2M compartilhada.
2. O responsavel autorizado revoga ou rotaciona a credencial no provedor.
3. A referencia externa e atualizada pelo responsavel, mantida com permissao `600`.
4. Executar apenas `ninjaone_readonly.py probe`: credencial revogada deve falhar;
   credencial substituta deve retornar somente escopo `monitoring`.
5. Confirmar que `management` e `control` continuam recusados pelo cliente.

## ARX/Cove

1. Hebert define a janela e os consumidores afetados pela integracao compartilhada.
2. O responsavel autorizado revoga ou rotaciona senha/token no provedor Cove.
3. A referencia externa e atualizada pelo responsavel, mantida com permissao `600`.
4. Executar apenas `arx_readonly.py probe` e confirmar que permanecem expostos
   somente `Login` e `EnumerateAccountStatistics`.

## Bitdefender

1. Hebert define a janela e os consumidores afetados pela API key compartilhada.
2. O responsavel autorizado revoga ou rotaciona a API key no GravityZone.
3. A referencia externa e atualizada pelo responsavel, mantida com permissao `600`.
4. Executar apenas `bitdefender_readonly.py probe`: a chave revogada deve falhar;
   a substituta deve responder somente aos quatro metodos de consulta da allowlist.
5. Confirmar que nenhuma operacao de quarentena, isolamento, remediacao, politica
   ou escrita foi exposta.

## Fontes locais

- Contexto e logs nao usam credencial no Sentinel; o controle e por cliente e allowlist.
- Revogacao exige aprovacao do Hebert para desabilitar o cliente ou retirar a fonte.
- Preservar os arquivos de auditoria e de alteracao durante qualquer rollback.
