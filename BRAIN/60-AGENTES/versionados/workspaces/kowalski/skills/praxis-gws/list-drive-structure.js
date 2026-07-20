#!/usr/bin/env node
/**
 * Listar estrutura completa do Google Drive
 * Usa OAuth do praxis-gws
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const TOKEN_PATH = path.join(process.env.HOME, '.config/praxis-gws/token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

async function listDriveStructure(parentId = 'root', indent = 0, maxDepth = 4) {
    if (indent > maxDepth) return;
    
    const prefix = '  '.repeat(indent);
    
    try {
        const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
        const credentials = new google.auth.OAuth2();
        credentials.setCredentials(tokenData);
        
        const drive = google.drive({ version: 'v3', auth: credentials });
        
        const results = await drive.files.list({
            q: `'${parentId}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false`,
            fields: 'files(id, name, modifiedTime)',
            orderBy: 'name',
            pageSize: 100
        });
        
        const folders = results.data.files || [];
        
        for (const folder of folders) {
            console.log(`${prefix}📂 ${folder.name} (ID: ${folder.id})`);
            await listDriveStructure(folder.id, indent + 1, maxDepth);
        }
        
        if (folders.length === 0 && indent === 0) {
            console.log('📁 Nenhuma pasta encontrada no root do Drive');
        }
        
    } catch (error) {
        console.error(`❌ Erro: ${error.message}`);
    }
}

// Executar
console.log('📁 ESTRUTURA COMPLETA DO GOOGLE DRIVE');
console.log('='.repeat(60));
listDriveStructure();
