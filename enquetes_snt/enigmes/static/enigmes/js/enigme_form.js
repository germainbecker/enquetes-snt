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

function MathJaxReload() {
    // recharger mathjax
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]); 
}

function apercuEnonce() {
    /* Énoncé */
    let enonceMD = document.getElementById('id_enonce').value;
    let enonceHTML = marked(enonceMD);  // conversion en HTML
    let enonceCleanHTML = DOMPurify.sanitize(enonceHTML);
    document.querySelector(".apercu-enonce").innerHTML = enonceCleanHTML;

    gestionImages();
    gestionLiens();
    gestionTableaux();

    // recharger JS
    Prism.highlightAll(async=true);
}

function apercuIndication() {
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

    gestionImages();
    gestionLiens();
    gestionTableaux();

    // recharger JS
    Prism.highlightAll(async=true);
}

function apercuReponse() {
    /* Réponse */
    let reponseMD = document.getElementById("id_reponse").value;

    if (!(reponseMD == "")) {
        let reponseHTML = marked(reponseMD);  // conversion en HTML
        let reponseCleanHTML = DOMPurify.sanitize(reponseHTML);
        let tmp = document.createElement("DIV");
        tmp.innerHTML = reponseCleanHTML;
        document.querySelector(".reponse").innerHTML = tmp.textContent;
        document.querySelector(".enigme-reponse").style.display = "initial";
    } else {
        document.querySelector(".enigme-reponse").style.display = "none";
    }

    // recharger JS
    Prism.highlightAll(async=true);
}

function conversion() {
    /* Thème choisi */
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
    apercuEnonce();
    apercuIndication(); 
    apercuFichier();
    apercuReponse();
    gestionImages();
    gestionLiens();
    gestionTableaux();
    
    MathJaxReload(); 

    // recharger JS
    Prism.highlightAll(async=true);
}

document.querySelector("#image-theme").style.display = "none";  // ne pas afficher au départ

document.querySelector(".apercu-indication").style.display = "none";  // ne pas afficher au départ

document.querySelector('#btn-apercu').addEventListener("click", conversion);

document.querySelector('#image').style.display = "none";

document.querySelector('.apercu-credits-image').style.display = "none";

document.querySelector('.piece-jointe').style.display = "none";

document.querySelector('.enigme-reponse').style.display = "none";

document.querySelector('#id_theme').addEventListener("change", function() {
    apercuImage(this.value);
});
document.querySelector('#id_enonce').addEventListener("keyup", apercuEnonce);
document.querySelector('#id_enonce').addEventListener("focusout", MathJaxReload);
document.querySelector('#id_reponse').addEventListener("keyup", apercuReponse);
document.querySelector('#id_indication').addEventListener("keyup", apercuIndication);
document.querySelector('#id_indication').addEventListener("focusout", MathJaxReload);
document.querySelector('#id_url_image').addEventListener("keyup", function() {
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
});
document.querySelector('#id_image').addEventListener("load", function() {
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
});
document.querySelector('#id_credits_image').addEventListener("keyup", function() {
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
});



document.querySelector('#id_fichier').addEventListener("change", apercuFichier);

function isValidHttpUrl(string) {
    let url;
    
    try {
      url = new URL(string);
    } catch (_) {
      return false;  
    }
  
    return url.protocol === "http:" || url.protocol === "https:";
}


