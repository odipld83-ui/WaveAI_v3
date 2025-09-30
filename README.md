# 🌊 WaveAI v3 - Agents IA Intelligents

[![Déployer sur Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 Déploiement instantané

### Option 1 : Déploiement automatique avec Render
1. Cliquez sur le bouton "Deploy to Render" ci-dessus
2. Connectez votre compte GitHub
3. L'application se déploie automatiquement
4. Votre WaveAI sera accessible en quelques minutes !

### Option 2 : Déploiement manuel
1. **Fork ce repository** sur votre compte GitHub
2. **Connectez-vous à [Render.com](https://render.com)**
3. **Créez un nouveau "Web Service"**
4. **Connectez votre repository** forké
5. **Render détecte automatiquement** la configuration via `render.yaml`
6. **Cliquez sur "Deploy"** ✅

## 🤖 Fonctionnalités

### 5 Agents IA Spécialisés
- **📧 Alex** - Assistant productivité (emails, Gmail, tâches)
- **💼 Lina** - Experte LinkedIn (networking, posts, stratégie)
- **📱 Marco** - Expert réseaux sociaux (contenu viral, social media)
- **📅 Sofia** - Assistante organisation (calendrier, planning)
- **💬 Kai** - Assistant conversationnel (chat général)

### 🔄 Système IA Triple
1. **OpenAI (GPT-3.5)** - Réponses dynamiques premium
2. **Anthropic (Claude)** - Alternative intelligente
3. **Fallback intelligent** - Fonctionne même sans clés API !

## ⚙️ Configuration (Optionnel)

WaveAI fonctionne immédiatement après déploiement ! Pour une expérience premium :

1. Accédez à la section **"Configuration"** de votre application
2. Ajoutez vos clés API (optionnel) :
   - **OpenAI** : Obtenez votre clé sur [platform.openai.com](https://platform.openai.com/api-keys)
   - **Anthropic** : Obtenez votre clé sur [console.anthropic.com](https://console.anthropic.com/)

🔒 **Sécurité** : Vos clés sont stockées localement dans votre navigateur et ne sont jamais envoyées à nos serveurs.

## 🎯 Comment utiliser

1. **Choisissez votre agent** sur la page d'accueil
2. **Commencez à discuter** naturellement
3. **Obtenez des réponses expertes** adaptées à chaque domaine

## 📱 Fonctionnalités techniques

- ✅ **Interface responsive** - Fonctionne sur tous appareils
- ✅ **Mode hors-ligne intelligent** - Réponses utiles même sans APIs
- ✅ **Sécurité maximale** - Aucune donnée stockée côté serveur
- ✅ **Déploiement gratuit** - Compatible avec le plan gratuit Render
- ✅ **HTTPS automatique** - Sécurisé par défaut

## 🛠️ Structure du projet

```
waveai-v3/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── render.yaml           # Configuration de déploiement
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── chat.html         # Interface de chat
│   └── settings.html     # Configuration
└── README.md             # Ce fichier
```

## 🔧 Développement local

```bash
# Cloner le repository
git clone https://github.com/votre-username/waveai-v3.git
cd waveai-v3

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

Accédez à : http://localhost:5000

## 🌟 Variables d'environnement (optionnel)

Pour configurer des clés API par défaut côté serveur :

```bash
SECRET_KEY=votre-clé-secrète
OPENAI_API_KEY=sk-votre-clé-openai      # Optionnel
ANTHROPIC_API_KEY=sk-ant-votre-clé      # Optionnel
```

## 🚨 Résolution de problèmes

### L'application ne démarre pas
- Vérifiez que tous les fichiers sont présents
- Regardez les logs de déploiement Render
- Assurez-vous que `requirements.txt` est correct

### Les agents ne répondent pas
- Les agents fonctionnent même sans clés API (mode fallback)
- Vérifiez votre connexion internet
- Testez vos clés API dans la section Configuration

### Erreurs de template
- Vérifiez que le dossier `templates/` contient tous les fichiers HTML
- Regardez les logs pour identifier le template manquant

## 📞 Support

- **Issues GitHub** : Rapportez les bugs via les issues
- **Discussions** : Partagez vos idées et questions
- **Wiki** : Documentation détaillée (à venir)

## 🎉 Après le déploiement

Une fois déployé, votre WaveAI sera accessible 24/7 avec :
- 🌐 **URL personnalisée** fournie par Render
- 🔐 **HTTPS automatique** 
- ⚡ **Haute disponibilité**
- 📈 **Scaling automatique**

---

## 🌊 **Surfez sur la vague de l'IA !**

WaveAI v3 - Simple, efficace, et toujours disponible pour vous accompagner dans vos tâches quotidiennes.

**[🚀 Commencer maintenant](https://render.com/deploy)**