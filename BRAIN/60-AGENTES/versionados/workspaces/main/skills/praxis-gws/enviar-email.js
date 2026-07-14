#!/usr/bin/env node
/**
 * Envio simples de e-mail via Gmail API.
 * Uso: node enviar-email.js "destino@exemplo.com" "Assunto" "Corpo" [anexo]
 */
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const CONFIG_DIR = path.join(process.env.HOME || '/tmp', '.config', 'praxis-gws');
const TOKEN_PATH = path.join(CONFIG_DIR, 'token.json');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');

function b64url(input) {
  return Buffer.from(input).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

const [to, subject, body, attachmentPath] = process.argv.slice(2);
if (!to || !subject || !body) {
  console.error('Uso: node enviar-email.js "destino@exemplo.com" "Assunto" "Corpo" [anexo]');
  process.exit(1);
}

async function main() {
  if (!fs.existsSync(CREDENTIALS_PATH)) throw new Error(`credentials.json não encontrado em ${CREDENTIALS_PATH}`);
  if (!fs.existsSync(TOKEN_PATH)) throw new Error(`token.json não encontrado em ${TOKEN_PATH}`);
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
  const auth = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  auth.setCredentials(JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8')));
  const gmail = google.gmail({ version: 'v1', auth });

  const boundary = 'boundary_' + Date.now();
  const msg = [];
  if (process.env.GOOGLE_FROM_EMAIL) msg.push(`From: ${process.env.GOOGLE_FROM_EMAIL}`);
  msg.push(`To: ${to}`);
  msg.push(`Subject: =?utf-8?B?${Buffer.from(subject).toString('base64')}?=`);
  msg.push('MIME-Version: 1.0');

  if (attachmentPath && fs.existsSync(attachmentPath)) {
    const fileName = path.basename(attachmentPath);
    const fileContent = fs.readFileSync(attachmentPath).toString('base64').replace(/(.{76})/g, '$1\r\n');
    msg.push(`Content-Type: multipart/mixed; boundary="${boundary}"`, '', `--${boundary}`);
    msg.push('Content-Type: text/plain; charset=utf-8', 'Content-Transfer-Encoding: 8bit', '', body, '', `--${boundary}`);
    msg.push(`Content-Type: application/octet-stream; name="${fileName}"`);
    msg.push('Content-Transfer-Encoding: base64', `Content-Disposition: attachment; filename="${fileName}"`, '', fileContent, '', `--${boundary}--`);
  } else {
    msg.push('Content-Type: text/plain; charset=utf-8', 'Content-Transfer-Encoding: 8bit', '', body);
  }

  const res = await gmail.users.messages.send({ userId: 'me', requestBody: { raw: b64url(msg.join('\r\n')) } });
  console.log('E-mail enviado. ID:', res.data.id);
}
main().catch(err => { console.error('Erro:', err.message); process.exit(1); });
