import React, { useState } from 'react';
import api from '../services/api';

function ChatbotPage() {
  const [messages, setMessages] = useState([
    { text: "Bonjour ! Je suis votre assistant bibliothécaire intelligent. Posez-moi des questions sur les livres disponibles !", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Ajouter le message de l'utilisateur
    const userMessage = { text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await api.post('/chatbot/question/', { question: inputValue });
      const botMessage = { text: response.data.reponse, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Erreur:', error);
      const errorMessage = { text: "Désolé, une erreur s'est produite. Veuillez réessayer.", sender: 'bot' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-page">
      <h1>🤖 Assistant Bibliothécaire IA</h1>
      <p>Posez-moi des questions sur les livres, leur disponibilité, ou demandez des recommandations !</p>
      
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message bot">
              <div className="message-content">
                <div className="loading">🤔 Réflexion en cours...</div>
              </div>
            </div>
          )}
        </div>
        
        <form onSubmit={handleSendMessage} className="chat-input-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Posez votre question..."
            className="chat-input"
            disabled={loading}
          />
          <button type="submit" className="chat-submit" disabled={loading}>
            Envoyer ✨
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatbotPage;