# Budget, appli perso de suivi d'argent

PWA (appli web installable). Toutes les données restent **sur le téléphone**. Internet sert seulement à télécharger les actus.

## Mise en ligne (une seule fois, environ 10 min, plus simple sur PC)

1. Crée un compte sur https://github.com
2. Crée un dépôt : bouton **New** > nom `budget` > **Public** > **Create repository**.
3. Clique sur **uploading an existing file**, puis glisse tout le contenu du dossier (pas le dossier lui-même) : `index.html`, `sw.js`, `manifest.webmanifest`, `news.json`, `feeds.json`, `README.md`, et les dossiers `icons` et `scripts`. Clique sur **Commit changes**.
4. Le dossier `.github` est souvent caché, donc crée ce fichier à la main : **Add file > Create new file**, nom `.github/workflows/news.yml`, colle le contenu du fichier `news.yml` fourni, puis **Commit**.
5. **Settings > Pages** : Source = *Deploy from a branch*, Branch = `main`, dossier `/ (root)`, puis **Save**. Après 1 ou 2 minutes, ton lien apparaît : `https://TONPSEUDO.github.io/budget/`
6. **Actions** : si GitHub te le demande, active les workflows. Ouvre ensuite « Actualités » et clique sur **Run workflow** pour lancer la première récupération. Si l'étape échoue avec une erreur de permission, va dans **Settings > Actions > General > Workflow permissions**, choisis **Read and write**, puis relance.

## Installer sur le téléphone

- **iPhone** : ouvre le lien dans **Safari**, puis Partager > **Sur l'écran d'accueil**.
- **Android** : ouvre le lien dans **Chrome**, puis menu ⋮ > **Installer l'application**.

Ouvre-la toujours depuis l'icône : c'est là que tes données sont stockées. Safari et l'appli installée ne partagent pas les mêmes données sur iPhone.

## Importer ses relevés

Depuis le site ou l'appli de ta banque, exporte tes opérations en **CSV**. Dans l'appli, va dans ⚙︎ > **Importer un relevé (CSV)**.
- Les doublons sont ignorés : tu peux réimporter une période qui se chevauche.
- Les opérations non reconnues sont marquées « à classer ». Quand tu en classes une, l'appli retient le commerçant et classe automatiquement les mêmes la prochaine fois.

## Sauvegarde

⚙︎ > **Exporter une sauvegarde**, à faire régulièrement. Si tu effaces les données du navigateur ou si tu changes de téléphone, tout est perdu sans sauvegarde. Pour récupérer tes données : ⚙︎ > **Restaurer une sauvegarde**.

## Mettre à jour l'appli

Remplace les fichiers sur GitHub. L'appli récupère la nouvelle version à la prochaine ouverture avec internet, et tes données ne sont pas touchées.

## Actus

`scripts/fetch_news.py` tourne sur GitHub toutes les 3 h, lit les flux de `feeds.json` et écrit `news.json`. Pour changer de sources, modifie `feeds.json`. Un flux en panne est simplement ignoré, et l'onglet Actions indique lesquels répondent (OK / FAIL).
Le tri « Pour toi » se fait sur le téléphone, d'après tes plus grosses catégories de dépenses. Rien de tes données ne part sur GitHub.

À savoir : GitHub peut mettre en pause les tâches planifiées d'un dépôt resté inactif 60 jours. Dans ce cas, réactive-le dans l'onglet Actions.
