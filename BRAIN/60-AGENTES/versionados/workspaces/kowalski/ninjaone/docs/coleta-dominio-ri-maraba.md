# Coleta de dominio RI Maraba via NinjaOne

## Objetivo

Coletar dados do servidor de dominio do RI Maraba para analise posterior pelo Kowalski.

## Script

`/data/.openclaw/workspace-kowalski/ninjaone/scripts/coletar-dominio-ri-maraba-readonly.ps1`

## Onde executar

Executar pelo NinjaOne no servidor:

- `DM-SERVER`
- `dm-server.rimaraba.local`
- Funcao identificada pela API NinjaOne: `Primary Domain Controller`

## Comando

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\coletar-dominio-ri-maraba-readonly.ps1
```

## Saida esperada

O script imprime um resumo JSON no console do NinjaOne e grava o arquivo completo em:

```text
C:\ProgramData\Bikon\NinjaOne\ri-maraba-domain-inventory-YYYYMMDD-HHMMSS.json
```

Depois da execucao, enviar esse JSON para o Kowalski ler e gerar o levantamento.

## Escopo coletado

- dados do dominio e floresta AD;
- controladores de dominio;
- politica de senha do dominio;
- usuarios AD habilitados por padrao;
- grupos AD;
- computadores AD;
- OUs;
- GPOs e vinculos por dominio/OU, quando o modulo GroupPolicy estiver disponivel;
- shares SMB nao administrativos;
- permissoes de share;
- ACL NTFS na raiz dos caminhos compartilhados;
- usuarios e grupos locais do servidor.

## Seguranca

- Somente leitura.
- Nao altera AD, GPO, shares, ACLs ou configuracao local.
- Nao coleta senhas, hashes, secrets ou conteudo de arquivos.
- Por padrao nao inclui usuarios desabilitados nem shares administrativos.

## Opcionais

Incluir usuarios desabilitados:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\coletar-dominio-ri-maraba-readonly.ps1 -IncludeDisabledUsers
```

Incluir shares administrativos:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\coletar-dominio-ri-maraba-readonly.ps1 -IncludeAdminShares
```

Definir caminho de saida manual:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\coletar-dominio-ri-maraba-readonly.ps1 -OutputPath C:\Temp\ri-maraba-domain-inventory.json
```
