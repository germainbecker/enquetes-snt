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
document.querySelector('#id_image').addEventListener("change", function() {
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
    
    var apercuImage = document.querySelector("#image");
    var fichierImage = document.getElementById("id_image");
    var imageTheme = document.querySelector("#image-theme");
    var creditsImageMD = document.getElementById('id_credits_image');
    var apercuCreditsImage = document.querySelector('.apercu-credits-image');
    var urlImage = document.getElementById('id_url_image');

    
    if (fichierImage.value === "" && urlImage.value === "") {
        // on active le choix d'une image
        fichierImage.disabled = false;
        // on active le champ URL
        urlImage.disabled = false;
        // on bloque la saisie de crédits
        bloqueSaisieCredits();
        // on met à jour la source de l'image de l'apercu
        apercuImage.src = "";
        // on n'affiche rien dans l'apercu
        apercuImage.style.display = "none";
        apercuCreditsImage.style.display = "none";

        if (!(theme == "NC")) {  // si le thème est défini (!= NC)
            imageTheme.style.display = "block";  // on affiche l'image du thème par défaut
            imageTheme.data = THEMES[theme];
        } else {  // sinon
            // on n'affiche pas l'image du thème
            imageTheme.style.display = "none";
            imageTheme.data = "none";
        }
    }

    if (!(fichierImage.value === "")){
        // on désactive le champ URL
        urlImage.disabled = true;
        // on autorise la saisie de crédits
        autoriseSaisieCredits();
        // on n'affiche pas l'image du thème
        imageTheme.style.display = "none";
        imageTheme.data = "none";
        // on récupère l'url de l'image à afficher
        let urlFichier = fichierImage.options[fichierImage.selectedIndex].dataset.url;
        // on met à jour la source l'image de l'apercu
        apercuImage.src = urlFichier;
        // on affiche l'image de l'apercu
        apercuImage.style.display = "block";

        // si des crédits sont absents
        if (creditsImageMD.value == "") {
            // on n'affichage pas les crédits dans l'aperçu
            apercuCreditsImage.style.display = "none";
        }
        else {
            // sinon on les affiche
            apercuCreditsImage.style.display = "flex";
            let creditsImageHTML = marked(creditsImageMD.value);  // conversion en HTML
            let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
            let tmp = document.createElement("DIV");
            tmp.innerHTML = creditsImageCleanHTML;
            document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
        }
    }

    if (!(urlImage.value === "")){
        if (isValidHttpUrl(urlImage.value)) {  // si l'url saisie est valide
            // on désactive le champ Image
            fichierImage.disabled = true;
            // on autorise la saisie de crédits
            autoriseSaisieCredits();
            EXIF.getData(urlImage, function() {
                let artiste = EXIF.getTag(this, "Artist");
                let copyright = EXIF.getTag(this, "Copyright");
                majCredits(copyright + " " + artiste);
            });
            // on n'affiche pas l'image du thème
            imageTheme.style.display = "none";
            imageTheme.data = "none";
            // on met à jour la source l'image de l'apercu
            apercuImage.src = urlImage.value;
            // on affiche l'image de l'apercu
            apercuImage.style.display = "block";
            
            // si des crédits sont absents
            if (creditsImageMD.value == "") {
                // on n'affichage pas les crédits dans l'aperçu
                apercuCreditsImage.style.display = "none";
            }
            else {
                // sinon on les affiche
                apercuCreditsImage.style.display = "flex";
                let creditsImageHTML = marked(creditsImageMD.value);  // conversion en HTML
                let creditsImageCleanHTML = DOMPurify.sanitize(creditsImageHTML);
                let tmp = document.createElement("DIV");
                tmp.innerHTML = creditsImageCleanHTML;
                document.querySelector(".credits-image").innerHTML = creditsImageCleanHTML;
            }
        } else {
            // on met à jour la source de l'image de l'apercu
            apercuImage.src = "";
            // on n'affiche rien dans l'apercu
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

function bloqueSaisieCredits() {
    document.getElementById('id_credits_image').disabled = true;
}

function autoriseSaisieCredits() {
    document.getElementById('id_credits_image').disabled = false;
}

function majCredits(texte) {
    if (!(texte == "")){
        document.getElementById('id_credits_image').innerHTML = texte
    }
}


function apercuFichier() {

    // Aperçu fichier joint
    var apercuPj = document.querySelector('.piece-jointe');
    var lienPj = document.querySelector("#nom-fichier");
    var hrefPJ = document.querySelector('#fichier');
    var fichierPj = document.getElementById("id_fichier");
    
    if (fichierPj.value === ""){
        // on n'affiche rien dans l'apercu
        apercuPj.style.display = "none";
        lienPj.href = "";
        lienPj.innerHTML = "";
    } else {
        // on récupère l'URL du fichier
        let urlFichier = fichierPj.options[fichierPj.selectedIndex].dataset.url;
        // on récupère le nom du fichier
        let nomFichier = fichierPj.options[fichierPj.selectedIndex].innerHTML;
        // on met à jour la source (href) du fichier dans l'apercu
        hrefPJ.href = urlFichier;
        lienPj.innerHTML = nomFichier;
        apercuPj.style.display = "flex";
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


window.onload=getExif;
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
