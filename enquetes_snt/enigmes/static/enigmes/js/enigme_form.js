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

function apercuCommentaire() {
    let commentaireMD = document.getElementById('id_commentaires').value;
    if (!(commentaireMD == "")) {
        let commentaireHTML = marked(commentaireMD);  // conversion en HTML
        let commentaireCleanHTML = DOMPurify.sanitize(commentaireHTML);
        document.querySelector(".apercu-commentaire").innerHTML = commentaireCleanHTML;
        document.querySelector("#apercu-para-commentaires").style.display = 'block';
    } else {
        document.querySelector("#apercu-para-commentaires").style.display = "none";
    }

    gestionImages();
    gestionLiens();
    gestionTableaux();

    // recharger JS
    Prism.highlightAll(async=true);
}

function reponsesPresentes(tableauReponsesMD) {
    let reponsePresente = false;
    for (reponse of tableauReponsesMD) {
        if (!(reponse == '')) {
            reponsePresente = true;
        }
    }
    return reponsePresente;
}

function apercuReponse() {
    let reponseEnigmeContainer = document.getElementById('reponse-enigme-container');
    let reponseLibreContainer = document.getElementById('reponse-libre-container');
    // si réponse libre attendue
    if (caseQuestionLibre.checked) {
        document.getElementById('warning-reponse-libre').style.display = "inline-block";
        reponseEnigmeContainer.classList.add('hidden');
        reponseLibreContainer.classList.remove('hidden');
        let reponseLibreMD = document.querySelector('#id_reponse_libre').value;
        if (!(reponseLibreMD === '')) {
            let reponseLibreHTML = marked(reponseLibreMD);  // conversion en HTML
            let reponseLibreCleanHTML = DOMPurify.sanitize(reponseLibreHTML);
            document.querySelector('#reponse-libre').innerHTML = reponseLibreCleanHTML;
            document.querySelector(".enigme-reponse").style.display = "initial";
        } else {            
            document.querySelector(".enigme-reponse").style.display = "none";
        }
    } // sinon s'il s'agit d'une énigme classique 
    else {
        document.getElementById('warning-reponse-libre').style.display = "none";
        reponseEnigmeContainer.classList.remove('hidden');
        reponseLibreContainer.classList.add('hidden');
        if (nbReponsesAffichees == 4) {
            boutonAjouterReponse.classList.add('hidden');
        }
    
        let reponsePrincipale = document.querySelector('#id_reponse').value;
        
        if (reponsePrincipale === '') {
            boutonAjouterReponse.classList.add('hidden');
            champsReponsesOptionnelles.forEach(champ => {
                champ.disabled = true;
            })
        } else {
            champsReponsesOptionnelles.forEach(champ => {
                champ.disabled = false;
            })
            if (nbReponsesAffichees === 4) {
                boutonAjouterReponse.classList.add('hidden');
            } else {
                boutonAjouterReponse.classList.remove('hidden');
            }
        }
    
        /* Réponse */
        let listeChampsReponse = document.querySelectorAll('input[type=text][id*=id_reponse]');
        let tableauReponsesMD = [];
        for (let champ of listeChampsReponse) {
            tableauReponsesMD.push(champ.value)
        }
    
        reponsePresente = reponsesPresentes(tableauReponsesMD);
        
        if (reponsePresente) {
            let tableauReponsesHTML = tableauReponsesMD.map(reponseMD => marked(reponseMD));
                let tableauReponseCleanHTML = tableauReponsesHTML.map(reponseHTML => DOMPurify.sanitize(reponseHTML));
            if (tableauReponseCleanHTML[0] === '') {
                document.querySelector(".enigme-reponse").style.display = "none";
            } else {
                
                let tableauReponses = tableauReponseCleanHTML.filter(x => x !== '');
                const nbReponses = tableauReponses.length;
                let tmp = document.createElement("DIV");
                let reponse = document.querySelector(".reponse-affichee");
                let autresReponses = document.querySelector("#autres-reponses");
                let autresReponsesAffichees = document.querySelector(".autres-reponses-affichees");
                
                tmp.innerHTML = tableauReponses[0];
                reponse.innerHTML = tmp.textContent;
                if (nbReponses === 1) {
                    autresReponses.classList.add('hidden');
                }
                else {
                    tableauReponses.shift() // enlève le premier élément du tableau
                    tableauReponses = tableauReponses.map(x => x.replace('\n', ''));
                    let reponses = tableauReponses.join(', ');
                    tmp.innerHTML = reponses;
                    autresReponsesAffichees.innerHTML = tmp.textContent;
                    autresReponses.classList.remove('hidden');
                }
        
                document.querySelector(".enigme-reponse").style.display = "initial";
            }
        } else {
            document.querySelector(".enigme-reponse").style.display = "none";
        }
    }

    
    apercuCommentaire();
    // recharger JS
    Prism.highlightAll(async=true);
}


