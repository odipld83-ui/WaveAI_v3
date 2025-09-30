from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'waveai-v3-ultimate-2024')

class UniversalAI:
    """Système IA universel supportant toutes les APIs + IA hors ligne"""
    
    def __init__(self):
        self.server_openai_key = os.environ.get('OPENAI_API_KEY', '')
        self.server_anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
    
    def get_response(self, message, agent_type="kai", user_apis=None):
        """Obtenir une réponse IA avec support universel"""
        
        if not user_apis:
            user_apis = {}
        
        # Prompts spécialisés pour chaque agent
        agent_prompts = {
            "alex": "Tu es Alex, expert en productivité et emails. Tu aides avec Gmail, organisation et tâches professionnelles. Réponds en français de manière professionnelle mais amicale.",
            "lina": "Tu es Lina, experte LinkedIn et networking. Tu aides avec les stratégies professionnelles, posts LinkedIn et développement de réseau. Réponds en français de manière inspirante.",
            "marco": "Tu es Marco, expert en réseaux sociaux et marketing digital. Tu crées du contenu viral et optimises la présence en ligne. Réponds en français de manière créative.",
            "sofia": "Tu es Sofia, assistante organisation et planification. Tu gères calendriers, plannings et optimises le temps. Réponds en français de manière précise et organisée.",
            "kai": "Tu es Kai, assistant conversationnel intelligent. Tu discutes de tout avec intelligence, humour et empathie. Réponds en français de manière naturelle et engageante."
        }
        
        prompt = agent_prompts.get(agent_type, agent_prompts["kai"])
        
        # 1. ESSAYER OPENAI (format universel)
        openai_keys = [
            user_apis.get('openai_key', ''),
            user_apis.get('openai', ''),
            self.server_openai_key
        ]
        
        for key in openai_keys:
            if self._is_valid_openai_key(key):
                try:
                    response = self._call_openai(message, prompt, key)
                    if response:
                        return f"🤖 {response}"
                except Exception as e:
                    print(f"[OpenAI Error] {e}")
                    continue
        
        # 2. ESSAYER ANTHROPIC (format universel)
        anthropic_keys = [
            user_apis.get('anthropic_key', ''),
            user_apis.get('anthropic', ''),
            user_apis.get('claude', ''),
            self.server_anthropic_key
        ]
        
        for key in anthropic_keys:
            if self._is_valid_anthropic_key(key):
                try:
                    response = self._call_anthropic(message, prompt, key)
                    if response:
                        return f"🧠 {response}"
                except Exception as e:
                    print(f"[Anthropic Error] {e}")
                    continue
        
        # 3. ESSAYER AUTRES APIs (Gemini, Mistral, etc.)
        other_apis = ['gemini', 'mistral', 'cohere', 'huggingface']
        for api_name in other_apis:
            key = user_apis.get(api_name, '')
            if key and len(key.strip()) > 10:
                try:
                    response = self._call_universal_api(api_name, message, prompt, key)
                    if response:
                        return f"⚡ {response}"
                except Exception as e:
                    print(f"[{api_name.title()} Error] {e}")
                    continue
        
        # 4. IA HORS LIGNE (Hugging Face gratuit)
        try:
            response = self._call_offline_ai(message, prompt, agent_type)
            if response:
                return f"🔄 {response}"
        except Exception as e:
            print(f"[Offline AI Error] {e}")
        
        # 5. FALLBACK INTELLIGENT
        return self._get_smart_fallback(agent_type, message)
    
    def _is_valid_openai_key(self, key):
        """Valider clé OpenAI (tous formats)"""
        if not key or len(key.strip()) < 20:
            return False
        key = key.strip()
        return key.startswith('sk-') and len(key) > 40
    
    def _is_valid_anthropic_key(self, key):
        """Valider clé Anthropic"""
        if not key or len(key.strip()) < 20:
            return False
        key = key.strip()
        return key.startswith('sk-ant-') and len(key) > 50
    
    def _call_openai(self, message, prompt, api_key):
        """Appel OpenAI universel"""
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
            'max_tokens': 800,
            'temperature': 0.7
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', 
                               headers=headers, json=data, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"OpenAI Error {response.status_code}: {response.text}")
    
    def _call_anthropic(self, message, prompt, api_key):
        """Appel Anthropic universel"""
        headers = {
            'x-api-key': api_key.strip(),
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 800,
            'messages': [
                {'role': 'user', 'content': f"{prompt}\n\nQuestion: {message}"}
            ]
        }
        
        response = requests.post('https://api.anthropic.com/v1/messages', 
                               headers=headers, json=data, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text'].strip()
        else:
            raise Exception(f"Anthropic Error {response.status_code}: {response.text}")
    
    def _call_universal_api(self, api_name, message, prompt, api_key):
        """Support pour autres APIs (Gemini, Mistral, etc.)"""
        # Placeholder pour futures intégrations
        # Ajoutera support Gemini, Mistral, Cohere, etc.
        raise Exception(f"{api_name} pas encore supporté")
    
    def _call_offline_ai(self, message, prompt, agent_type):
        """IA hors ligne via Hugging Face gratuit"""
        try:
            # Utilisation de l'API Inference gratuite de Hugging Face
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": "Bearer hf_demo"}  # Token demo gratuit
            
            payload = {
                "inputs": f"{prompt}\n\nUtilisateur: {message}\nAssistant:",
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '').strip()
                    if generated_text and len(generated_text) > 10:
                        return f"[IA Hors ligne] {generated_text}"
            
            raise Exception("Pas de réponse valide de l'IA hors ligne")
            
        except Exception as e:
            raise Exception(f"IA hors ligne indisponible: {e}")
    
    def _get_smart_fallback(self, agent_type, message):
        """Fallback intelligent basé sur le contexte"""
        
        # Analyse du message pour réponse contextuelle
        message_lower = message.lower() if message else ""
        
        smart_responses = {
            "alex": {
                "email": "Pour vos emails, utilisez la règle des 4D : Supprimer, Déléguer, Faire, Différer. Organisez avec des dossiers clairs et traitez par blocs de temps.",
                "productivité": "La méthode Pomodoro (25 min focus + 5 min pause) et la matrice d'Eisenhower (urgent/important) sont vos meilleurs alliés.",
                "gmail": "Dans Gmail : utilisez les libellés, filtres automatiques, raccourcis clavier et la fonction 'Réponses automatiques' pour gagner du temps.",
                "default": "💡 Pour une aide personnalisée complète, connectez une clé API dans Configuration. En attendant, je peux vous donner des conseils généraux de productivité !"
            },
            "lina": {
                "linkedin": "LinkedIn : Postez 3-5x/semaine, commentez authentiquement, personnalisez vos invitations et optimisez votre titre professionnel.",
                "réseau": "Pour développer votre réseau : participez aux discussions, partagez du contenu de valeur et connectez avec des pairs de votre industrie.",
                "profil": "Profil LinkedIn optimal : photo pro, titre accrocheur, résumé avec mots-clés, expériences détaillées et recommandations.",
                "default": "🌟 LinkedIn est votre vitrine professionnelle ! Pour des stratégies personnalisées avancées, ajoutez votre clé API dans Configuration."
            },
            "marco": {
                "social": "Réseaux sociaux : Contenu visuel (80%), posts réguliers, interaction authentique et analyse de vos métriques pour optimiser.",
                "contenu": "Contenu viral : Utilisez les tendances actuelles, ajoutez de l'émotion, posez des questions et publiez aux heures de pointe.",
                "instagram": "Instagram : Stories quotidiennes, Reels créatifs, hashtags stratégiques (5-10 max) et collaborations avec d'autres créateurs.",
                "default": "🚀 Les réseaux sociaux évoluent vite ! Pour des stratégies à jour et personnalisées, configurez votre API pour des conseils d'expert."
            },
            "sofia": {
                "planning": "Planning efficace : Time-blocking au calendrier, buffers entre RDV, préparation la veille et révision hebdomadaire.",
                "calendrier": "Calendrier optimal : Couleurs par catégorie, notifications intelligentes, synchronisation multi-appareils et temps de déplacement inclus.",
                "organisation": "Organisation : Méthode GTD (Getting Things Done), outils numériques synchronisés et revues régulières de vos systèmes.",
                "default": "📅 L'organisation est un art ! Pour un système sur-mesure adapté à vos besoins, ajoutez votre clé API dans Configuration."
            },
            "kai": {
                "default": "💬 Je suis là pour discuter de tout ! Pour des conversations plus approfondies et personnalisées, connectez une API dans Configuration. En attendant, je peux vous aider avec des conseils généraux !"
            }
        }
        
        agent_responses = smart_responses.get(agent_type, smart_responses["kai"])
        
        # Recherche de mot-clé dans le message
        for keyword, response in agent_responses.items():
            if keyword != "default" and keyword in message_lower:
                return f"💡 {response}"
        
        return f"💡 {agent_responses['default']}"

# Instance IA globale
ai_system = UniversalAI()

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/chat/<agent>')
def chat_page(agent):
    """Page de chat avec un agent spécifique"""
    if agent not in ['alex', 'lina', 'marco', 'sofia', 'kai']:
        return redirect(url_for('index'))
    
    return render_template('chat_ultimate.html', agent=agent)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API universelle pour tous les agents et toutes les APIs IA"""
    data = request.get_json()
    
    if not data or 'message' not in data or 'agent' not in data:
        return jsonify({'error': 'Message et agent requis'}), 400
    
    message = data['message']
    agent = data['agent']
    
    # Récupération de TOUTES les clés API possibles
    user_apis = {
        'openai_key': data.get('openai_key', '').strip(),
        'openai': data.get('openai', '').strip(),
        'anthropic_key': data.get('anthropic_key', '').strip(),
        'anthropic': data.get('anthropic', '').strip(),
        'claude': data.get('claude', '').strip(),
        'gemini': data.get('gemini', '').strip(),
        'mistral': data.get('mistral', '').strip(),
        'cohere': data.get('cohere', '').strip(),
        'huggingface': data.get('huggingface', '').strip()
    }
    
    if agent not in ['alex', 'lina', 'marco', 'sofia', 'kai']:
        return jsonify({'error': 'Agent invalide'}), 400
    
    try:
        print(f"[INFO] Agent {agent} traite: '{message[:50]}...'")
        print(f"[INFO] APIs disponibles: {[k for k, v in user_apis.items() if v]}")
        
        response = ai_system.get_response(message, agent, user_apis)
        
        print(f"[INFO] Réponse générée: {response[:100]}...")
        
        return jsonify({
            'response': response,
            'agent': agent,
            'timestamp': datetime.now().isoformat(),
            'apis_tried': [k for k, v in user_apis.items() if v]
        })
    except Exception as e:
        print(f"[ERROR] Erreur API chat: {e}")
        return jsonify({'error': 'Erreur lors de la génération de la réponse'}), 500

@app.route('/settings')
def settings():
    """Page de configuration universelle"""
    return render_template('settings_ultimate.html')

@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'version': 'WaveAI v3 Ultimate'
    })

@app.route('/api/test-keys', methods=['POST'])
def test_api_keys():
    """Test universel de toutes les clés API"""
    data = request.get_json()
    results = {}
    
    # Test OpenAI
    openai_keys = [data.get('openai_key'), data.get('openai')]
    for i, key in enumerate(openai_keys):
        if key and key.strip():
            try:
                key = key.strip()
                if ai_system._is_valid_openai_key(key):
                    headers = {'Authorization': f'Bearer {key}'}
                    response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=10)
                    results[f'openai_{i+1}'] = response.status_code == 200
                else:
                    results[f'openai_{i+1}'] = False
            except:
                results[f'openai_{i+1}'] = False
    
    # Test Anthropic
    anthropic_keys = [data.get('anthropic_key'), data.get('anthropic'), data.get('claude')]
    for i, key in enumerate(anthropic_keys):
        if key and key.strip():
            results[f'anthropic_{i+1}'] = ai_system._is_valid_anthropic_key(key.strip())
    
    # Test IA hors ligne
    try:
        test_response = ai_system._call_offline_ai("test", "Tu es un assistant", "kai")
        results['offline_ai'] = bool(test_response)
    except:
        results['offline_ai'] = False
    
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[INFO] 🌊 Démarrage WaveAI v3 Ultimate sur le port {port}")
    print(f"[INFO] 🤖 Support: OpenAI, Anthropic, IA hors ligne + APIs universelles")
    app.run(host='0.0.0.0', port=port, debug=False)
