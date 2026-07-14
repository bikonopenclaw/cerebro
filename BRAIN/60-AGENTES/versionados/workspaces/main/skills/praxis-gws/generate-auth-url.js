const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const CREDENTIALS_PATH = path.join(process.env.HOME, '.config', 'praxis-gws', 'credentials.json');
const TOKEN_PATH = path.join(process.env.HOME, '.config', 'praxis-gws', 'token.json');

async function generateAuthUrl() {
  try {
    console.log('=== GERANDO URL DE AUTENTICAÇÃO ===\n');
    
    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
    const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;
    
    console.log('Client ID:', client_id);
    console.log('Redirect URIs:', redirect_uris.join(', '));
    console.log('');
    
    const oauth2Client = new google.auth.OAuth2(
      client_id,
      client_secret,
      redirect_uris[0]
    );
    
    const scopes = [
      'https://www.googleapis.com/auth/gmail.modify',
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/drive'
    ];
    
    const authUrl = oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: scopes,
      prompt: 'consent' // Força a gerar refresh_token
    });
    
    console.log('=== URL DE AUTENTICAÇÃO ===\n');
    console.log(authUrl);
    console.log('\n=== INSTRUÇÕES ===');
    console.log('1. Copie o URL acima');
    console.log('2. Cole no seu browser');
    console.log('3. Faça login com a conta Google que sera autorizada');
    console.log('4. Autorize o acesso');
    console.log('5. Você será redirecionado para uma URL com ?code=...');
    console.log('6. Copie apenas o código (após ?code=)');
    console.log('7. Execute: node verify-code.js <CODIGO>');
    
  } catch (error) {
    console.error('Erro:', error.message);
  }
}

generateAuthUrl();
