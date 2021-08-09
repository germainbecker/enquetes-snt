// A SUPPRIMER

// redimensionnement des images d'une énigme
const DIM_MAX = 760;

var contenu = document.querySelector('.enigme');
contenu.querySelectorAll('img:not(.dim-fixe').forEach(item => {
    // APRÈS chargement
    item.addEventListener("load", function() {
        
        // redimensionnement
        var largeur = item.clientWidth;
        var hauteur = item.clientHeight;
        if (largeur > DIM_MAX || hauteur > DIM_MAX) {
            if (largeur < hauteur) {
                this.style.height = DIM_MAX.toString()+"px";
            } else {
                this.style.width = DIM_MAX.toString()+"px";
            }
        }

        // ajout classes
        item.classList.add("centre", "image-responsive"); 
      });
});