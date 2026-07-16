# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Bitdefender GravityZone

- Responsável operacional: Kowalski.
- Segredo local: `/data/.openclaw/secrets/bitdefender-gravityzone.env`.
- Permissão esperada do segredo: `600`.
- Variáveis: `BITDEFENDER_GZ_BASE_URL`, `BITDEFENDER_GZ_API_KEY`.
- Rotina local: `bitdefender-gravityzone/scripts/gz_client.py`.
- Regra: nunca copiar API key para Drive, Telegram, relatório, log ou workspace.
- Não enviar comunicação externa sem aprovação do Hebert/Puppet Master.
- Não delegar para Darth Vader, salvo impacto financeiro/faturamento e copiando o Puppet Master.
- Teste validado: `getCompaniesList` via endpoint `network`, HTTP/API OK, 21 empresas retornadas.

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)

## Git e versionamento

- Binario: `/usr/bin/git`.
- Repositorio oficial: `/data/.openclaw/workspace/Brain`.
- Remoto: `git@github.com:bikonopenclaw/cerebro.git`.
- Snapshot seguro do Kowalski: `BRAIN/60-AGENTES/versionados/workspaces/kowalski/` dentro do repositorio Brain.
- O workspace vivo `/data/.openclaw/workspace-kowalski` nao e repositorio. Nunca executar `git init` nele.
- Motivo: o workspace vivo contem credenciais locais, relatorios, caches e artefatos que nao podem entrar no Git.

Consultas Git permitidas sem alterar estado:

```bash
git -C /data/.openclaw/workspace/Brain status --short --branch
git -C /data/.openclaw/workspace/Brain diff -- BRAIN/60-AGENTES/versionados/workspaces/kowalski
git -C /data/.openclaw/workspace/Brain log -n 10 --oneline
```

Fluxo que exige aprovacao explicita do Hebert:

1. Executar o sincronizador seguro `Brain/scripts/sync-agentes-versionados.py`.
2. Revisar diff e varredura de segredo.
3. Preparar lista exata dos arquivos que entrarao.
4. Aguardar novo OK para `git add`, `git commit` e `git push`.

Nunca versionar `.env`, token, OAuth, credencial, banco local, relatorio final de cliente, cache, sessao ou artefato binario gerado.
