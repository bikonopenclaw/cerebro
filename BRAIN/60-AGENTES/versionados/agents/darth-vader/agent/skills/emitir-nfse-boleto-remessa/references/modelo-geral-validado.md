# Modelo geral validado, NFS-e + boleto + remessa Cresol

## Objetivo

Repetir o fluxo completo sem hardcode de cliente:

1. Emitir ou registrar dados reais da NFS-e.
2. Gerar boleto PDF limpo para conferência/homologação.
3. Gerar remessa CNAB400 Cresol.
4. Validar estrutura e aguardar retorno/homologação bancária.

## Regra importante

Não usar cliente real como referência de processo, template ou golden case.

Casos históricos de cliente servem apenas como histórico/auditoria do que foi feito naquele atendimento. Para novas emissões, usar somente o schema parametrizado, os dados atuais do cliente e as regras bancárias/fiscais vigentes.

## Regras gerais

- Cliente, pagador, documento, nosso número, vencimento, valor e sequencial vêm do job JSON atual.
- Nunca reaproveitar valor atualizado de segunda via com multa/mora como valor base de cobrança nova.
- O boleto PDF da skill é para homologação/conferência visual. Registro bancário real depende da remessa validada ou sistema do banco.
- A remessa `.rem` gerada pela skill é homologação até o Hebert aprovar produção.
- Depois que o banco validar um `.rem`, registrar no pacote/status, mas não subir produção automaticamente.

## Arquivos gerados pelo pacote

- `job.json`: cópia da entrada original.
- `boleto-input.json`: dados normalizados usados no boleto.
- `*-boleto.html`: boleto HTML limpo.
- `*-boleto.pdf`: boleto PDF para conferência.
- `remessa-input.json`: dados normalizados usados na remessa.
- `*.rem`: remessa CNAB400.
- `status-emissao.md`: status consolidado.

## Validações mínimas

Boleto:

- Linha digitável calculada pelo código de barras.
- Código de barras I25 gerado no PDF.
- Nosso número com DV calculado.
- PDF renderizado deve ser conferido visualmente antes de enviar.

Remessa:

- 400 caracteres por linha antes do CRLF.
- Header começa com `0`.
- Detalhes começam com `1`.
- Trailer começa com `9`.
- Documento, nosso número, vencimento, valor, CNPJ e pagador batem com boleto/NFS-e.

## Próximo endurecimento

Quando houver integração real do banco ou emissor de boleto, substituir `boleto_emitido_homologacao` por status real retornado pela API/sistema bancário.
