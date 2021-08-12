var THEMES = {  // ne doit pas être modifié !!!!
    'INT': "/static/enigmes/img/theme-int.svg",
    'WEB': "/static/enigmes/img/theme-web.svg",
    'RS': "/static/enigmes/img/theme-rs.svg",
    'DATA': "/static/enigmes/img/theme-data.svg",
    'LCM': "/static/enigmes/img/theme-lcm.svg",
    'IEOC': "/static/enigmes/img/theme-ieoc.svg",
    'IMG': "/static/enigmes/img/theme-img.svg",
    'PY': "/static/enigmes/img/python-logo.svg"
}

function conversion() {

    /* Thème choisi */
    let theme = document.querySelector('#id_theme').value;

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

    apercuFichiers(theme);
    gestionImages();
    gestionLiens();
    gestionTableaux();
    
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

    // recharger mathjax
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]); 

    // recharger JS
    Prism.highlightAll(async=true);
}

document.querySelector("#image-theme").style.display = "none";  // ne pas afficher au départ

document.querySelector(".apercu-indication").style.display = "none";  // ne pas afficher au départ

document.querySelector('#btn-apercu').addEventListener("click", conversion);

document.querySelector('#image').style.display = "none";

document.querySelector('.piece-jointe').style.display = "none";

document.querySelector('.enigme-reponse').style.display = "none";

function apercuFichiers(theme) {
    // voir https://developer.mozilla.org/fr/docs/Web/API/FileReader/readAsDataURL
    
    // Aperçu image en fonction du thème choisi
    var apercuImage = document.querySelector("#image");
    var fichierImage = document.getElementById("id_image");
    var imageTheme = document.querySelector("#image-theme");
    var imageActuelle = document.getElementById("lien-image");
    var checkBoxImageActuelle = document.getElementById("image-clear_id");
    
    if (!(checkBoxImageActuelle)) {  // en cas d'une image non présente
        if (!(theme == "NC")) {
            if (fichierImage.files.length == 0){
                imageTheme.style.display = "block";  // on affiche l'image du thème par défaut
                imageTheme.data = THEMES[theme];
            } else {
                imageTheme.style.display = "none";
                imageTheme.data = "none";
            }
        } else {
            imageTheme.style.display = "none";
            imageTheme.data = "none";
        }
    } else {  // modification en cas d'une image déjà présente
        if (!(theme == "NC")) {
            if (fichierImage.files.length == 0 && Boolean(imageActuelle) && checkBoxImageActuelle.checked){
                imageTheme.style.display = "block";  // on affiche l'image du thème par défaut
                imageTheme.data = THEMES[theme];
            } else {
                imageTheme.style.display = "none";
                imageTheme.data = "none";
            }
        } else {
            imageTheme.style.display = "none";
            imageTheme.data = "none";
        }
    }

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
    
    if (fichierPj.files.length == 1 && fichierPj.files[0]) {
        if (/\.(csv|xls|xlsx|ods|py|html|css|jpg|jpeg|png|json)$/i.test(fichierPj.files[0].name)) {
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


// Ajout target="_blank" à tous les liens d'une énigme (pour ne pas quitter une enquête)
function gestionLiens() {
    enigmeContainer.querySelectorAll('a:not(.lien-detail)').forEach(lien => {
        lien.setAttribute("target", "_blank");
    });
}


// Ajout de la classe tbl à tous les tableaux
function gestionTableaux() {
    enigmeContainer.querySelectorAll('table').forEach(tableau => {
        tableau.classList.add("tbl");
    });
}

// VALIDATION DES FICHIERS A TELEVERSER

// Image

document.getElementById("id_image").addEventListener("change", validationImage);

function validationImage(){
    let btnResetImage = document.querySelector('#reset-image');

    const extensionsAcceptees =  ['jpeg','jpg','png'],
            tailleMax = 1024*300; // 300 Kio

    // si un fichier image a été choisi
    if (this.files.length == 1 && this.files[0]) {
        
        // récupération du nom et de la taille à partir de l'objet fichier
        const {name: nomFichier, size: tailleFichier} = this.files[0];

        // récupération de l'extension de l'image
        const extensionFichier = nomFichier.split(".").pop();

        // vérification de l'extension et de la taille de l'image
        if(!extensionsAcceptees.includes(extensionFichier)){
            alert("Extension non acceptée. Seules les images aux formats .jpg ou .png sont acceptées.");
            this.value = null;
            return false;
        }else if(tailleFichier > tailleMax){
            alert("Fichier trop volumineux. Assurez-vous que l'image ait une taille inférieure à 300 Kio.")
            this.value = null;
            return false;
        } else {            
            btnResetImage.style.display = "flex";
            return true;
        }
    } else {
        btnResetImage.style.display = "none";
        return false;
    }
    
}

// Pièce jointe

document.getElementById("id_fichier").addEventListener("change", validationPieceJointe);

function validationPieceJointe(){

    let btnResetFichier = document.querySelector('#reset-fichier');

    const extensionsAcceptees =  ['csv','xls','ods','py','html','css','jpeg','jpg','png'],
            tailleMax = 1024 * 1000; // 1 Mio

    // si un fichier a été choisi
    if (this.files.length == 1 && this.files[0]) {
        
        // récupération du nom et de la taille à partir de l'objet fichier
        const { name:nomFichier, size:tailleFichier } = this.files[0];
        
        // récupération de l'extension du fichier
        const extensionFichier = nomFichier.split(".").pop();

        // vérification de l'extension et de la taille du fichier
        if (!extensionsAcceptees.includes(extensionFichier)){
            alert("Extension non acceptée. Seuls les fichiers aux formats .csv, .ods, .xls, .xlsx, .py, .html, .css, .jpg, .png et .json sont acceptés.");
            this.value = null;
            return false;
        } else if (tailleFichier > tailleMax){
            alert("Fichier trop volumineux. Assurez-vous que le fichier joint ait une taille inférieure à 1 Mio.")
            this.value = null;
            return false;
        } else {
            btnResetFichier.style.display = "flex";
            return true;
        }
    } else {
        btnResetFichier.style.display = "none";
        return true;
    }  
}

// Suppression de l'image sélectionnée

let btnResetImage = document.querySelector('#reset-image');
btnResetImage.addEventListener('click', resetImage);

function resetImage() {
    var fichierImage = document.getElementById("id_image");
    fichierImage.value = '';
    btnResetImage.style.display = "none";
}



// Suppression du fichier sélectionné

let btnResestFichier = document.querySelector('#reset-fichier');
btnResestFichier.addEventListener("click", resetFichier);

function resetFichier() {
    var fichier = document.getElementById("id_fichier");
    fichier.value = '';
    btnResestFichier.style.display = "none";
}

// VALIDATION FORMULAIRE (le thème ne doit pas être NC)

document.querySelector("form").addEventListener("submit", function(event) {
    let theme = document.querySelector('#id_theme').value;
    let selectTheme = document.querySelector("#id_theme");
    if (theme === "NC") {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth" 
        });
        
        selectTheme.style.border = "1px solid red";
        alert("Veuillez sélectionner un thème. Si une énigme s'appuie sur plusieurs d'entre eux, choisissez celui qui vous semble le plus cohérent.");
        event.preventDefault();
        return false;
    } else {
        selectTheme.style.border = "inherit";
        return true;
    }
});
