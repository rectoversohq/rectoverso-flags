# Drapeaux

Reconnaître un drapeau. Le retrouver à partir du nom d’un lieu.

[English](README.md) · [Périmètre et sources](docs/coverage.md) · [Construction et mises à jour](docs/build.md)

**Candidat local pour revue — non publié.** Aucun téléchargement n’est encore publié.

Une source commune produit **480 cartes en français** et **480 en anglais**, dans deux paquets indépendants. Le référentiel comporte 249 pays et territoires ISO ; seules les questions pertinentes sont incluses. Les exclusions sont documentées, sans drapeau inventé.

Les proportions des drapeaux sont conservées. Les dessins partagés ou similaires reçoivent une précision géographique dans la question. Les champs continent et région facilitent la recherche. Dans Anki, **Explorer** ouvre une courte note après la réponse. La compatibilité native RectoVerso reste une vérification distincte.

## Construire pour Anki

Utiliser Python 3.14 et la version d’Anki fixée dans `requirements.txt`. Aucun compte ni service payant n’est nécessaire. Les PNG suivis dans Git suffisent ; WebKit sur macOS n’est nécessaire que pour les régénérer depuis les SVG.

```sh
python3.14 -m venv /chemin/hors-du-depot/anki-venv
/chemin/hors-du-depot/anki-venv/bin/python -m pip install -r requirements.txt
/chemin/hors-du-depot/anki-venv/bin/python scripts/ci.py --output /chemin/hors-du-depot/premiere-construction
```

La sortie doit être un **nouveau dossier hors du dépôt**. La commande construit chaque langue deux fois, contrôle les identités et le contenu, importe et affiche les deux faces de chaque carte avec le moteur Anki, effectue une vraie réponse, puis vérifie médias et progression après export/réimport.

Importer `packages/Drapeaux-fr-480.apkg` dans Anki. Le paquet anglais s’appelle `Flags-en-480.apkg`. Chacun possède ses propres identités et sa propre progression.

## Modifier et publier

Travailler sur une branche du dépôt du jeu. Modifier les données partagées ou les fichiers de langue, conserver les identités stables et relancer la même commande dans un nouveau dossier. Une revue éditoriale et visuelle native, dans les deux langues et thèmes, reste nécessaire. La réussite de CI n’autorise pas la publication.

Les sources initiales et les corrections sont attribuées dans les données. Les drapeaux inclus sont dans le domaine public ou sous CC0. Les nouvelles créations sont sous CC BY 4.0 ; les licences d’origine des composants sont conservées. Voir [les crédits par fichier](docs/flag-credits.md), [NOTICE](NOTICE.md) et [LICENSE](LICENSE.md).
