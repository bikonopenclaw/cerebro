# STANDBY

Status: standby com retomada experimental controlada
Dono: Darth Vader
Escopo: somente workspace do Darth Vader

Esta pasta ainda não é skill ativa do OpenClaw.
Ela fica guardada para retomada futura da integração SERPRO/parcelamentos.

## Retomada experimental, broker local

Autorizado testar somente o broker local de certificado A1:

- certificado fica no Mac/host do Hebert;
- senha digitada localmente, não salva;
- broker escuta apenas em `127.0.0.1`;
- OpenClaw/servidor não recebe `.pfx`, senha ou token colado no chat;
- testes iniciais só autenticam e consultam token;
- geração real de DAS ou chamada `/Emitir` continua bloqueada até aprovação explícita.

Arquivos:

- `broker-local/serpro_cert_broker.py`
- `broker-local/.serpro-broker.env.example`
- `broker-local/README-BROKER-LOCAL.md`
- `scripts/testar_broker_local.sh`

Regras:
- Não mover para skills ativas sem pedido explícito do Hebert/Puppet Master.
- Não registrar como skill global.
- Não usar em produção sem revisão, teste e aprovação.
- Quando for retomada, criar `SKILL.md` formal e separar referências, scripts e dados operacionais.
