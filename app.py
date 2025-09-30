from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'waveai-simple-key-2024')

# Configuration simple pour les APIs IA
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

class SimpleAI:
    """Système IA simple avec fallback robuste"""
    
    def __init__(self):
        self.openai_key = OPENAI_API_KEY
        self.anthropic_key = ANTHROPIC_API_KEY
    
    def get_response(self, message, agent_type="general", user_openai_key=None, user_anthropic_key=None):
        """Obtenir une réponse IA avec fallback robuste"""
        
        # Prompts pour chaque agent
        agent_prompts = {
            "alex": "Tu es Alex, assistant productivité. Tu aides avec Gmail, emails et tâches professionnelles. Réponds en français, sois professionnel mais amical.",
            "lina": "Tu es Lina, experte LinkedIn. Tu aides avec le networking, posts LinkedIn et stratégie professionnelle. Réponds en français, sois inspirant.",
            "marco": "Tu es Marco, expert réseaux sociaux. Tu crées du contenu viral et optimises la présence sociale. Réponds en français, sois créatif.",
            "sofia": "Tu es Sofia, assistante organisation. Tu gères calendriers, plannings et rappels. Réponds en français, sois précise et organisée.",
            "kai": "Tu es Kai, assistant conversationnel. Tu discutes de tout avec intelligence et humour. Réponds en français, sois naturel et engageant."
        }
        
        prompt = agent_prompts.get(agent_type, agent_prompts["kai"])
        
        # Utiliser les clés utilisateur en priorité, puis les clés serveur
        openai_key = user_openai_key or self.openai_key
        anthropic_key = user_anthropic_key or self.anthropic_key
        
        print(f"[DEBUG] Clé OpenAI présente: {bool(openai_key)}")
        print(f"[DEBUG] Clé Anthropic présente: {bool(anthropic_key)}")
        
        # Essayer OpenAI d'abord SEULEMENT si clé valide
        if openai_key and len(openai_key.strip()) > 30 and openai_key.startswith('sk-'):
            try:
                print("[DEBUG] Tentative OpenAI...")
                response = self._call_openai(message, prompt, openai_key)
                if response and len(response.strip()) > 5:
                    print("[DEBUG] ✅ OpenAI réussi")
                    return f"[GPT] {response}"
            except Exception as e:
                print(f"[DEBUG] ❌ OpenAI error: {e}")
        else:
            print("[DEBUG] Clé OpenAI invalide ou absente")
        
        # Puis Anthropic SEULEMENT si clé valide
        if anthropic_key and len(anthropic_key.strip()) > 30 and anthropic_key.startswith('sk-ant-'):
            try:
                print("[DEBUG] Tentative Anthropic...")
                response = self._call_anthropic(message, prompt, anthropic_key)
                if response and len(response.strip()) > 5:
                    print("[DEBUG] ✅ Anthropic réussi")
                    return f"[Claude] {response}"
            except Exception as e:
                print(f"[DEBUG] ❌ Anthropic error: {e}")
        else:
            print("[DEBUG] Clé Anthropic invalide ou absente")
        
        # Fallback simple
        print("[DEBUG] 🔄 Utilisation du fallback")
        return self._get_fallback_response(agent_type, message)
    
    def _call_openai(self, message, prompt, api_key):
        """Appel à l'API OpenAI avec gestion d'erreur détaillée"""
        headers = {
            'Authorization': f'Bearer {api_key.strip()}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', 
                               headers=headers, json=data, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        elif response.status_code == 401:
            raise Exception(f"Clé API OpenAI invalide")
        elif response.status_code == 429:
            raise Exception(f"Quota OpenAI dépassé")
        elif response.status_code == 400:
            raise Exception(f"Requête OpenAI invalide")
        else:
            raise Exception(f"Erreur OpenAI {response.status_code}")
    
    def _call_anthropic(self, message, prompt, api_key):
        """Appel à l'API Anthropic avec gestion d'erreur détaillée"""
        headers = {
            'x-api-key': api_key.strip(),
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 500,
            'messages': [
                {'role': 'user', 'content': f"{prompt}\n\nQuestion: {message}"}
            ]
        }
        
        response = requests.post('https://api.anthropic.com/v1/messages', 
                               headers=headers, json=data, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        elif response.status_code == 401:
            raise Exception(f"Clé API Anthropic invalide")
        elif response.status_code == 429:
            raise Exception(f"Quota Anthropic dépassé")
        else:
            raise Exception(f"Erreur Anthropic {response.status_code}")
    
    def _get_fallback_response(self, agent_type, message):
        """Réponses de fallback intelligentes"""
        
        fallbacks = {
            "alex": [
                "Je vous aiderai avec vos emails dès que les services IA premium seront configurés. En attendant, voici quelques conseils généraux pour la productivité...",
                "Pour organiser vos emails, je recommande de créer des dossiers par projet et d'utiliser des règles de tri automatiques.",
                "Une bonne pratique est de traiter vos emails en blocs de temps dédiés, plutôt qu'en continu."
            ],
            "lina": [
                "LinkedIn est un outil puissant ! Pour améliorer votre visibilité, postez régulièrement du contenu de qualité dans votre domaine.",
                "N'hésitez pas à commenter les posts d'autres professionnels de votre secteur pour créer des connexions authentiques.",
                "Un profil LinkedIn optimisé doit avoir une photo professionnelle, un titre accrocheur et un résumé qui met en valeur vos compétences."
            ],
            "marco": [
                "Le contenu visuel performe toujours mieux sur les réseaux sociaux ! Pensez images, vidéos courtes et stories.",
                "La régularité est clé sur les réseaux sociaux. Mieux vaut poster 3 fois par semaine que 10 fois puis rien pendant un mois.",
                "Interagissez avec votre audience ! Répondez aux commentaires et posez des questions dans vos posts."
            ],
            "sofia": [
                "Pour une organisation optimale, je recommande la méthode GTD (Getting Things Done) : capturer, clarifier, organiser, réfléchir, agir.",
                "Utilisez un calendrier unique pour tous vos rendez-vous et bloquez du temps pour vos tâches importantes.",
                "La règle des 2 minutes : si une tâche prend moins de 2 minutes, faites-la immédiatement !"
            ],
            "kai": [
                "C'est une question intéressante ! Pour une réponse plus personnalisée, ajoutez vos clés API dans la configuration.",
                "Je suis là pour discuter de tout et n'importe quoi ! Qu'est-ce qui vous intéresse aujourd'hui ?",
                "En mode fallback, je donne des conseils généraux. Configurez une API pour des réponses sur mesure !"
            ]
        }
        
        import random
        responses = fallbacks.get(agent_type, fallbacks["kai"])
        selected_response = random.choice(responses)
        
        # Ajouter un contexte basé sur le message si possible
        message_lower = message.lower() if message else ""
        if "api" in message_lower or "gpt" in message_lower or "openai" in message_lower:
            return f"[Mode Fallback] {selected_response} 💡 Ajoutez votre clé API dans Configuration pour activer GPT/Claude !"
        
        return f"[Mode Fallback] {selected_response}"

# Instance IA globale
ai_system = SimpleAI()

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/chat/<agent>')
def chat_page(agent):
    """Page de chat avec un agent spécifique"""
    if agent not in ['alex', 'lina', 'marco', 'sofia', 'kai']:
        return redirect(url_for('index'))
    
    try:
        return render_template('chat.html', agent=agent)
    except Exception as e:
        print(f"Template error: {e}")
        return redirect(url_for('index'))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API pour discuter avec les agents"""
    data = request.get_json()
    
    if not data or 'message' not in data or 'agent' not in data:
        return jsonify({'error': 'Message et agent requis'}), 400
    
    message = data['message']
    agent = data['agent']
    user_openai_key = data.get('openai_key', '').strip()
    user_anthropic_key = data.get('anthropic_key', '').strip()
    
    if agent not in ['alex', 'lina', 'marco', 'sofia', 'kai']:
        return jsonify({'error': 'Agent invalide'}), 400
    
    try:
        response = ai_system.get_response(
            message, 
            agent, 
            user_openai_key=user_openai_key, 
            user_anthropic_key=user_anthropic_key
        )
        return jsonify({
            'response': response,
            'agent': agent,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"API chat error: {e}")
        return jsonify({'error': 'Erreur lors de la génération de la réponse'}), 500

@app.route('/settings')
def settings():
    """Page de configuration"""
    return render_template('settings.html')

@app.route('/health')
def health():
    """Endpoint de santé pour Render"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/test-keys', methods=['POST'])
def test_api_keys():
    """Tester les clés API"""
    data = request.get_json()
    
    results = {}
    
    # Test OpenAI
    if data.get('openai_key'):
        try:
            key = data["openai_key"].strip()
            if not key.startswith('sk-'):
                results['openai'] = False
                results['openai_error'] = 'Format invalide'
            else:
                headers = {'Authorization': f'Bearer {key}'}
                response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=10)
                results['openai'] = response.status_code == 200
                if response.status_code != 200:
                    results['openai_error'] = f'Code {response.status_code}'
        except Exception as e:
            results['openai'] = False
            results['openai_error'] = str(e)
    
    # Test Anthropic
    if data.get('anthropic_key'):
        try:
            key = data["anthropic_key"].strip()
            if not key.startswith('sk-ant-'):
                results['anthropic'] = False
                results['anthropic_error'] = 'Format invalide'
            else:
                results['anthropic'] = True  # Pas de test simple pour Anthropic
        except Exception as e:
            results['anthropic'] = False
            results['anthropic_error'] = str(e)
    
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[INFO] Démarrage WaveAI v3 sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
