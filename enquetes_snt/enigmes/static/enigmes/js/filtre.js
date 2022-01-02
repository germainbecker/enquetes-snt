/* Zone filtre et zone recherche */

function selectionFiltre() {
    var btnFiltresContainer = document.querySelector(".btn-filtres-container");
    // recherche du critère de filtre sélectionné
    let courant = btnFiltresContainer.querySelector(".focus");
    let critere = courant.dataset.filter;
    // récupération du contenu de la zone de recherche
    let search = document.getElementById("barre-recherche").value.toLowerCase();
    let filterDivs = document.getElementsByClassName("filterDiv");
    
    // cas particulier : afficher toutes les énigmes
    if (critere === "*") {
        for (i = 0; i < filterDivs.length; i++){
            let enigme = filterDivs[i];
            // si correspondance avec nom de l'auteur
            if (enigme.dataset.auteur.toLowerCase().indexOf(search) > -1) {
                if (caseMasqueQuestionsLibres.checked && enigme.classList.contains("question-libre")) {
                    enigme.classList.remove("show");
                } else {
                    enigme.classList.add("show");
                }
            }
            else {
                enigme.classList.remove("show");
            }            
        }
    }
    // autres cas
    else {
        for (i = 0; i < filterDivs.length; i++){
            let enigme = filterDivs[i];
            // si correspondance avec critère de filtre et nom de l'auteur
            if (enigme.classList.contains(critere) && enigme.dataset.auteur.toLowerCase().indexOf(search) > -1) {
                if (caseMasqueQuestionsLibres.checked && enigme.classList.contains("question-libre")) {
                    enigme.classList.remove("show");
                } else {
                    enigme.classList.add("show");
                }
            }
            else {
                enigme.classList.remove("show");
            }            
        }
    }
}

// détection clics sur boutons de filtre et ajout/suppression de la classe "focus"
var btnFiltresContainer = document.querySelector(".btn-filtres-container");
var btnsFiltre = btnFiltresContainer.getElementsByClassName("btn");
for (var i = 0; i < btnsFiltre.length; i++) {
    btnsFiltre[i].addEventListener("click", function() {
    var courant = btnFiltresContainer.querySelector(".focus");
    courant.classList.remove("focus");
    this.classList.add("focus");
    selectionFiltre();
    });
}

// détection saisies au clavier et bouton pour effacer
document.getElementById("barre-recherche").addEventListener("keyup", selectionFiltre);
document.getElementById("barre-recherche").addEventListener("search", selectionFiltre);


let caseMasqueQuestionsLibres = document.getElementById("case-choix-questions-libres");
caseMasqueQuestionsLibres.addEventListener("change", filtreQuestionsLibres)

selectionFiltre();

/* Zone tri */

function triAsc() {
    var listeEnigmes = document.getElementById("liste-enigmes");
    listeEnigmes.style.flexDirection = "column";
}

function triDesc() {
    var listeEnigmes = document.getElementById("liste-enigmes");
    listeEnigmes.style.flexDirection = "column-reverse";
}

var btnTriContainer = document.querySelector(".tri");
var btnsTri = btnTriContainer.getElementsByClassName("btn");
for (var i = 0; i < btnsTri.length; i++) {
    btnsTri[i].addEventListener("click", function() {
    var courant = btnTriContainer.querySelector(".focus");
    courant.classList.remove("focus");
    this.classList.add("focus");
    });
}

document.getElementById("asc").addEventListener("click", triAsc);
document.getElementById("desc").addEventListener("click", triDesc);


/* Afficher/Masque les énigmes à réponse libre */

function filtreQuestionsLibres() {
    let enigmesReponseLibre = document.querySelectorAll('.question-libre');
    if (caseMasqueQuestionsLibres.checked) {
        enigmesReponseLibre.forEach(enigme => {
            enigme.classList.remove('show');
        });
    } else {
        enigmesReponseLibre.forEach(enigme => {
            enigme.classList.add('show');
        });
    }
}
