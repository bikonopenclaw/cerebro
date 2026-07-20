const { google } = require('googleapis');
const fs = require('fs');

const tokenPath = '/mnt/data/openclaw/workspace/.config/praxis-gws/token.json';
const credentialsPath = '/mnt/data/openclaw/workspace/.config/praxis-gws/credentials.json';

const credentials = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
const token = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));

const oauth2Client = new google.auth.OAuth2(
  credentials.installed.client_id,
  credentials.installed.client_secret,
  credentials.installed.redirect_uris[0]
);

oauth2Client.setCredentials(token);

async function listarEmailsRecentes() {
  try {
    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
    
    console.log('📬 Últimos 15 e-mails na caixa de entrada:\n');
    
    const response = await gmail.users.messages.list({
      userId: 'me',
      maxResults: 15
    });
    
    if (!response.data.messages || response.data.messages.length === 0) {
      console.log('❌ Nenhum e-mail encontrado.');
      return;
    }
    
    for (const msg of response.data.messages) {
      const fullMsg = await gmail.users.messages.get({
        userId: 'me',
        id: msg.id,
        format: 'metadata',
        metadataHeaders: ['From', 'Subject', 'Date']
      });
      
      const from = fullMsg.data.payload.headers.find(h => h.name === 'From')?.value || 'Desconhecido';
      const subject = fullMsg.data.payload.headers.find(h => h.name === 'Subject')?.value || 'Sem assunto';
      const date = fullMsg.data.payload.headers.find(h => h.name === 'Date')?.value || 'Desconhecida';
      
      const hasAttachment = fullMsg.data.payload.parts?.some(p => p.filename) ? '📎' : '';
      
      console.log(`${hasAttachment} De: ${from}`);
      console.log(`   Assunto: ${subject}`);
      console.log(`   Data: ${date}`);
      console.log('');
    }
    
  } catch (err) {
    console.error('❌ Erro:', err.message);
  }
}

listarEmailsRecentes();
