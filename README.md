# Budget, appli perso de suivi d'argent

PWA (appli web installable). Toutes les données restent **sur le téléphone**. Internet sert seulement à télécharger les actus.

## Mise en ligne (une seule fois)

Le code est déjà sur GitHub (`Mal-VI/Budget`). Il reste 3 réglages, à faire depuis un navigateur (le site github.com, pas l'appli GitHub) :

1. **Rendre le dépôt public** : Settings > General > tout en bas *Danger Zone* > **Change visibility** > Public. GitHub Pages gratuit ne marche pas sur un dépôt privé. Aucune donnée perso n'est dans le dépôt : tes opérations restent sur le téléphone.
2. **Settings > Pages** : Source = *Deploy from a branch*, choisis la branche du dépôt et le dossier `/ (root)`, puis **Save**. Après 1 ou 2 minutes, l'appli est en ligne sur `https://mal-vi.github.io/Budget/`
3. **Actions** : ouvre « Actualités » et clique sur **Run workflow** pour la première récupération des actus. Si l'étape échoue avec une erreur de permission : **Settings > Actions > General > Workflow permissions** > **Read and write**, puis relance.

## Installer sur le téléphone

- **iPhone** : ouvre le lien dans **Safari**, puis Partager > **Sur l'écran d'accueil**.
- **Android** : ouvre le lien dans **Chrome**, puis menu ⋮ > **Installer l'application**.

Ouvre-la toujours depuis l'icône : c'est là que tes données sont stockées. Safari et l'appli installée ne partagent pas les mêmes données sur iPhone.

## Importer ses relevés

Depuis le site ou l'appli de ta banque, exporte tes opérations en **CSV**. Dans l'appli, va dans ⚙︎ > **Importer un relevé (CSV)**.
- Les doublons sont ignorés : tu peux réimporter une période qui se chevauche. Une opération importée que tu as supprimée ne revient pas non plus.
- Les opérations non reconnues sont marquées « à classer ». Quand tu en classes une, l'appli retient le commerçant et classe automatiquement les mêmes la prochaine fois.

## Sauvegarde

⚙︎ > **Exporter une sauvegarde**, à faire régulièrement (l'accueil te le rappelle au bout de 30 jours). Sur téléphone, ça ouvre le menu de partage : choisis « Enregistrer dans Fichiers » ou Drive. Si tu effaces les données du navigateur ou si tu changes de téléphone, tout est perdu sans sauvegarde. Pour récupérer tes données : ⚙︎ > **Restaurer une sauvegarde**.

## Mettre à jour l'appli

Remplace les fichiers sur GitHub et change `VERSION` dans `sw.js`. L'appli récupère la nouvelle version à la prochaine ouverture avec internet, et tes données ne sont pas touchées.

## Actus

`scripts/fetch_news.py` tourne sur GitHub toutes les 3 h, lit les flux de `feeds.json` et écrit `news.json`. Pour changer de sources, modifie `feeds.json`. Un flux en panne est simplement ignoré, et l'onglet Actions indique lesquels répondent (OK / FAIL).
Le tri « Pour toi » se fait sur le téléphone, d'après tes plus grosses catégories de dépenses. Rien de tes données ne part sur GitHub.

À savoir : GitHub peut mettre en pause les tâches planifiées d'un dépôt resté inactif 60 jours. Dans ce cas, réactive-le dans l'onglet Actions.
