#!/usr/bin/env node
/**
 * Enviar e-mail com anexo via Gmail API
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const CONFIG_DIR = path.join(process.env.HOME || '/tmp', '.config', 'praxis-gws');
const TOKEN_PATH = path.join(CONFIG_DIR, 'token.json');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');

const Base64 = {
  encodeURI: (str) => Buffer.from(str).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
};

async function sendEmailWithAttachment(to, subject, htmlBody, attachmentPath, isHtml = true) {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
  
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  
  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
    oAuth2Client.setCredentials(token);
  } else {
    console.error('Erro: Token não encontrado. Execute a autenticação primeiro.');
    process.exit(1);
  }
  
  const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
  
  // Ler anexo
  const attachmentData = fs.readFileSync(attachmentPath);
  const attachmentBase64 = attachmentData.toString('base64');
  const fileName = path.basename(attachmentPath);
  
  // Criar mensagem MIME multipart
  const boundary = 'boundary_' + Date.now();
  const contentType = isHtml ? 'text/html; charset=utf-8' : 'text/plain; charset=utf-8';
  const messageParts = [
    'From: a conta Google autorizada',
    `To: ${to}`,
    `Subject: =?utf-8?B?${Buffer.from(subject).toString('base64')}?=`,
    'MIME-Version: 1.0',
    `Content-Type: multipart/mixed; boundary="${boundary}"`,
    '',
    `--${boundary}`,
    `Content-Type: ${contentType}`,
    'Content-Transfer-Encoding: 7bit',
    '',
    htmlBody,
    '',
    `--${boundary}`,
    `Content-Type: application/pdf; name="${fileName}"`,
    'Content-Transfer-Encoding: base64',
    `Content-Disposition: attachment; filename="${fileName}"`,
    '',
    // Quebrar linha a cada 76 caracteres (padrão MIME)
    attachmentBase64.match(/.{1,76}/g).join('\r\n'),
    '',
    `--${boundary}--`
  ];
  
  const message = messageParts.join('\r\n');
  const encodedMessage = Base64.encodeURI(message);
  
  const res = await gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedMessage,
    },
  });
  
  console.log('✅ E-mail enviado com sucesso!');
  console.log('ID da mensagem:', res.data.id);
  console.log('Destinatário:', to);
  console.log('Assunto:', subject);
  console.log('Anexo:', fileName);
}

// CLI
const args = process.argv.slice(2);
if (args.length < 4) {
  console.log('Uso: node send-email-attachment.js <to> <subject> <body> <attachment> [--text]');
  console.log('  --text: Enviar corpo como texto puro (padrão: HTML)');
  process.exit(1);
}

const isHtml = !args.includes('--text');
sendEmailWithAttachment(args[0], args[1], args[2], args[3], isHtml)
  .catch(err => {
    console.error('Erro:', err.message);
    process.exit(1);
  });