function apercuImage(theme) {
    // voir https://developer.mozilla.org/fr/docs/Web/API/FileReader/readAsDataURL
    
    // Aperçu image en fonction du thème choisi
    var apercuImage = document.querySelector("#image");
    var fichierImage = document.getElementById("id_image");
    var imageTheme = document.querySelector("#image-theme");
    var imageActuelle = document.getElementById("lien-image");
    var checkBoxImageActuelle = document.getElementById("image-clear_id");
    var creditsImageMD = document.getElementById('id_credits_image').value;
    var apercuCreditsImage = document.querySelector('.apercu-credits-image');
    var urlImage = document.getElementById('id_url_image').value;
    console.log("url", urlImage);
    
    var fichierImageReader = new FileReader();
    fichierImageReader.addEventListener("load", function () {
        if (!(fichierImage.files.length == 0)) {
            apercuImage.src = fichierImageReader.result;
        } else {
            apercuImage.src = '';
        }
      }, false);


    if (!(checkBoxImageActuelle) && urlImage === "") {  // en cas d'une image non présente au départ
        
        console.log("a");
        if (isValidHttpUrl(urlImage)) {  // si l'url saisie est valide
            // on désactive le téléversement d'une image
            document.getElementById('id_image').disabled = true;
            // on met à jour la source de l'image dans l'apercu
            apercuImage.src = urlImage;
            // on l'affiche dans l'aperçu
            apercuImage.style.display = "block";
            // on n'affiche pas l'image du thème
            imageTheme.style.display = "none";
            imageTheme.data = "none";
            // on autorise la saisie des crédits
            autoriseSaisieCredits();
            // si des crédits sont absents
            if (creditsImageMD == "") {
                // on n'affichage pas les crédits dans l'aperçu
                apercuCreditsImage.style.display = "none";
            }
            else {
                // sinon on les affiche
                apercuCreditsImage.style.display = "flex";
                let creditsImageHTML = marked(creditsImageMD);  // conversion en HTML
                let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                console.log(creditsImageCleanHTML);
                let tmp = document.createElement("DIV");
                tmp.innerHTML = creditsImageCleanHTML;
                document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
                console.log("ici");
            }
        } else {
            // on active le téléversement d'une image
            document.getElementById('id_image').disabled = false;
            if (fichierImage.files.length == 1 && fichierImage.files[0]) {  // si une nouvelle image est sélectionnée
                if (/\.(jpe?g|png)$/i.test(fichierImage.files[0].name)) {  // et que son format est accepté                   
                    // on désactive l'ajout d'url
                    document.getElementById('id_url_image').disabled = true;
                    // on lit son contenu
                    fichierImageReader.readAsDataURL(fichierImage.files[0]);  
                    // on l'affiche dans l'aperçu
                    apercuImage.style.display = "block";
                    // on n'affiche pas l'image du thème
                    imageTheme.style.display = "none";
                    imageTheme.data = "none";
                    // on autorise la saisie des crédits
                    autoriseSaisieCredits();
                    // si des crédits sont absents
                    if (creditsImageMD == "") {
                        // on n'affichage pas les crédits dans l'aperçu
                        apercuCreditsImage.style.display = "none";
                    }
                    else {
                        // sinon on les affiche
                        apercuCreditsImage.style.display = "flex";
                        let creditsImageHTML = marked(creditsImageMD);  // conversion en HTML
                        let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                        console.log(creditsImageCleanHTML);
                        let tmp = document.createElement("DIV");
                        tmp.innerHTML = creditsImageCleanHTML;
                        document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
                        console.log("ici");
                    }
                }
            }
            else {  // si pas de nouvelle image sélectionnée
                // on n'affiche rien
                apercuImage.style.display = "none";
                apercuCreditsImage.style.display = "none";
                // on bloque la saisie de crédits
                bloqueSaisieCredits();
                
                if (!(theme == "NC")) {  // si le thème est défini (!= NC)
                        imageTheme.style.display = "block";  // on affiche l'image du thème par défaut
                        imageTheme.data = THEMES[theme];
                } else {  // sinon
                        // on n'affiche pas l'image du thème
                        imageTheme.style.display = "none";
                        imageTheme.data = "none";
                }
            }
        }

        
    } else {  // si une image est présente au départ !
        if (!(urlImage === '')) {   // si une url est définie
            // on désactive la suppression de l'image actuelle et le téléversement d'une nouvelle image
            document.getElementById('id_image').disabled = true;
            if (document.getElementById('image-clear_id')) {
                document.getElementById('image-clear_id').disabled = true;
            }
            // on met à jour la source de l'image dans l'apercu
            apercuImage.src = urlImage;
            // on l'affiche dans l'aperçu
            apercuImage.style.display = "block";
            // on n'affiche pas l'image du thème
            imageTheme.style.display = "none";
            imageTheme.data = "none";
            // on autorise la saisie des crédits
            autoriseSaisieCredits();
            // si des crédits sont absents
            if (creditsImageMD == "") {
                // on n'affichage pas les crédits dans l'aperçu
                apercuCreditsImage.style.display = "none";
            } else {
                // sinon on les affiche
                apercuCreditsImage.style.display = "flex";
                let creditsImageHTML = marked(creditsImageMD);  // conversion en HTML
                let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                console.log(creditsImageCleanHTML);
                let tmp = document.createElement("DIV");
                tmp.innerHTML = creditsImageCleanHTML;
                document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
                console.log("ici");
            }
        } else {  // sinon, si pas d'url définie
            
            // on active la suppression de l'image actuelle et le téléversement d'une nouvelle image
            document.getElementById('id_image').disabled = false;
            document.getElementById('image-clear_id').disabled = false;
            
            if (fichierImage.files.length == 1 && fichierImage.files[0]) { // si une nouvelle image est sélectionnée
                if (/\.(jpe?g|png)$/i.test(fichierImage.files[0].name)) {  // si son format est OK
                    // on désactive l'ajout d'url
                    document.getElementById('id_url_image').disabled = true;
                    // on désactive la case à cocher de suppression
                    document.getElementById('image-clear_id').disabled = true;
                    
                    // on lit son contenu
                    fichierImageReader.readAsDataURL(fichierImage.files[0]);
                    // on l'affiche dans l'aperçu
                    apercuImage.style.display = "block";
                    // on n'affiche pas l'image du thème
                    imageTheme.style.display = "none";
                    imageTheme.data = "none";
                    // on autorise la saisie des crédits
                    autoriseSaisieCredits();
                    // si des crédits sont absents
                    if (creditsImageMD == "") {
                        // on n'affichage pas les crédits dans l'aperçu
                        apercuCreditsImage.style.display = "none";
                    } else {
                        // sinon on les affiche
                        apercuCreditsImage.style.display = "flex";
                        let creditsImageHTML = marked(creditsImageMD);  // conversion en HTML
                        let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                        console.log(creditsImageCleanHTML);
                        let tmp = document.createElement("DIV");
                        tmp.innerHTML = creditsImageCleanHTML;
                        document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
                        console.log("ici");
                    }
                }
            } else {  // si pas de nouvelle image sélectionnée, on regarde si la checkbox est cochée ou pas
                if (!(checkBoxImageActuelle.checked)){  // si l'image n'est pas à supprimer
                    // on désactive l'ajout d'url
                    document.getElementById('id_url_image').disabled = true;
                    // on récupère son URL
                    var urlImage = imageActuelle.href;
                    // on l'utilise pour l'apercu
                    apercuImage.src = urlImage;
                    apercuImage.style.display = "block";
                    // on n'affiche pas l'image du thème
                    imageTheme.style.display = "none";
                    imageTheme.data = "none";
                    // on autorise la modif des crédits
                    autoriseSaisieCredits();
                    // si des crédits sont absents
                    if (creditsImageMD == "") {
                        // on n'affichage pas les crédits dans l'aperçu
                        apercuCreditsImage.style.display = "none";
                    } else {
                        // sinon on les affiche
                        apercuCreditsImage.style.display = "flex";
                        let creditsImageHTML = marked(creditsImageMD);  // conversion en HTML
                        let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                        console.log(creditsImageCleanHTML);
                        let tmp = document.createElement("DIV");
                        tmp.innerHTML = creditsImageCleanHTML;
                        document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
                        console.log("ici");
                    }
                } else {  // si l'image actuelle est à supprimer
                    // on active l'ajout d'url
                    document.getElementById('id_url_image').disabled = false;
                    // on desactive l'ajout d'une image
                    document.querySelector('#id_image').disabled = true;

                    // on n'affiche rien
                    apercuImage.style.display = "none";
                    apercuCreditsImage.style.display = "none";
                    // on bloque la saisie de crédits
                    bloqueSaisieCredits();
                    if (!(theme == "NC")) {  // si le thème est défini (!= NC)
                        imageTheme.style.display = "block";  // on affiche l'image du thème par défaut
                        imageTheme.data = THEMES[theme];
                    } else {  // sinon
                        // on n'affiche pas l'image du thème
                        imageTheme.style.display = "none";
                        imageTheme.data = "none";
                    }
                }
    
            }
        }

        
    }
}

