# Examen machine du 21 Mars 2023

## Préambule

Les versions séquentielles des programmes à paralléliser se trouvent avec le dépôt que vous venez de télécharger.

À l'issue de l'examen, vous enverrez les fichiers code source modifiés ainsi qu'un compte-rendu écrit (fichier nommé `README-Nom-Prenom.md`) aux adresses suivantes : 

- xavier.juvigny@onera.fr
- jean-didier.garaud@onera.fr
- augustin.parret-freaud@safrangroup.com


## Introduction

Dans le fichier texte qui accompagne votre travail, répondez aux questions suivantes :

- Quel est le nombre de coeurs physiques de votre machine ?

6

- Quel est le nombre de coeurs logiques de votre machine  ?

12

- Quelle est la quantité de mémoire cache L2 et L3 de votre machine ?

cache L2: 3,0 MB
cache L3: 16,0 MB

## Automate cellulaire 1D

Le but de ce programme est d'étudier un automate cellulaire très simple en **une dimension**. Un automate cellulaire consiste en une grille régulière en une seule dimension
pouvant avoir plusieurs "*états*" (ici seulement *allumée* = 1 et *éteinte* = 0) qui seront modifiés selon l'état des cellules voisines (immédiates ou non) en suivant des règles
fixes à chaque itération.

On considère l'automate le plus simple où une cellule donnée n'est influencée que par les cellules adjacentes. Pour une cellule donnée, il existe donc huit "motifs" différents
(les trois cellules pouvant être éteintes ou allumées, soit huit configurations possibles pour une cellule et son voisinage immédiat), précisément les motifs suivants :

| Motif | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|--- |:-: |:-: |:-: |:-: |:-: |:-: |:-: |:-:

 On veut donc fixer une règle donnant pour chacun de ces motifs si la cellule concernée devient vivante ou morte à la génération suivante. Il y a donc 2**8 = 256 règles possibles
 qu'on pourra représenter par un nombre binaire dont la valeur entière varie entre 0 et 255.

 Par exemple, la règle numéro trente (en binaire 30 = 00011110) sera:

| Motif initial (t)              | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|--- |:-: |:-: |:-: |:-: |:-: |:-: |:-: |:-:
| valeur cellule centrale en t+1 |  0  |  0  |  0  |  1  |  1  |  1  |  1  |  0  |

On veut donc étudier l'influence de ces règles en regardant l'évolution d'une grille de cellule dont au départ toutes sont éteintes sauf une cellule au centre de la grille qui elle sera allumée.

On rajoute de plus une "condition limite" consistant à conserver une cellule à gauche et une cellule à droite qui sera toujours éteinte.

On parcourt ensuite toutes les règles possibles pour générer pour chacune un diagramme "espace-temps" où chaque ligne *i* du diagramme représente un état de la grille au temps *t+i*.

Toujours avec la règle n°30, les trois premières itérations d'évolution de l'automate sont :

| itération | état |
| --------- | ---- |
| 0 (initial) | ⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜ |
| 1           | ⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜ |
| 2           | ⬜⬜⬜⬛⬛⬜⬜⬛⬜⬜⬜ |
| 3           | ⬜⬜⬛⬛⬜⬛⬛⬛⬛⬜⬜ |

Pour chaque diagramme calculé, on créée une image ``resultat_*.png`` représentant le diagramme.

### Parallélisation

1. Paralléliser avec MPI le code afin de pouvoir créer l'ensemble des images illustrant les différents diagrammes suivant chacun une règle différente. Justifier dans votre code votre stratégie de parallélisation (statique contre dynamique, à quel niveau j'ai parallélisé, etc.).

Le choix de la stratégie de parallélisation dépend du problème spécifique à résoudre et des caractéristiques des ressources informatiques utilisées. Dans ce cas, la parallélisation statique est une solution appropriée car le nombre d'automates cellulaires à générer et à afficher est connu avant l'exécution, et les sous-tâches peuvent être réparties de manière équitable entre les cœurs de calcul disponibles. Cela permet une utilisation efficace des ressources disponibles et évite les surcharges potentielles de communication qui peuvent survenir avec la parallélisation dynamique.

En outre, la mise en œuvre de la parallélisation statique dans ce code est relativement simple et facile à comprendre, ce qui peut être un avantage lors du développement et du débogage de programmes parallèles.

