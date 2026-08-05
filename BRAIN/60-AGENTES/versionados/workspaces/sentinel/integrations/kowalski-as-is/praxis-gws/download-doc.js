#!/usr/bin/env node
/**
 * Baixar conteúdo de Google Doc via API
 * Uso: node download-doc.js <DOC_ID> [output.txt]
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

async function downloadDoc(docId, outputFile) {
  const auth = getAuthClient();
  const drive = google.drive({ version: 'v3', auth });
  
  console.log(`📄 Baixando documento: ${docId}`);
  
  // Primeiro, pega metadata
  const metadata = await drive.files.get({
    fileId: docId,
    fields: 'id, name, mimeType',
  });
  
  console.log(`   Nome: ${metadata.data.name}`);
  console.log(`   Tipo: ${metadata.data.mimeType}`);
  
  // Exporta como texto
  const res = await drive.files.export(
    { fileId: docId, mimeType: 'text/plain' },
    { responseType: 'text' }
  );
  
  const content = res.data;
  
  if (outputFile) {
    fs.writeFileSync(outputFile, content, 'utf8');
    console.log(`   ✅ Salvo em: ${outputFile}`);
  }
  
  return content;
}

// CLI
const docId = process.argv[2];
const outputFile = process.argv[3];

if (!docId) {
  console.log('Uso: node download-doc.js <DOC_ID> [output.txt]');
  process.exit(1);
}

downloadDoc(docId, outputFile).catch(err => {
  console.error('❌ Erro:', err.message);
  console.error(err);
  process.exit(1);
});
