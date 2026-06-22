# 👋 BOAS-VINDAS - NOTAAS NFSE

> Seu guia de primeiros passos

---

## 🎉 PARABÉNS! VOCÊ INSTALOU A SKILL NOTAAS NFSE

Esta skill vai automatizar a emissão de Notas Fiscais de Serviço (NFS-e) para sua empresa.

**Tempo estimado para começar:** 10 minutos ⏱️

---

## 🚀 COMEÇANDO AGORA

### **Passo 1: Configurar (5 min)**

```bash
cd ~/.openclaw/workspace/skills/notaas-nfse
python3 scripts/setup.py
```

Você vai precisar de:
- ✅ API Key da Notaas (pegar em platform.notaas.com.br)
- ✅ CNPJ da sua empresa
- ✅ Cidade/UF

### **Passo 2: Cadastrar Clientes (5 min)**

```bash
python3 scripts/cadastrar_cliente.py
```

Ou edite manualmente: `data/clientes.json`

### **Passo 3: Primeira Emissão (2 min)**

```bash
# Modo teste (não emite de verdade)
python3 scripts/emitir_nota.py --dry-run --cnpj 00.000.000/0001-00 --nome TESTE --email teste@exemplo.com --codigo 171901 --descricao 'Teste' --valor 100

# Emissão real
python3 scripts/emitir_nota.py --confirmar-emissao \
  --cnpj "00.000.000/0001-00" \
  --valor 1000.00 \
  --descricao "Serviços"
```

---

## 📚 ONDE ENCONTRAR

| Arquivo | O que tem |
|---------|-----------|
| `README.md` | Guia completo de instalação |
| `SKILL.md` | Documentação técnica |
| `IMPLANTACAO.md` | Como implantar em outras instâncias |
| `scripts/` | Scripts prontos para usar |
| `examples/` | Exemplos de código |
| `data/clientes.json` | Seus clientes |

---

## 🆘 PRECISA DE AJUDA?

### **Erros Comuns**

**"API Key inválida"**
```bash
# Rodar setup novamente
python3 scripts/setup.py
```

**"Cliente não encontrado"**
```bash
# Cadastrar cliente
python3 scripts/cadastrar_cliente.py
```

**"PDF não disponível"**
- Aguarde 15 minutos
- XML já está disponível
- Retry automático após 15 min

### **Mais Ajuda**

- 📖 Leia: `cat README.md`
- 💬 Telegram: Grupo OpenClaw
- 📧 Email: suporte@marquescap.com.br

---

## ✅ CHECKLIST RÁPIDO

- [ ] Skill instalada
- [ ] Setup rodado
- [ ] API Key configurada
- [ ] Empresa configurada
- [ ] Primeiro cliente cadastrado
- [ ] Nota de teste emitida
- [ ] PDF baixado
- [ ] E-mail enviado

---

## 🎯 PRÓXIMOS PASSOS

Depois de configurar:

1. **Cadastre todos os clientes**
2. **Teste emissão individual**
3. **Teste emissão em lote**
4. **Configure e-mails automáticos**
5. **Agende emissões mensais**

---

**Bom trabalho! 🚀**

*Skill criada por Claw D. Marques - Marques Cap*
