#!/usr/bin/env node
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME, '.config', 'praxis-gws');
const TOKEN_PATH = path.join(CONFIG_DIR, 'token.json');
const CREDENTIALS_PATH = path.join(CONFIG_DIR, 'credentials.json');

const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;

const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
oAuth2Client.setCredentials(token);

const drv = google.drive({ version: 'v3', auth: oAuth2Client });

async function listFolders() {
  try {
    console.log('📁 Pastas no Drive:\n');
    
    const res = await drv.files.list({
      q: "mimeType = 'application/vnd.google-apps.folder' and trashed = false",
      pageSize: 20,
      fields: 'files(id, name, parents)',
    });
    
    const folders = res.data.files || [];
    folders.forEach(folder => {
      console.log(`📂 ${folder.name} (ID: ${folder.id})`);
    });
  } catch (err) {
    console.error('❌ Erro:', err.message);
  }
}

listFolders();
