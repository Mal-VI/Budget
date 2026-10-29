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

## Ton argent (compte + épargne)

Sur l'accueil, touche **Ton argent** et entre le total que t'affiche ta banque : compte courant + épargne (Livret A…). L'appli ajoute ensuite les opérations datées d'après (importées ou ajoutées à la main). Quand tu regardes un mois passé, elle recalcule ce que tu avais à la fin du mois. Si le montant s'écarte du vrai, touche la case et retape ton total du jour.

Les virements entre ton compte et ton épargne ne changent pas ce total : ils sont classés « Épargne » (vers l'épargne) ou « Depuis l'épargne » (retour sur le compte), souvent automatiquement. Les intérêts du livret ne sont pas suivis : corrige le total de temps en temps.

« Bilan du mois », c'est autre chose : tes revenus moins tes dépenses du mois.

## Importer ses relevés

⚙︎ > **Importer des relevés (PDF ou CSV)**. Tu peux en sélectionner plusieurs d'un coup.
- **PDF** : les relevés de compte du Crédit Agricole (téléchargés depuis l'appli Ma Banque, puis « Enregistrer dans Fichiers »). Le PDF est lu sur le téléphone avec pdf.js (dans `lib/pdfjs`), rien n'est envoyé. L'appli compare ce qu'elle a lu avec la ligne « Total des opérations » du relevé et te dit si ça correspond. Seul le premier compte du relevé est importé (pas les livrets). Il faut internet la première fois pour télécharger le lecteur PDF.
- **CSV** : l'export des opérations depuis le site de ta banque.
- N'importe pas la même période en PDF et en CSV : les libellés diffèrent un peu, donc les opérations seraient en double.
- Les doublons sont ignorés : tu peux réimporter une période qui se chevauche. Une opération importée que tu as supprimée ne revient pas non plus.
- Les opérations non reconnues sont marquées « à classer ». Quand tu en classes une, l'appli retient le commerçant et classe automatiquement les mêmes la prochaine fois.
- Relevé mal lu ? ⚙︎ > **Diagnostic anonymisé** : une version du PDF où les lettres deviennent x et les chiffres 9, qui ne garde que la position du texte. Elle permet de corriger la lecture sans voir tes données.

## Sauvegarde

⚙︎ > **Exporter une sauvegarde**, à faire régulièrement (l'accueil te le rappelle au bout de 30 jours). Sur téléphone, ça ouvre le menu de partage : choisis « Enregistrer dans Fichiers » ou Drive. Si tu effaces les données du navigateur ou si tu changes de téléphone, tout est perdu sans sauvegarde. Pour récupérer tes données : ⚙︎ > **Restaurer une sauvegarde**.

## Mettre à jour l'appli

Remplace les fichiers sur GitHub et change `VERSION` dans `sw.js`. L'appli récupère la nouvelle version à la prochaine ouverture avec internet, et tes données ne sont pas touchées.

## Actus

`scripts/fetch_news.py` tourne sur GitHub toutes les 3 h, lit les flux de `feeds.json` et écrit `news.json`. Pour changer de sources, modifie `feeds.json`. Un flux en panne est simplement ignoré, et l'onglet Actions indique lesquels répondent (OK / FAIL).
Le tri « Pour toi » se fait sur le téléphone, d'après tes plus grosses catégories de dépenses. Rien de tes données ne part sur GitHub.

À savoir : GitHub peut mettre en pause les tâches planifiées d'un dépôt resté inactif 60 jours. Dans ce cas, réactive-le dans l'onglet Actions.
