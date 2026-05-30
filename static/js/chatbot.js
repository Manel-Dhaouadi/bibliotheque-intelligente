// Stocker l'historique
let conversationHistorique = [];
let messageCount = 0;

// Charger l'historique
async function chargerHistorique() {
    try {
        const response = await fetch('/api/chatbot/historique/', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.historique && data.historique.length > 0) {
                conversationHistorique = data.historique;
                messageCount = data.historique.length;
                
                const messagesDiv = document.getElementById('chatMessages');
                messagesDiv.innerHTML = '';
                
                ajouterMessageBot("👋 Bonjour ! Je suis votre assistant IA. Posez-moi vos questions sur les livres !");
                
                for (const msg of data.historique) {
                    ajouterMessageUser(msg.question);
                    ajouterMessageBot(msg.reponse);
                }
            } else {
                ajouterMessageBot("👋 Bonjour ! Je suis votre assistant IA. Posez-moi vos questions sur les livres !");
            }
        } else {
            ajouterMessageBot("👋 Bonjour ! Je suis votre assistant IA. Posez-moi vos questions sur les livres !");
        }
    } catch (error) {
        console.error('Erreur:', error);
        ajouterMessageBot("👋 Bonjour ! Je suis votre assistant IA. Posez-moi vos questions sur les livres !");
    }
}

function ajouterMessageUser(message) {
    const messagesDiv = document.getElementById('chatMessages');
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'message user';
    userMsgDiv.innerHTML = `<div class="message-content">${escapeHtml(message)}</div>`;
    messagesDiv.appendChild(userMsgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function ajouterMessageBot(message) {
    const messagesDiv = document.getElementById('chatMessages');
    const botMsgDiv = document.createElement('div');
    botMsgDiv.className = 'message bot';
    botMsgDiv.innerHTML = `<div class="message-content">${escapeHtml(message)}</div>`;
    messagesDiv.appendChild(botMsgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    
    messageCount++;
    
    ajouterMessageUser(message);
    input.value = '';
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot';
    loadingDiv.id = 'loading';
    loadingDiv.innerHTML = `<div class="message-content">🤔 Réflexion...</div>`;
    document.getElementById('chatMessages').appendChild(loadingDiv);
    
    try {
        const response = await fetch('/api/chatbot/question/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 
                question: message,
                historique: conversationHistorique,
                messageCount: messageCount
            })
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const data = await response.json();
        
        document.getElementById('loading')?.remove();
        ajouterMessageBot(data.reponse);
        
        conversationHistorique.push({
            question: message,
            reponse: data.reponse,
            date: new Date().toLocaleString()
        });
        
        if (conversationHistorique.length > 50) {
            conversationHistorique = conversationHistorique.slice(-50);
        }
        
    } catch (error) {
        document.getElementById('loading')?.remove();
        ajouterMessageBot("❌ Erreur, veuillez réessayer.");
    }
}

function toggleChatbot() {
    const window = document.getElementById('chatbotWindow');
    window.classList.toggle('open');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('chatbotWindow')) {
        chargerHistorique();
    }
});