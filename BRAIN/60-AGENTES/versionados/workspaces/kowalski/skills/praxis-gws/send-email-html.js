#!/usr/bin/env node
/**
 * Enviar e-mail HTML via Gmail API.
 * Uso: node send-email-html.js <destino> <assunto> <html_ou_arquivo.html> [anexo]
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

async function authClient() {
  if (!fs.existsSync(CREDENTIALS_PATH)) throw new Error(`credentials.json não encontrado em ${CREDENTIALS_PATH}`);
  if (!fs.existsSync(TOKEN_PATH)) throw new Error(`token.json não encontrado em ${TOKEN_PATH}`);
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
  const auth = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  auth.setCredentials(JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8')));
  return auth;
}

async function sendEmail(to, subject, htmlContent, attachmentPath = null) {
  const gmail = google.gmail({ version: 'v1', auth: await authClient() });
  const boundary = 'boundary_' + Date.now();
  const message = [];
  if (process.env.GOOGLE_FROM_EMAIL) message.push(`From: ${process.env.GOOGLE_FROM_EMAIL}`);
  message.push(`To: ${to}`);
  message.push(`Subject: =?utf-8?B?${Buffer.from(subject).toString('base64')}?=`);
  message.push('MIME-Version: 1.0');

  if (attachmentPath && fs.existsSync(attachmentPath)) {
    const fileName = path.basename(attachmentPath);
    const fileContent = fs.readFileSync(attachmentPath).toString('base64').replace(/(.{76})/g, '$1\r\n');
    message.push(`Content-Type: multipart/mixed; boundary="${boundary}"`, '', `--${boundary}`);
    message.push('Content-Type: text/html; charset=utf-8', 'Content-Transfer-Encoding: 8bit', '', htmlContent, '', `--${boundary}`);
    message.push(`Content-Type: application/octet-stream; name="${fileName}"`);
    message.push('Content-Transfer-Encoding: base64', `Content-Disposition: attachment; filename="${fileName}"`, '', fileContent, '', `--${boundary}--`);
  } else {
    message.push('Content-Type: text/html; charset=utf-8', 'Content-Transfer-Encoding: 8bit', '', htmlContent);
  }

  const res = await gmail.users.messages.send({ userId: 'me', requestBody: { raw: b64url(message.join('\r\n')) } });
  console.log('E-mail enviado. ID:', res.data.id);
}

const [to, subject, htmlArg, attachment] = process.argv.slice(2);
if (!to || !subject || !htmlArg) {
  console.error('Uso: node send-email-html.js <destino> <assunto> <html_ou_arquivo.html> [anexo]');
  process.exit(1);
}
let htmlContent;
if (htmlArg.includes('<html') || htmlArg.includes('<!DOCTYPE')) htmlContent = htmlArg;
else if (fs.existsSync(htmlArg)) htmlContent = fs.readFileSync(htmlArg, 'utf-8');
else { console.error('HTML inválido ou arquivo não encontrado:', htmlArg); process.exit(1); }

sendEmail(to, subject, htmlContent, attachment).catch(err => { console.error('Erro:', err.message); process.exit(1); });
