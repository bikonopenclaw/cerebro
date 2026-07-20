#!/usr/bin/env node
/**
 * Drive CLI - Lista arquivos e pastas do Google Drive
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

async function search(query, max = 10) {
  const auth = getAuthClient();
  const drv = google.drive({ version: 'v3', auth });
  
  const res = await drv.files.list({
    q: query,
    pageSize: max,
    fields: 'files(id, name, mimeType, modifiedTime, size)',
  });
  
  const files = res.data.files || [];
  console.log(JSON.stringify(files, null, 2));
}

async function listFolders(max = 20) {
  const auth = getAuthClient();
  const drv = google.drive({ version: 'v3', auth });
  
  const res = await drv.files.list({
    q: "mimeType = 'application/vnd.google-apps.folder' and trashed = false",
    pageSize: max,
    fields: 'files(id, name, parents)',
  });
  
  const folders = res.data.files || [];
  console.log(JSON.stringify(folders, null, 2));
}

async function getMetadata(fileId) {
  const auth = getAuthClient();
  const drv = google.drive({ version: 'v3', auth });
  
  const res = await drv.files.get({
    fileId,
    fields: '*',
  });
  
  console.log(JSON.stringify(res.data, null, 2));
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

if (!command || command === '--help') {
  console.log('Drive CLI - Google Drive (praxis-gws)');
  console.log('');
  console.log('Uso:');
  console.log('  node drive-cli.js search <query> [max]  - Busca arquivos');
  console.log('  node drive-cli.js folders [max]         - Lista pastas');
  console.log('  node drive-cli.js get <fileId>          - Metadata do arquivo');
  console.log('');
  console.log('Exemplos de query:');
  console.log("  \"name contains 'Marques'\"");
  console.log("  \"mimeType = 'application/vnd.google-apps.document'\"");
  console.log("  \"mimeType = 'application/pdf'\"");
  console.log('  "modifiedTime > \'2026-03-01\'"');
  process.exit(0);
}

if (command === 'search') {
  const query = args[1] || '';
  const max = parseInt(args[2]) || 10;
  search(query, max);
} else if (command === 'folders') {
  const max = parseInt(args[1]) || 20;
  listFolders(max);
} else if (command === 'get') {
  if (!args[1]) {
    console.error('Erro: informe o fileId');
    process.exit(1);
  }
  getMetadata(args[1]);
} else {
  console.error('Comando desconhecido:', command);
  process.exit(1);
}
