# 📦 NOTAAS NFSE SKILL - PACOTE PARA IMPLANTAÇÃO

> **Versão:** 2.0.0 (Portátil)  
> **Data:** 2026-06-12  
> **Autor:** Claw D. Marques - Marques Cap

---

## 🎯 O QUE É ESTE PACOTE

Skill completa para emissão de NFS-e via API Notaas. **100% portátil** - funciona em qualquer instância OpenClaw com qualquer empresa.

**Diferencial:** Configuração via setup interativo. Não precisa editar arquivos manualmente!

---

## 📁 O QUE TEM NO PACOTE

```
notaas-nfse/
├── 📄 SKILL.md                 # Documentação completa
├── 📄 README.md                # Guia de instalação
├── 📄 BOAS_VINDAS.md           # Primeiros passos
├── 📄 IMPLANTACAO.md           # Guia de implantação
├── 📄 CHANGELOG.md             # Histórico
├── 🔧 instalar.sh              # Script de instalação
├── 📦 empacotar.sh             # Criar pacote ZIP
├── 📁 scripts/
│   ├── setup.py               # ⭐ SETUP INTERATIVO
│   ├── emitir_nota.py
│   ├── emitir_lote.py
│   ├── cancelar_nota.py
│   └── cadastrar_cliente.py
├── 📁 core/
│   ├── client.py              # API client
│   └── config.py              # Configuração automática
├── 📁 examples/               # Exemplos de uso
├── 📁 templates/              # Templates de payload/email
└── 📁 data/                   # Criado após instalação
    ├── clientes.json
    └── historico.json
```

---

## 🚀 INSTALAÇÃO RÁPIDA

### **Opção A: ClawHub** (Recomendado)

```bash
# Na nova instância:
clawhub install notaas-nfse
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

### **Opção B: ZIP Manual**

```bash
# Na nova instância:
unzip notaas-nfse.zip -d ~/.openclaw/workspace/skills/
cd ~/.openclaw/workspace/skills/notaas-nfse
./instalar.sh
```

---

## ⚙️ SETUP INTERATIVO

O script `setup.py` vai coletar:

1. **API Key da Notaas** (ntaas_xxxxxx)
2. **Nome da Empresa** (razão social)
3. **CNPJ da Empresa** (14 dígitos)
4. **Inscrição Municipal** (opcional)
5. **Cidade/UF** (para código IBGE)

**NÃO precisa saber nada antes!** O script guia passo-a-passo.

---

## 📋 PRÉ-REQUISITOS DA NOVA INSTÂNCIA

| Item | Obrigatório? | Onde Obter |
|------|--------------|------------|
| **Python 3.8+** | ✅ | Já vem no OpenClaw |
| **Conta na Notaas** | ✅ | https://platform.notaas.com.br |
| **API Key** | ✅ | Config → API na plataforma |
| **Certificado A1** | ✅ | Cadastrado na Notaas |
| **CNPJ da Empresa** | ✅ | Contrato social |

---

## 🧪 TESTES PÓS-INSTALAÇÃO

```bash
# 1. Verificar configuração
python3 -c "from core.config import get_config; print(get_config().resumo())"

# 2. Testar conexão
python3 -c "from core.client import NotaasClient; c = NotaasClient(); print('OK')"

# 3. Emitir nota de teste
python3 scripts/emitir_nota.py --dry-run --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao 'Teste' --valor 100
```

---

## 📊 O QUE MUDOU DA VERSÃO 1.0 PARA 2.0

| Versão 1.0 (Marques Cap) | Versão 2.0 (Portátil) |
|--------------------------|-----------------------|
| Dados hardcoded | Setup interativo |
| Certificado local | Certificado na Notaas |
| Config manual | Config automática |
| 1 empresa | Multi-empresas |
| Editar arquivos | CLI interativa |

---

## 🎁 BÔNUS INCLUÍDOS

### **Scripts de Apoio**

- `empacotar.sh` - Cria ZIP limpo para distribuição
- `instalar.sh` - Instalação automática
- `setup.py` - Configuração interativa

### **Documentação Completa**

- `SKILL.md` - Especificação técnica
- `README.md` - Guia de instalação
- `BOAS_VINDAS.md` - Primeiros passos
- `IMPLANTACAO.md` - Guia de implantação
- `CHANGELOG.md` - Histórico de versões

### **Exemplos Prontos**

- `examples/individual.py` - Emissão individual
- `examples/lote.py` - Emissão em lote
- `templates/payload.json` - Template de payload

---

## 📞 SUPORTE

**Criado por:** Claw D. Marques - Marques Cap  
**Email:** clawmarquescap@gmail.com  
**Telegram:** Grupo OpenClaw Marques Cap

**Documentação:**
- Local: `cat SKILL.md`
- Online: (em breve no ClawHub)

---

## ✅ CHECKLIST DE IMPLANTAÇÃO

Para quem for implantar:

- [ ] Baixar pacote (ZIP ou ClawHub)
- [ ] Extrair em `~/.openclaw/workspace/skills/`
- [ ] Rodar `./instalar.sh`
- [ ] Preencher setup interativo
- [ ] Cadastrar clientes
- [ ] Testar emissão
- [ ] Validar PDFs
- [ ] Testar e-mails

**Tempo estimado:** 15-20 minutos

---

## 🎉 PRONTO!

Skill pronta para usar em **qualquer instância OpenClaw** com **qualquer empresa**!

**Só precisa da API Key e CNPJ - o resto é automático!** 🚀

---

*Pacote gerado em 2026-06-12 por Claw D. Marques*
