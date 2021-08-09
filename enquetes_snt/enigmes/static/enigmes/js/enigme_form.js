function conversion() {
    /* Image */
    /* let imageURL = document.getElementById('id_image').value;
    if (!(imageURL == "")) {
        imageCodeHTML = "<img class=\"centre image-responsive\" src=\"" + imageURL + "\" alt=\"image illustration\">"
        document.querySelector(".apercu-image").innerHTML = imageCodeHTML;
        document.querySelector(".apercu-image").style.display = 'inline';    
    } else {
        document.querySelector(".apercu-image").style.display = "none";
    } */


    /* Énoncé */
    let enonceMD = document.getElementById('id_enonce').value;
    let enonceHTML = marked(enonceMD);  // conversion en HTML
    let enonceCleanHTML = DOMPurify.sanitize(enonceHTML);
    document.querySelector(".apercu-enonce").innerHTML = enonceCleanHTML;
    
    /* Indication */
    let indicationMD = document.getElementById('id_indication').value;
    if (!(indicationMD == "")) {
        let indicationHTML = marked(indicationMD);  // conversion en HTML
        let indicationCleanHTML = DOMPurify.sanitize(indicationHTML);
        document.querySelector(".texte-indication").innerHTML = indicationCleanHTML;
        document.querySelector(".apercu-indication").style.display = 'flex';
    } else {
        document.querySelector(".apercu-indication").style.display = "none";
    }

    apercuFichiers();
    gestionImages();
    gestionLiens();
    gestionTableaux();
    //redimensionnementImage();
    
    /* Réponse */
    let reponseMD = document.getElementById("id_reponse").value;

    if (!(reponseMD == "")) {
        let reponseHTML = marked(reponseMD);  // conversion en HTML
        let reponseCleanHTML = DOMPurify.sanitize(reponseHTML);
        document.querySelector(".reponse").innerHTML = reponseCleanHTML;
        document.querySelector(".enigme-reponse").style.display = "initial";
    } else {
        document.querySelector(".enigme-reponse").style.display = "none";
    }

    //rechargeCSS();

    // recharger mathjax
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]); 

    // recharger JS
    //reload_prism();
    Prism.highlightAll(async=true);
}



document.querySelector(".apercu-indication").style.display = "none";  // ne pas afficher au départ

document.querySelector('#btn-apercu').addEventListener("click", conversion);

document.querySelector('#image').style.display = "none";

document.querySelector('.piece-jointe').style.display = "none";

document.querySelector('.enigme-reponse').style.display = "none";

function apercuFichiers() {
    // voir https://developer.mozilla.org/fr/docs/Web/API/FileReader/readAsDataURL
    // Aperçu image
    var apercuImage = document.querySelector("#image");
    var fichierImage = document.getElementById("id_image");
    var fichierImageReader = new FileReader();
    fichierImageReader.addEventListener("load", function () {
        apercuImage.src = fichierImageReader.result;
      }, false);
    
    if (fichierImage.files.length == 1 && fichierImage.files[0]) {  // si une nouvelle image est sélectionnée
        if (/\.(jpe?g|png)$/i.test(fichierImage.files[0].name)) {
            fichierImageReader.readAsDataURL(fichierImage.files[0]);
            apercuImage.style.display = "block";
        }
    } else {
        var imageActuelle = document.getElementById("lien-image");
        var checkBoxImageActuelle = document.getElementById("image-clear_id");
        if (imageActuelle && checkBoxImageActuelle.checked == false) {  // si l'image actuelle existe et n'est pas à supprimer
            var urlImage = imageActuelle.href;  // on l'utilise pour l'apercu
            apercuImage.src = urlImage;
            apercuImage.style.display = "block"; 
        } else {
            apercuImage.style.display = "none";
        }
    }

    // Aperçu fichier joint
    var apercuPj = document.querySelector('.piece-jointe');
    var lienPj = document.querySelector("#nom-fichier");
    var fichierPj = document.getElementById("id_fichier");
    var fichierPjReader = new FileReader();
    fichierPjReader.addEventListener("load", function () {
        lienPj.href = fichierPjReader.result;
      }, false);
    
    console.log(fichierPj.files.length);
    if (fichierPj.files.length == 1 && fichierPj.files[0]) {
        if (/\.(csv|xls|ods|py|html|css)$/i.test(fichierPj.files[0].name)) {
            fichierPjReader.readAsDataURL(fichierPj.files[0]);
            apercuPj.style.display = "flex";
            lienPj.innerHTML = fichierPj.files[0].name;
        }
    } else {
        var fichierActuel = document.getElementById("lien-fichier");
        var checkBoxFichierActuel = document.getElementById("fichier-clear_id");
        if (fichierActuel && checkBoxFichierActuel.checked == false) {  // si l'image actuelle existe et n'est pas à supprimer
            // on l'utilise pour l'apercu
            lienPj.href = fichierActuel.href;
            lienPj.innerHTML = fichierActuel.innerHTML;
            apercuPj.style.display = "flex"; 
        } else {
            apercuPj.style.display = "none";
        }

    }
}

function redimensionnementImage() {
    var image = document.querySelector("#image");
    image.addEventListener("load", function() {
        
        // redimensionnement
        var largeur = image.clientWidth;
        var hauteur = image.clientHeight;
        if (largeur > 500 || hauteur > 500) {
            if (largeur < hauteur) {
                this.style.height = "500px";
            } else {
                this.style.width = "500px";
            }
        }

        // ajout classes
        image.classList.add("centre", "image-responsive"); 
      });
}

/* function reload_prism(){
    var js_section = document.querySelector('.js-files');
    var script= document.createElement('script');
    script.src= "/static/enigmes/js/prism.js";
    js_section.appendChild(script);
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('pre code').forEach((el) => {
      hljs.highlightElement(el);
    });
  }); */



var enigmeContainer = document.querySelector(".apercu");

// Ajout des classes aux images
function gestionImages() {
    enigmeContainer.querySelectorAll('img:not(.dim-fixe)').forEach(image => {
        image.classList.add("centre", "image-responsive", "agrandir");
    });
    // instructions pour la modale qui doivent être rappelées
    const modale = document.querySelector("#modale");
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
    
    
}


/* enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('img:not(.dim-fixe)').forEach(image => {
        image.classList.add("centre", "image-responsive", "agrandir");
    });
}); */

// Ajout target="_blank" à tous les liens d'une énigme (pour ne pas quitter une enquête)
function gestionLiens() {
    enigmeContainer.querySelectorAll('a:not(.lien-detail)').forEach(lien => {
        lien.setAttribute("target", "_blank");
    });
}

/* enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('a:not(.lien-detail)').forEach(lien => {
        lien.setAttribute("target", "_blank");
    });
}); */

// Ajout de la classe tbl à tous les tableaux
function gestionTableaux() {
    enigmeContainer.querySelectorAll('table').forEach(tableau => {
        tableau.classList.add("tbl");
    });
}

/* enigmesContainers.forEach(enigmeContainer => {
    enigmeContainer.querySelectorAll('table').forEach(tableau => {
        tableau.classList.add("tbl");
    });
}); */
