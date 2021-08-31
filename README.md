# enquetes-snt

![logo](https://www.enquetes-snt.fr/static/enigmes/img/enquetesSNT-white.svg)

Le projet **enquetes-snt** permet aux enseignants de SNT (Sciences Numériques et Technologie) de créer, mutualiser et partager des énigmes à destination de leurs élèves.

Il s'agit d'une application Django développée par Germain Becker, enseignant de Mathématiques, NSI et SNT. Celle-ci est disponible à l'adresse : [enquetes-snt.fr](https://www.enquetes-snt.fr)

Concrètement, chaque enseignant peut se créer un compte sur la plateforme et peut ensuite :

* créer des énigmes qui seront ajoutées à la base commune
* créer ses propres enquêtes à partir d'une ou plusieurs énigmes de la base
* proposer ses enquêtes à ses élèves et récupérer leurs résultats

Ce document est une présentation de l'application.

**Table des matières**

* [Création d'un compte enseignant](#cr%C3%A9ation-dun-compte-enseignant)
* [Énigmes](#%C3%A9nigmes)
    * [Énigmes](#%C3%A9nigmes)
    * [Qu'est-ce qu'une *énigme* ?](#quest-ce-quune-%C3%A9nigme)
    * [Ajout d'une énigme](#ajout-dune-%C3%A9nigme)
* [Enquêtes](#enqu%C3%AAtes)
    * [Qu'est-ce qu'une enquête ?](#quest-ce-quune-enqu%C3%AAte)
    * [Création d'une enquête](#cr%C3%A9ation-dune-enqu%C3%AAte)
    * [Tableau de bord, détails et résultats d'une enquête](#tableau-de-bord-d%C3%A9tails-et-r%C3%A9sultats-dune-enqu%C3%AAte)
* [](#)
* [](#)
* [](#)
* [](#)
* [](#)
* [](#)


<figure>
  <img src="img/accueil.png" alt="une énigme" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Page d'accueil</em></figcaption>
</figure>

## Création d'un compte enseignant

La page d'accueil [enquetes-snt.fr](https://www.enquetes-snt.fr) est à destination des élèves. On y trouve en haut à droite un lien pour accéder à l'espace enseignant où les enseignants peuvent s'identifier.

Pour accéder à l'application, un enseignant devra créer un compte à la première connexion en renseignant :

* un nom et un prénom (seront visibles uniquement des enseignants et permettront de filtrer les recherches d'énigmes par nom d'auteur)
* un nom d'utilisateur
* une adresse email (⚠️ seules les **adresses e-mail académiques** sont acceptées afin de garantir l'accès aux enseignants uniquement).
* un mot de passe évidemment

Chaque enseignant sera ensuite identifié grâce au couple (adresse e-mail, mot de passe).

> Les formats acceptés d'adresse e-mail sont du type _prenom.nom@ac-&lt;academie&gt;.&lt;domaine&gt;_. Pour les cas particuliers, vous pouvez me contacter.

## Énigmes

### Qu'est-ce qu'une *énigme* ?

À l'origine, l'idée était de proposer aux élèves des énigmes nécessitant un travail de recherche de leur part (d'où les termes _énigme_ et _enquête_), afin de valider leurs connaissances et compétences. 

<figure>
  <img src="img/enigme_ex1.png" alt="une énigme" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Une énigme</em></figcaption>
</figure>


Mais tout est possible ! On peut également imaginer des énigmes comme des questions rapides plus classiques.

<figure>
  <img src="img/enigme_ex2.png" alt="une autre énigme" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Une autre énigme</em></figcaption>
</figure>

Libre à vous de vous approprier l'application comme vous le souhaitez, aussi bien dans les énigmes créées que dans l'utilisation avec vos élèves.

> D'autres énigmes sont déjà disponibles dans la base de données, elles pourront vous donner des idées 😀

Chaque énigme devra être associée à l'un des thèmes suivants :

* Internet
* Le Web
* Les réseaux sociaux
* Les données structurées et leur traitement
* Localisation, cartographie, mobilité
* Informatique embarquée et objets connectés
* La photographie numérique
* Python (qui est finalement un thème à part dans l'application)

> Si une énigme s'appuie sur plusieurs de ces thèmes, il faut choisir l'un d'entre eux, le plus cohérent/évident.
> Il est possible de filtrer les énigmes par thème et/ou par auteur.

<figure>
  <img src="img/enigmes.png" alt="Filtrer les énigmes" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 20px 0"><em>Filtrer les énigmes</em></figcaption>
</figure>

**⚠️ Remarques importantes sur les énigmes**

* la réponse à une énigme est **unique** et nécessairement **de type texte**, donc de préférence un **mot unique ou un code** qui devra être **bien orthographié**. 
* Un traitement est néanmoins prévu pour nettoyer les réponses afin de comparer celles saisies par les élèves à celle attendue : passage en minuscules, suppression des accents et des espaces inutiles en début et fin. Ainsi, si la réponse attendue (saisie par l'auteur de l'énigme) est la chaîne de caractères `"Orléans"` et qu'un élève saisit `"orleans "`, sa réponse sera jugée correcte. En revanche, s'il répond `"Orléan"`, elle sera incorrecte.
* les énigmes ne peuvent pas être des questions de type Vrai/Faux, QCM, associations, texte à trous, etc.

### Ajout d'une énigme

Le lien suivant, que vous trouverez également sur la page de création d'une énigme, donne des explications détaillées sur la création d'une énigme : [https://www.enquetes-snt.fr/enigme/creation/exemple/](https://www.enquetes-snt.fr/enigme/creation/exemple/).

Très rapidement, une énigme est composée de 6 champs :

1. Thème (obligatoire) : pour sélectionner le thème de l'énigme (l'un des 8 cités au-dessus)
2. Énoncé (obligatoire) : pour saisir l'énoncé de l'énigme
3. Réponse (obligatoire) : pour saisir la réponse à l'énigme
4. Indication (optionnel) : pour saisir une indication à destination des élèves (l'affichage des indications pourra être activée ou désactivée dans les paramètres d'une enquête)
5. Image d'illustration (optionnel) : pour téléverser une image pour accompagner l'énigme
6. Fichier en pièce jointe (optionnel) : pour téléverser une pièce jointe à l'énigme qui pourra être téléchargée par les élèves

Sachez que les énoncés et indications peuvent être rédigées en **Markdown** ou en **HTML**.

> Même si c'est sans doute moins utile, il est également possible d'utiliser LaTeX (via la bibliothèque MathJax dont le script est téléchargé par le navigateur automatiquement).

## Enquêtes

### Qu'est-ce qu'une *enquête* ?

Une enquête est formée d'au moins une énigme de la base. On peut donc créer des enquêtes plus ou moins longues.

### Création d'une enquête

Il y a deux façons de créer une enquête :

1. en sélectionnant les énigmes souhaitées en parcourant la liste d'énigmes
2. en renseignant directement la liste des numéros des énigmes souhaitées

Une enquête créée est par défaut **active**, c'est-à-dire qu'elle est disponible pour les élèves. Vous pouvez désactiver une enquête, elle ne sera alors plus accessible pour les élèves.

Au moment de la création d'une enquête, il faudra :

* renseigner une **description de l'enquête** (à destination uniquement de l'enseignant). Cette description peut contenir le nom de la classe ou du groupe concerné, le(s) thème(s) de l'enquête, etc. Cette description permettra de mieux vous y retrouver.
* définir les 4 paramètres suivants :
    * choisir si les élèves auront accès aux **indications** (si celles-ci existent pour les énigmes choisies)
    * choisir si une **correction** est proposée aux élèves à la fin de leur enquête
    * choisir si le **score** de l'élève lui est communiqué à la fin de son enquête (en cas de correction activée, le score est automatiquement affiché)
    * choisir si les énigmes de l'enquête sont proposées dans un **ordre aléatoire** aux élèves

Ces quatre paramètres peuvent être modifiés après la création de l'enquête, mais il faudra d'abord _désactiver_ l'enquête, puis la réactiver pour qu'elle soit à nouveau accessible aux élèves.

Les enquêtes ne sont pas partagées avec les autres utilisateurs.

### Tableau de bord

Un tableau de bord permet à chaque enseignant de visualiser en un coup d'oeil toutes les enquêtes qu'il a créées. Ce tableau permet d'accéder au détail de chaque enquête, d'activer ou désactiver une enquête, de connaître le code à communiquer à ses élèves, d'accéder aux résultats des enquêtes, de supprimer une enquête.

<figure>
  <img src="img/tableau_bord.png" alt="Tableau de bord" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;""/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Tableau de bord</em></figcaption>
</figure>

### Détails d'une enquête

La page de détail d'une enquête recense toutes les informations de l'enquête, c'est aussi sur cette page que l'on peut modifier les paramètres de l'enquête, que l'on peut accéder aux résultats des élèves ou les télécharger (au format CSV). On peut également visualiser l'enquête telle qu'elle sera vue par les élèves.

<figure>
  <img src="img/details_enquete.png" alt="Détails d'une enquête" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Détails d'une enquête</em></figcaption>
</figure>

> Il est possible de supprimer une enquête via le tableau de bord ou la page de détails de l'enquête, mais toutes les données de l'enquête seront perdues. ⚠️ Assurez-vous donc d'avoir récupéré les résultats avant la suppression !

### Résultats d'une enquête

La page de résultats d'une enquête permet de voir dans un tableau la réussite des élèves pour l'enquête, énigme par énigme. Il est possible de masquer/afficher les identifiants des élèves, leurs réponses, leurs résultats. Ceci a pour but de pouvoir visualiser en temps réel les résultats, tout en préservant si on le souhaite l'identité des élèves et leurs réponses. Cette page permet également de procéder directement à la correction de l'enquête puisque sous les résultats on retrouve les énigmes et leurs réponses.


<figure>
  <img src="img/resultats_enquete.png" alt="Résultats d'une enquête" style="display:block;margin:auto;border:2px solid #ddd; padding: 10px; border-radius: 10px;"/>
  <figcaption style="text-align:center; margin: 10px 0"><em>Résultats d'une enquête</em></figcaption>
</figure>

### Côté élève

Lors de la création d'une enquête, un code de 8 caractères sera généré ainsi qu'un lien. Les élèves n'auront qu'à saisir ce code sur la page d'accueil pour accéder à l'enquête, ou suivre le lien.

Pour différencier vos différents élèves, un **identifiant** leur sera demandé. C'est à vous de définir les identifiants de vos élèves (un numéro par élève par exemple). Ces identifiants seront stockés dans la base de donnnées et permettront d'associer un résultat à chaque élève pour chaque enquête.


## Mot de l'auteur


