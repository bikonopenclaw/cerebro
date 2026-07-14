#!/usr/bin/env node
/**
 * Renomear arquivo no Drive
 * Uso: node rename-file.js <fileId> <novo-nome>
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME, '.config', 'praxis-gws');
const TOKEN_PATH = path.join(CONFIG_DIR, 'token.json');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');

function getAuthClient() {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
  oAuth2Client.setCredentials(token);
  return oAuth2Client;
}

async function renameFile(fileId, newName) {
  const auth = getAuthClient();
  const drv = google.drive({ version: 'v3', auth });
  const res = await drv.files.update({
    fileId: fileId,
    requestBody: { name: newName },
    fields: 'id, name, webViewLink',
  });
  return res.data;
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('Uso: node rename-file.js <fileId> <novo-nome>');
    process.exit(1);
  }
  
  const [fileId, newName] = args;
  
  console.log(`🏷️  Renomeando arquivo...`);
  const renamed = await renameFile(fileId, newName);
  console.log(`✅ Renomeado: ${renamed.name}`);
  console.log(`🔗 Link: ${renamed.webViewLink}`);
}

main().catch(err => {
  console.error('❌ ERRO:', err.message);
  process.exit(1);
});