function bloqueSaisieCredits() {
    document.getElementById('id_credits_image').disabled = true;
    console.log("bloque");
}

function autoriseSaisieCredits() {
    document.getElementById('id_credits_image').disabled = false;
    console.log("ok");
}

function apercuFichier() {

    // Aperçu fichier joint
    var apercuPj = document.querySelector('.piece-jointe');
    var lienPj = document.querySelector("#nom-fichier");
    var hrefPJ = document.querySelector('#fichier');
    var fichierPj = document.getElementById("id_fichier");
    var fichierPjReader = new FileReader();
    fichierPjReader.addEventListener("load", function () {
        hrefPJ.href = fichierPjReader.result;
      }, false);
    
    if (fichierPj.files.length == 1 && fichierPj.files[0]) {
        if (/\.(csv|xls|xlsx|ods|py|html|css|txt|jpg|jpeg|png|json)$/i.test(fichierPj.files[0].name)) {
            fichierPjReader.readAsDataURL(fichierPj.files[0]);
            apercuPj.style.display = "flex";
            lienPj.innerHTML = fichierPj.files[0].name;
            hrefPJ.download = fichierPj.files[0].name;
        }
    } else {
        var fichierActuel = document.getElementById("lien-fichier");
        var checkBoxFichierActuel = document.getElementById("fichier-clear_id");
        if (fichierActuel && checkBoxFichierActuel.checked == false) {  // si le fichier actuel existe et n'est pas à supprimer
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
    let theme = document.querySelector('#id_theme').value;

    const extensionsAcceptees =  ['jpeg','jpg','png'],
            tailleMax = 1024*300; // 300 Kio

    // si un fichier image a été choisi
    if (this.files.length == 1 && this.files[0]) {
        
        // récupération du nom et de la taille à partir de l'objet fichier
        const {name: nomFichier, size: tailleFichier} = this.files[0];

        // récupération de l'extension de l'image
        const extensionFichier = nomFichier.split(".").pop();

        // vérification de l'extension et de la taille de l'image
        if (!extensionsAcceptees.includes(extensionFichier)){
            alert("Extension non acceptée. Seules les images aux formats .jpg ou .png sont acceptées.");
            this.value = null;            
            apercuImage(theme);
            return false;
        } else if (tailleFichier > tailleMax){
            alert("Fichier trop volumineux. Assurez-vous que l'image ait une taille inférieure à 300 Kio.")
            this.value = null;
            apercuImage(theme);
            return false;
        } else {            
            btnResetImage.style.display = "flex";
            apercuImage(theme);
            return true;
        }
    } else {
        this.value = "";
        btnResetImage.style.display = "none";
        apercuImage(theme);
        return false;
    }
    
}

// Pièce jointe

document.getElementById("id_fichier").addEventListener("change", validationPieceJointe);

function validationPieceJointe(){

    let btnResetFichier = document.querySelector('#reset-fichier');
    const extensionsAcceptees =  ['csv', 'xls', 'ods', 'xlsx' ,'py', 'html', 'css', 'txt', 'jpeg', 'jpg', 'png', 'json'],
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
            this.value = '';
            apercuFichier();
            return false;
        } else {
            btnResetFichier.style.display = "flex";
            apercuFichier();
            return true;
        }
    } else {
        btnResetFichier.style.display = "none";
        apercuFichier();
        return true;
    }  
}