let caseQuestionLibre = document.getElementById('id_question_libre');
caseQuestionLibre.addEventListener('change', gestionQuestionLibre);

function gestionQuestionLibre() {
    apercuReponse();
    gestionReponsesOptionnelles();
    let paraReponses = document.getElementById('para-reponse');
    /* let paraReponsesOptionnelles = document.querySelectorAll('.champ-reponse'); */
    let paraReponseLibre = document.getElementById('para-reponse-libre');
    let divBoutonAjouterReponse = document.querySelector('.btn-ajout-reponse');
    if (caseQuestionLibre.checked) {
        paraReponses.classList.add('hidden');
        paraReponseLibre.classList.remove('hidden')
        divBoutonAjouterReponse.classList.add('hidden');
        gestionReponsesOptionnelles(false);
    } else {
        paraReponses.classList.remove('hidden');
        paraReponseLibre.classList.add('hidden');
        divBoutonAjouterReponse.classList.remove('hidden');
        gestionReponsesOptionnelles(true);
    }
}

function gestionReponsesOptionnelles(affiche) {
    let paraReponsesOptionnelles = document.querySelectorAll('.champ-reponse');
    if (affiche) {
        for (i=0; i<nbReponsesAffichees-1; i++) {
            paraReponsesOptionnelles[i].classList.remove('hidden');
        }
    } else {
        for (i=0; i<nbReponsesAffichees-1; i++) {
            paraReponsesOptionnelles[i].classList.add('hidden');
        }
    }
}

function conversion() {
    /* Thème choisi */
    let theme = document.querySelector('#id_theme').value;
    apercuImage(theme);
    apercuEnonce();
    apercuIndication(); 
    apercuFichier();
    apercuReponse();
    apercuCommentaire();
    gestionImages();
    gestionLiens();
    gestionTableaux();
    
    MathJaxReload(); 

    // recharger JS
    Prism.highlightAll(async=true);
}

let reponsesOptionnelles = document.querySelectorAll('.champ-reponse');

/* Ajout des champs "Réponse" */

let nbReponsesAffichees = 4 - document.querySelectorAll('.champ-reponse.hidden').length;

function ajouterReponse() {    
    if (nbReponsesAffichees <= 3) {
        let champ = document.getElementById(`champ-reponse${nbReponsesAffichees+1}`);
        champ.classList.toggle('hidden');
        nbReponsesAffichees = nbReponsesAffichees + 1;
    }
    if (nbReponsesAffichees == 4) {
        boutonAjouterReponse.classList.add('hidden');
    } 
}

function cacherBoutonAjouterReponse() {
    if (nbReponsesAffichees == 4) {
        boutonAjouterReponse.classList.add('hidden');
    }
}

let boutonAjouterReponse = document.querySelector('#ajouter-reponse');
boutonAjouterReponse.addEventListener('click', ajouterReponse);

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

let champsReponsesOptionnelles = document.querySelectorAll('#id_reponse2, #id_reponse3, #id_reponse4');
champsReponsesOptionnelles.forEach(champ => {
    champ.addEventListener("keyup", apercuReponse);
})

let reponseLibre = document.querySelector('#id_reponse_libre');
reponseLibre.addEventListener('keyup', apercuReponse);

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

document.querySelector('#id_commentaires').addEventListener("keyup", apercuCommentaire);

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
            // on n'affiche pas l'image du thème
            imageTheme.style.display = "none";
            imageTheme.data = "none";
            // on met à jour la source l'image de l'apercu
            apercuImage.src = urlImage.value;
            // on affiche l'image de l'apercu
            apercuImage.style.display = "block";
            // recherche des données EXIF pour les crédits
            var texteCredit = "";
            EXIF.getData(urlImage, function() {
                let artiste = EXIF.getTag(this, "Artist");
                let copyright = EXIF.getTag(this, "Copyright");
                texteCredit = copyright + " " + artiste;
            });
            // si des crédits sont absents
            if (creditsImageMD.value == "" && texteCredit == "") {
                // on n'affichage pas les crédits dans l'aperçu
                apercuCreditsImage.style.display = "none";
            }
            else {
                if (creditsImageMD.value == "" && !(texteCredit == "")) {
                    creditsImageMD.value = texteCredit;
                }
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

    if (!(texte == "") && (creditsImageMD.value == "")){
        
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
gestionQuestionLibre();
apercuImage(theme);
apercuEnonce();
apercuIndication(); 
apercuFichier();
apercuReponse();
cacherBoutonAjouterReponse(); // pour cacher le btn "ajouter une énigme" si 4 réponses
gestionImages();
gestionLiens();
gestionTableaux();
