# Les visuels de la page d'accueil

Les cartes, boutons et titres de la page d'accueil sont des images fabriquées par `generer.py` : chaque élément est mis en page en HTML/CSS, puis photographié par Chrome.

Pour changer un texte ou ajouter un projet :

1. modifier la fonction `composants()` dans `generer.py` ;
2. lancer `pip install playwright imagequant`, puis `python3 design/generer.py` ;
3. les images sont réécrites dans `assets/` ; ajouter la carte correspondante dans `README.md`.

Polices : Cormorant Garamond (licence OFL) et Inter. Icônes : Lucide (licence ISC). Bannière : celle du profil LinkedIn.
