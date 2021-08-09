var enigmesContainers = document.querySelectorAll(".enigme-container");

// Ajout des classes aux images
enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('img:not(.dim-fixe)').forEach(image => {
        image.classList.add("centre", "image-responsive", "agrandir");
    });
});

// Ajout target="_blank" à tous les liens d'une énigme (pour ne pas quitter une enquête)
enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('a:not(.lien-detail):not(.btn-modif)').forEach(lien => {
        lien.setAttribute("target", "_blank");
    });
});

// Ajout de la classe tbl à tous les tableaux
enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('table').forEach(tableau => {
        tableau.classList.add("tbl");
    });
});


// Modale (source : https://youtu.be/2R525oEOl2s)

window.onload = () => {
    const modale = document.querySelector("#modale");
    const close = document.querySelector(".close");
    const images = document.querySelectorAll("img.agrandir");
    
    // On ajoute l'écouteur click sur les images
    for(let image of images){
        image.addEventListener("click", function(e){

            // On ajoute l'image du lien cliqué dans la modale
            const image_agrandie = modale.querySelector(".modal-content img");
            image_agrandie.src = this.src;

            // On affiche la modale
            modale.classList.add("show");
            document.querySelector("body").style.overflow = 'hidden'; // empêche le scroll en arrière-plan
        });
    }
    
    // On active le bouton close
    close.addEventListener("click", function(){
        modale.classList.remove("show");
        document.querySelector("body").style.overflow = 'visible'; // réactive le scroll
    });

    // On ferme au clic sur la modale
    modale.addEventListener("click", function(){
        modale.classList.remove("show");
        document.querySelector("body").style.overflow = 'visible'; // réactive le scroll
    });
}

/* window.onload = () => {
    const modale = document.querySelector("#modale");
    const close = document.querySelector(".close");
    const links = document.querySelectorAll("#liste-enigmes a.agrandir");
    
    // On ajoute l'écouteur click sur les liens
    for(let link of links){
        link.addEventListener("click", function(e){
            // On désactive le comportement des liens
            e.preventDefault();

            // On ajoute l'image du lien cliqué dans la modale
            const image = modale.querySelector(".modal-content img");
            image.src = this.href;

            // On affiche la modale
            modale.classList.add("show");
            document.querySelector("body").style.overflow = 'hidden'; // empêche le scroll en arrière-plan
        });
    }
    
    // On active le bouton close
    close.addEventListener("click", function(){
        modale.classList.remove("show");
        document.querySelector("body").style.overflow = 'visible'; // réactive le scroll
    });

    // On ferme au clic sur la modale
    modale.addEventListener("click", function(){
        modale.classList.remove("show");
        document.querySelector("body").style.overflow = 'visible'; // réactive le scroll
    });
} */


/* window.onload = () => {
    
    // pour chaque image à redimensionner
    contenu.querySelectorAll('img:not(.dim-fixe):not(.centre)').forEach(item => {
        
        // on affiche une image avec dimensions maximales si nécessaire
        var largeur = item.clientWidth;
        var hauteur = item.clientHeight;
        if (largeur > DIM_MAX || hauteur > DIM_MAX) {
            if (largeur < hauteur) {
                item.style.height = DIM_MAX.toString()+"px";
            } else {
                item.style.width = DIM_MAX.toString()+"px";
            }
        }

        // on centre les images et on les rend responsive
        item.classList.add("centre", "image-responsive"); 
        });
} */

/* function redimensionnementImages() {
    console.log('fonction');
    var contenu = document.querySelector('#liste-enigmes');
    contenu.querySelectorAll('img:not(.dim-fixe)').forEach(item => {
        // APRÈS chargement
        console.log(item);
            
        // redimensionnement
        var largeur = item.clientWidth;
        var hauteur = item.clientHeight;
        if (largeur > DIM_MAX || hauteur > DIM_MAX) {
            if (largeur < hauteur) {
                item.style.height = DIM_MAX.toString()+"px";
            } else {
                item.style.width = DIM_MAX.toString()+"px";
            }
        }

        // ajout classes
        item.classList.add("centre", "image-responsive"); 
    });
} */