// Suppression de l'image sélectionnée

let btnResetImage = document.querySelector('#reset-image');
btnResetImage.addEventListener('click', resetImage);

function resetImage() {
    var fichierImage = document.getElementById("id_image");
    fichierImage.value = null;
    btnResetImage.style.display = "none";
    
    // on active l'ajout d'url
    document.getElementById('id_url_image').disabled = false;

    // actualisation apercu
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
}

// Suppression de l'image sélectionné dans le cas d'une modification d'une énigme

if (document.getElementById("image-clear_id")) {
    var checkBoxImageActuelle = document.getElementById("image-clear_id");
    checkBoxImageActuelle.addEventListener("click", () => {
        // actualisation apercu
        let theme = document.querySelector('#id_theme').value;
        apercuImage(theme);
    });
    
}

// Suppression du fichier sélectionné

let btnResestFichier = document.querySelector('#reset-fichier');
btnResestFichier.addEventListener("click", resetFichier);

function resetFichier() {
    var fichier = document.getElementById("id_fichier");
    fichier.value = null;
    btnResestFichier.style.display = "none";
    
    // actualisation apercu
    let theme = document.querySelector('#id_theme').value;
    apercuFichier(theme);
}

// Suppression du fichier sélectionné dans le cas d'une modification d'une énigme

if (document.getElementById("fichier-clear_id")) {
    var checkBoxFichierActuel = document.getElementById("fichier-clear_id");
    checkBoxFichierActuel.addEventListener("click", () => {
        // actualisation apercu
        apercuFichier();
    });
    
}


// Gestion saisie crédits image d'illustration





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


/* Pour afficher l'aperçu directement */
let theme = document.querySelector('#id_theme').value;
apercuImage(theme);
apercuEnonce();
apercuIndication(); 
apercuFichier();
apercuReponse();
gestionImages();
gestionLiens();
gestionTableaux();