
TD – Imagerie Numérique

![Une image contenant texte

Description générée automatiquement](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.001.png)**Partie 1 – Imagerie couleur**

**Programme python «lecture\_BMP.py» qui permettra de tester votre environnement.**

![Une image contenant texte

Description générée automatiquement](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.002.png)

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.003.png)

**Fonction ouverture\_Fichiers\_Image et Validation de l’entête en y rajoutant les paramètres nécessaires pour que vos fonctions soient réutilisables pour n’importe quel nom de fichier image.**

![Une image contenant texte

Description générée automatiquement](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.004.png)

Pour les données de l’entête, j’ai utilisé une boucle pour afficher toutes les informations contenues dans l’entête.

**Test avec l’image bitmap.bmp » (sur quelques pixels pour simplifier la compréhension), chaque carré est un pixel grossi au maximum. Et de bitmap-300x300.bmp il s’agit d’une image de test de 300 pixels sur 300 pixels**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.005.png)

**Tâche 1 : Afficher la couleur d’un pixel de la matrice de l’image de « lena\_couleur.bmp »** 

![Une image contenant texte

Description générée automatiquement](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.006.png)

Pour afficher la couleur d’un pixel, j’ai d’abord déterminé son indice puis j’ai parcouru la matrice contenant les pixels de l’image.

Quand je trouve l’indice correspondant lors du parcours, je l’affiche.


**Tâche 2 : Agrandir/Rétrécir une image (facteur 2, 4, 8…)**  

Même chose pour le scalage, j’ai multiplié par un facteur.

**Tâche 3 : Rotation de l’image de (90, 180 ou 270°)**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.007.png)

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.008.png)

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.009.png)

Pour la rotation de l’image, j’ai juste trouvé une relation entre une image tournée et une image non tournée puis j’ai changé les indices.



**Bonus : Sortir l’ensemble des données d’une l’entête pour le format png**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.010.png)

**Partie 2– Amélioration de l’image**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.011.png)




**5.1.1 Sauvegarde d’une image à l’identique**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.012.png)

Ici, j’ai juste copié un par un les pixels de l’image original.

**5.1.2 Modifier le contraste d’une image paramétrable**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.013.png)

Pour le contraste, j’ai d’abord considéré le facteur : facteur = (259\*(contrast+255)) / (255\*(259 - contrast)).

‘’contrast’’ est la valeur du contraste (entre -255 et +255) que l’utilisateur doit entrer.

Ensuite, pour chaque pixel de l’image, j’applique la formule :

(facteur\*(pixel - 128) + 128).

**5.1.3 Passage d’une photo couleur à une photo en nuances de gris**
**


![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.014.png)

Pour les nuances de gris, j’ai fait la somme des valeurs RGB d’un pixel puis j’ai divise par 3 afin d’obtenir les nuances : R+G+B/3.
**


**5.1.4 Passage d’une photo couleur à une photo en noir et blanc**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.015.png)

Pour le noir et blanc, j’ai fait la même chose que pour les nuances en gris (j’ai fait R+G+B/3).

La seule différence concerne la normalisation :

- Si ce calcul est inferieur à 128, je ramène à 0
- Sinon, je ramène à 255

**5.1.5 Passage d’une photo couleur à une photo en négatif**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.016.png)

Pour le négatif, pour chaque pixel, j’applique simplement la formule : 255-pixel. Aussi simple que cela.

**5.1.6 Passage d’une photo couleur à une photo en rouge uniquement**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.017.png)

Pour l’image en rouge, je mets simplement la 1ère et la 2eme composante de chaque pixel à 0. (RGB : normalement, c’est la 2ème et la 2ème mais comme on est en little endian c’est l’inverse)



**5.1.7 Passage d’une photo couleur à une photo en vert uniquement**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.018.png)

Pour l’image en verte, je mets simplement la 1ère et la 3ème composante de chaque pixel à 0. 

**5.1.8 Passage d’une photo couleur à une photo en bleu uniquement**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.019.png)

Pour l’image en rouge, je mets simplement la 2ère et la 3ème composante de chaque pixel à 0. (RGB : normalement, c’est la 1ère et la 2ème mais comme on est en little endian c’est l’inverse)

**5.1.9 Passage d’une photo couleur à une photo en 2 couleurs primaires uniquement**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.020.png)

Pour l’image en deux couleurs primaires, je choisis les deux positions (R, G, B) ou il faut mettre la couleur que l’utilisateur entre (entre 0 et 255)

Ensuite, je mets simplement ces deux composantes de chaque pixel à 0. (en tenant compte du fait que on est en little endian).





![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.021.png)**5.1.10 Création d’un histogramme se rapportant à une image (possibilité d’utiliser le module python « matplotlib » uniquement pour l’histogramme)**


**Partie 3 – Segmentation d’image**

![Une image contenant texte

Description générée automatiquement](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.022.png)







![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.023.png)**6.2.1. Détection de contour**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.024.png)**6.2.2. Renforcement des bords**



**6.2.3. Flou**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.025.png)


**6.2.4. Repoussage**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.026.png)

**6.2.4. Colorisation d’une photo en niveau de gris d’une photo NB de Eugène ATGET**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.027.png)

**6.2.5. Innovation**

Pour l’innovation, j’ai mis en place plusieurs filtres et j’ai codé une fonction qui permet de sélectionner une partie de l’image.

**6.4. Vous pourrez utiliser ensuite ces différents filtres pour créer un nouveau modèle de reconnaissance faciale.**

![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.028.png)



















![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.029.png)	











![](Aspose.Words.faf3fad2-c095-436c-8ca6-720007459d73.030.png)

J’ai utilisé le filtre de Sobel pour la reconnaissance de l’image :

D’abord, jai mis l’image en grayscale.
Ensuite, j’ai flouté l’image.

Pour finir, j’ai applique le filtre de Sobel horizontalement et verticalement en sommant les deux composantes. 
Page PAGE2
