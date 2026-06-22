# 📦 GUIA DE IMPLANTAÇÃO - NOTAAS NFSE SKILL

> Como implantar esta skill em qualquer instância OpenClaw

---

## 🎯 VISÃO GERAL

Esta skill foi projetada para ser **100% portátil**. Funciona em qualquer instância OpenClaw com qualquer empresa, sem necessidade de modificar o código.

**O que a skill faz:**
- ✅ Coleta configuração via setup interativo
- ✅ Armazena dados da empresa localmente
- ✅ Conecta à API Notaas com a chave fornecida
- ✅ Emite NFS-e para qualquer cliente cadastrado

**O que NÃO está na skill:**
- ❌ Dados da empresa (coletado no setup)
- ❌ API Key (coletada no setup)
- ❌ Certificado (fica na plataforma Notaas)
- ❌ Clientes (cadastrados após instalação)

---

## 📦 OPÇÕES DE IMPLANTAÇÃO

### **Opção 1: ClawHub (Recomendado)**

Publicar a skill no ClawHub para instalação fácil em qualquer instância.

```bash
# Na instância ORIGINAL (Marques Cap):
cd /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse
clawhub publish . --name notaas-nfse --version 2.0.0

# Na NOVA instância:
clawhub install notaas-nfse
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

**Vantagens:**
- ✅ Instalação com 1 comando
- ✅ Atualizações automáticas
- ✅ Versionamento

---

### **Opção 2: Pacote ZIP**

Criar pacote ZIP para envio manual.

```bash
# Na instância ORIGINAL:
cd /mnt/data/openclaw/workspace/.openclaw/workspace/skills/
zip -r notaas-nfse.zip notaas-nfse/ \
  -x "*.git*" \
  -x "config/*" \
  -x "data/*" \
  -x ".env" \
  -x "__pycache__/*"

# Enviar notaas-nfse.zip para nova instância
```

**Na NOVA instância:**
```bash
# Receber arquivo
unzip notaas-nfse.zip -d ~/.openclaw/workspace/skills/
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

**Vantagens:**
- ✅ Não depende do ClawHub
- ✅ Funciona offline
- ✅ Controle total

---

### **Opção 3: Git Repository**

Versionar em repositório Git privado.

```bash
# Na instância ORIGINAL:
cd /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse
git init
git add .
git commit -m "Skill notaas-nfse v2.0.0"
git remote add origin git@github.com:seu-user/notaas-nfse.git
git push -u origin main

# Na NOVA instância:
cd ~/.openclaw/workspace/skills/
git clone git@github.com:seu-user/notaas-nfse.git
cd notaas-nfse
./instalar.sh
```

**Vantagens:**
- ✅ Versionamento completo
- ✅ Histórico de mudanças
- ✅ Branches para desenvolvimento

---

### **Opção 4: Cópia Direta (SCP/RSYNC)**

Copiar diretamente via rede.

```bash
# Da instância ORIGINAL:
scp -r /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse \
  usuario@nova-instancia:~/.openclaw/workspace/skills/

# OU com rsync (mais eficiente):
rsync -avz --exclude 'config/*' --exclude 'data/*' --exclude '.env' \
  /mnt/data/openclaw/workspace/.openclaw/workspace/skills/notaas-nfse \
  usuario@nova-instancia:~/.openclaw/workspace/skills/

# Na NOVA instância:
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

**Vantagens:**
- ✅ Rápido para redes locais
- ✅ Sem dependências externas
- ✅ Cópia exata

---

## 🔧 CHECKLIST DE IMPLANTAÇÃO

### **Antes de Implantar**

- [ ] Remover dados sensíveis (config/, data/, .env)
- [ ] Testar instalação limpa
- [ ] Verificar permissions (chmod +x instalar.sh)
- [ ] Documentar versão atual

### **Na Nova Instância**

- [ ] Copiar/instalar skill
- [ ] Rodar `./instalar.sh`
- [ ] Preencher setup interativo
- [ ] Cadastrar primeiros clientes
- [ ] Testar emissão em homologação
- [ ] Testar emissão em produção
- [ ] Verificar logs

---

## 📋 DADOS NECESSÁRIOS PARA SETUP

A pessoa que for instalar precisa ter em mãos:

| Dado | Onde Obter |
|------|------------|
| **API Key Notaas** | platform.notaas.com.br → Config → API |
| **Razão Social** | Contrato social / CNPJ |
| **CNPJ** | Cartão CNPJ |
| **Inscrição Municipal** | Prefeitura (opcional) |
| **Código IBGE** | https://cidades.ibge.gov.br/ |

---

## 🧪 TESTES PÓS-INSTALAÇÃO

Após instalar, testar:

```bash
# 1. Verificar configuração
python3 -c "from core.config import get_config; print(get_config().resumo())"

# 2. Testar conexão API
python3 -c "from core.client import NotaasClient; c = NotaasClient(); print('OK')"

# 3. Emitir nota de teste (R$ 0,01)
python3 scripts/emitir_nota.py --confirmar-emissao \
  --cnpj "00.000.000/0001-00" \
  --valor 0.01 \
  --teste
```

---

## 🆘 SUPORTE PÓS-IMPLANTAÇÃO

### **Problemas Comuns**

| Problema | Solução |
|----------|---------|
| Setup não roda | `chmod +x scripts/setup.py` |
| API Key inválida | Gerar nova em platform.notaas.com.br |
| Erro de permissão | `chmod -R 755 ~/.openclaw/workspace/skills/notaas-nfse` |
| Python não encontrado | Instalar Python 3.8+ |

### **Canais de Suporte**

- 📧 Email: suporte@marquescap.com.br
- 💬 Telegram: Grupo OpenClaw
- 📚 Docs: `cat SKILL.md`

---

## 📊 MÉTRICAS DE IMPLANTAÇÃO

**Tempo estimado:**
- Instalação: 2-5 minutos
- Setup: 3-5 minutos
- Cadastro clientes: 5-10 minutos
- **Total: 10-20 minutos**

**Pré-requisitos:**
- Python 3.8+
- Acesso à internet
- Conta na Notaas

---

## ✅ CHECKLIST FINAL

Após implantação:

- [ ] Skill instalada
- [ ] Setup concluído
- [ ] Configuração válida
- [ ] Clientes cadastrados
- [ ] Primeira nota emitida
- [ ] PDFs baixando
- [ ] E-mails enviando
- [ ] Logs verificados

---

**Skill pronta para implantação em massa!** 🚀
