#!/usr/bin/env node
/**
 * Baixar PDF do Drive via API
 * Uso: node download-pdf.js <FILE_ID> [output.pdf]
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

async function downloadPdf(fileId, outputFile) {
  const auth = getAuthClient();
  const drive = google.drive({ version: 'v3', auth });
  
  console.log(`📄 Baixando PDF: ${fileId}`);
  
  // Metadata
  const metadata = await drive.files.get({
    fileId: fileId,
    fields: 'id, name, mimeType, size',
  });
  
  console.log(`   Nome: ${metadata.data.name}`);
  console.log(`   Tamanho: ${Math.round(metadata.data.size / 1024)} KB`);
  
  // Download
  const res = await drive.files.get(
    { fileId: fileId, alt: 'media' },
    { responseType: 'arraybuffer' }
  );
  
  const buffer = Buffer.from(res.data);
  
  if (outputFile) {
    fs.writeFileSync(outputFile, buffer);
    console.log(`   ✅ Salvo em: ${outputFile}`);
  }
  
  return buffer;
}

// CLI
const fileId = process.argv[2];
const outputFile = process.argv[3];

if (!fileId) {
  console.log('Uso: node download-pdf.js <FILE_ID> [output.pdf]');
  process.exit(1);
}

downloadPdf(fileId, outputFile).catch(err => {
  console.error('❌ Erro:', err.message);
  console.error(err);
  process.exit(1);
});