2. Créer une courbe donnant l'accélération obtenue avec votre parallélisation (jusqu'à la limite du nombre de coeur physique présent sur votre ordinateur).
![l'accélération](speed-up.png "l'accélération")

**Remarque** : Pour vérifier si les images contiennent des erreurs ou non, on peut vérifier que les fichiers images sont les mêmes qu'avec le code séquentiel en utilisant :

    md5sum -c check_resultats_md.md5sum
ou

    md5sum -c check_resultats_png.md5sum  # si vous avez choisi save_as_png

## Calcul d'une enveloppe convexe

On veut calculer l'enveloppe convexe d'un nuage de point sur le plan. Pour cela on utilise l'algorithme de Graham décrit dans le lien suivant :

    https://fr.wikipedia.org/wiki/Parcours_de_Graham

On obtient en sortie une sous-liste de points du nuage qui définissent l’enveloppe convexe. Ces points sont rangés de manière à parcourir le polygone de l’enveloppe dans le sens direct.

Le code séquentiel peut être trouvé dans le fichier `enveloppe_convexe.py`. En sortie, le code affiche les points et l'enveloppe convexe à l'écran.

Afin de paralléliser le code en distribué avec MPI, on veut distribuer les sommets sur plusieurs processus puis utiliser l’algorithme suivant :

- Calculer l’enveloppe convexe des sommets locaux de chaque processus
- Puis en échangeant deux à deux entre les processus les enveloppes convexes locales, calcul sur chacun la fusion des deux enveloppes convexes en remarquant que
l’enveloppe convexe de deux enveloppe convexe est l’enveloppe convexe de la réunion
des sommets définissant les deux enveloppes convexes.

1. Dans un premier temps, mettre en œuvre l’algorithme sur deux processus.

2. Dans un deuxième temps, en utilisant un algorithme de type hypercube, de sorte qu’un processus fusionne son enveloppe convexe avec le processus se trouvant dans la direction d, mettre en œuvre l’algorithme sur `2**n` processus.

3. Mesurer les speed-ups de votre algorithme en suivant le critère de Amdhal et de Gustafson. Interprétez votre résultat au regard de la complexité de l'algorithme et commentez.


![le critère de Amdhal et de Gustafson.](AG.png "le critère de Amdhal et de Gustafson.")
Les résultats obtenus montrent que l'ajout de coeurs améliore les performances de l'algorithme, mais de manière non linéaire, en accord avec la loi d'Amdhal et de Gustafson.

Selon la loi d'Amdhal, la vitesse d'exécution d'un programme parallèle est limitée par la proportion de code séquentiel dans le programme. Dans notre cas, l'algorithme parallèle a une partie séquentielle (la boucle externe) et une partie parallèle (la boucle interne), donc la vitesse d'exécution sera limitée par la partie séquentielle. En conséquence, le speed-up observé ne sera jamais supérieur au ratio entre la partie parallèle et la totalité du programme.

Dans notre cas, nous avons observé que le speed-up augmente avec le nombre de coeurs, mais à un taux décroissant. Le critère d'Amdhal montre que le speed-up maximum atteint est d'environ 2,3 avec 4 coeurs, ce qui correspond à une amélioration de performance de 2,3 fois par rapport à l'exécution séquentielle. En d'autres termes, l'algorithme parallèle peut s'exécuter environ 2,3 fois plus rapidement que l'algorithme séquentiel avec 4 coeurs.

Cependant, le critère de Gustafson prend également en compte l'évolution de la taille du problème avec le nombre de coeurs. Si la taille du problème augmente avec le nombre de coeurs, alors la partie parallèle augmente également et la vitesse d'exécution s'améliore plus rapidement. Dans notre cas, le critère de Gustafson montre que le speed-up maximum atteint est d'environ 1,8 avec 2 coeurs, ce qui est inférieur à celui observé avec le critère d'Amdhal. Cela peut s'expliquer par le fait que la taille du problème est relativement petite dans notre exemple et donc que la proportion de travail parallélisable reste relativement faible.

En conclusion, l'utilisation d'un algorithme parallèle peut améliorer les performances d'un programme, mais avec une augmentation décroissante du speed-up en fonction du nombre de coeurs utilisés, en accord avec les critères d'Amdhal et de Gustafson. Ces critères permettent d'estimer le speed-up maximal atteignable en fonction de la proportion de code parallélisable et de la taille du problème. Il est donc important de les prendre en compte lors de la conception d'un algorithme parallèle afin de déterminer le nombre optimal de coeurs à utiliser pour une performance maximale.

---

### Exemple sur 8 processus

- Les processus 0 à 7 calculent l’enveloppe convexe de leur nuage de points local.
- Le processus 0 et le processus 1 fusionnent leurs enveloppes, idem pour 2 avec 3, 4 avec 5 et 6 avec 7.
- Le processus 0 et le processus 2 fusionnent leurs enveloppes, idem pour 1 avec 3, 4 avec 6 et 5 avec 7.
- Le processus 0 et le processus 4 fusionnent leurs enveloppes, idem pour 1 avec 5, 2 avec 6 et 3 avec 7.

---
