# 🚀 Guide de Déploiement WaveAI v3

## 📋 Étapes de déploiement GitHub + Render

### 1. 📁 Créer le repository GitHub

1. **Connectez-vous à GitHub** : [github.com](https://github.com)
2. **Cliquez sur "New repository"** (bouton vert)
3. **Configurez le repository** :
   - **Nom** : `waveai-v3`
   - **Description** : `🌊 WaveAI v3 - Agents IA Intelligents avec 5 spécialistes`
   - **Visibilité** : Public (pour le déploiement gratuit)
   - ✅ **Cochez "Add a README file"**
   - **Licence** : MIT License

### 2. 📤 Uploader les fichiers

**Option A : Via l'interface GitHub** (Plus simple)
1. Cliquez sur **"uploading an existing file"**
2. **Glissez-déposez** tous les fichiers de votre dossier `waveai-v3/`
3. **Commit message** : `🌊 Initial WaveAI v3 - Ready for deployment`
4. Cliquez sur **"Commit changes"**

**Option B : Via Git en ligne de commande**
```bash
git clone https://github.com/votre-username/waveai-v3.git
cd waveai-v3
# Copiez tous vos fichiers ici
git add .
git commit -m "🌊 Initial WaveAI v3 - Ready for deployment"
git push origin main
```

### 3. 🚀 Déployer sur Render

1. **Connectez-vous à Render** : [render.com](https://render.com)
2. **Cliquez sur "New +"** → **"Web Service"**
3. **Configurez le service** :
   - **Source** : Connect GitHub repository
   - **Repository** : Sélectionnez `waveai-v3`
   - **Branch** : `main`
   - **Root Directory** : (laissez vide)
   
4. **Configuration auto-détectée** :
   - **Runtime** : Python 3 ✅
   - **Build Command** : `pip install -r requirements.txt` ✅
   - **Start Command** : `python app.py` ✅

5. **Plan** : Sélectionnez **"Free"** 💰

6. **Variables d'environnement** (optionnel) :
   - `SECRET_KEY` : Render le génère automatiquement ✅
   - `OPENAI_API_KEY` : (optionnel - ajoutez si vous voulez)
   - `ANTHROPIC_API_KEY` : (optionnel - ajoutez si vous voulez)

7. **Cliquez sur "Create Web Service"** 🚀

### 4. ⏱️ Attendre le déploiement

- **Durée** : 2-5 minutes ⏰
- **Logs** : Surveillez les logs de build
- **Status** : Attendez le ✅ "Live"

### 5. 🎉 Votre WaveAI est en ligne !

Render vous donnera une URL comme :
**`https://waveai-v3-xxxx.onrender.com`**

## 🔧 Configuration post-déploiement

### 🌐 URL personnalisée (optionnel)
- Dans Render, allez dans **Settings** → **Custom Domains**
- Ajoutez votre domaine personnalisé

### 🔑 Clés API utilisateur
- Vos utilisateurs peuvent ajouter leurs propres clés dans **Configuration**
- Les clés sont stockées localement, pas sur vos serveurs

### 📊 Monitoring
- **Health Check** : `https://votre-url/health`
- **Logs** : Disponibles dans le dashboard Render
- **Métriques** : CPU, mémoire, requêtes

## 🛠️ Mises à jour

Pour mettre à jour votre application :

1. **Modifiez vos fichiers** localement
2. **Committez sur GitHub** :
   ```bash
   git add .
   git commit -m "🔧 Amélioration WaveAI v3"
   git push origin main
   ```
3. **Render redéploie automatiquement** ! 🔄

## 🚨 Résolution de problèmes

### ❗ Build échoue
- Vérifiez `requirements.txt`
- Regardez les logs de build
- Assurez-vous que tous les fichiers sont présents

### 🔌 Application ne démarre pas
- Vérifiez que `app.py` existe
- Regardez les logs runtime
- Testez localement avec `python app.py`

### 🤖 Agents ne répondent pas
- Les agents fonctionnent même sans clés API !
- Vérifiez les logs pour les erreurs
- Testez l'endpoint `/health`

## 📞 Support rapide

### 🔍 URLs de test
- **Page d'accueil** : `https://votre-url/`
- **Chat Alex** : `https://votre-url/chat/alex`
- **Configuration** : `https://votre-url/settings`
- **Health Check** : `https://votre-url/health`

### 🧪 Test local avant déploiement
```bash
cd waveai-v3
pip install -r requirements.txt
python app.py
# Testez sur http://localhost:5000
```

---

## ✅ Checklist de déploiement

- [ ] Repository GitHub créé
- [ ] Tous les fichiers uploadés
- [ ] Service Render configuré
- [ ] Déploiement réussi (Status: Live)
- [ ] Tests des 5 agents
- [ ] Configuration optionnelle testée
- [ ] URL partagée avec les utilisateurs

**🌊 Votre WaveAI v3 est maintenant accessible 24/7 dans le monde entier !**