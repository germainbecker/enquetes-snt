// Gestion sélection des énigmes
document.querySelectorAll('.checkbox-container, .case-a-cocher').forEach(item => {
    item.addEventListener('click', function () { 
        miseAJour(item)
    });
});

function miseAJour(item) {
    changeCouleur(item);
    changeListeCle(item);
    changeCle();
}

function changeCouleur(item) {
    let num = item.id.split("-")[1];
    let id_case = "case-" + num;
    let id_enigme = "enigme-" + num;
    let conteneurCase = document.getElementById(id_case);    
    let caseACocher = document.getElementById(id_enigme);
    if (caseACocher.checked) {
        caseACocher.checked = false;
        conteneurCase.style.backgroundColor = couleurFond;
    } else {
        caseACocher.checked = true;
        conteneurCase.style.backgroundColor = "var(--main)";
    }
}

function initialisationCouleur() {
    let cases = document.querySelectorAll('.case-a-cocher');
    cases.forEach(elt => {
        let num = elt.id.split("-")[1];
        let id_case = "case-" + num;
        let conteneurCase = document.getElementById(id_case);
        if (elt.checked) {
            conteneurCase.style.backgroundColor = "var(--main)";
        }
    })
}

function changeListeCle(item) {
    let num = item.id.split("-")[1];
    // Si l'énigme était sélectionnée
    if (listeNumEnigmes.includes(num)) {
        // on la supprime du tableau des numéros d'énigmes
        index_enigme = listeNumEnigmes.indexOf(num);
        listeNumEnigmes.splice(index_enigme, 1);

        // si c'est une énigme à question libre on la retire de l'ensemble des énigmes à question libre
        if (ensembleEnigmesQuestionLibre.has(num)) {
            ensembleEnigmesQuestionLibre.delete(num);
        }
    } else {
        // sinon on l'ajoute
        listeNumEnigmes.push(num);
        // si l'énigme est à question libre on l'ajoute à l'ensemble des énigmes à question libre
        if (item.dataset.question === "ql") {
            ensembleEnigmesQuestionLibre.add(num);
        }
    }
}

function changeCle() {
    console.log(ensembleEnigmesQuestionLibre)
    chaine = listeNumEnigmes.join(";");
    let para = document.getElementById("cle-enquete-contenu");
    let correctionAuto = document.getElementById("correction-auto");
    
    if (chaine === "") {
        para.innerHTML = "Vous n'avez sélectionné aucune énigme.";
        correctionAuto.classList.remove("show");
    } else {
        let nb_enigmes = listeNumEnigmes.length.toString();
        para.innerHTML = "Vous avez sélectionné " + nb_enigmes + " énigme(s)." + " La clé de votre enquête est : " + chaine;

        // si il y a au moins une énigme à réponse libre sélectionnée
        if (ensembleEnigmesQuestionLibre.size > 0) {
            // on affiche un message à l'utilisateur
            correctionAuto.innerHTML = "L'enquête contient au moins une énigme \"à réponse libre\". Une correction entièrement automatique sera donc impossible.";
            correctionAuto.classList.add("show");
        } else {
            correctionAuto.classList.remove("show");
        }

        // on efface le message d'erreur si une enquete est sélectionnée
        document.querySelector('#message-erreur').classList.remove("show");
    }

    // on met à jour la valeur du champ clé caché
    document.getElementById('id_cle').value = chaine;

   

}

let listeNumEnigmes = [];
let ensembleEnigmesQuestionLibre = new Set();
const couleurFond = document.querySelector(".checkbox-container").style.backgroundColor;
initialisationCouleur();

// Gestion cases à cocher pour la correction et le score

let CbCorrection = document.getElementById('id_correction');
let CbScore = document.getElementById('id_score');

CbCorrection.addEventListener('change', () => {
    // si correction activée alors il faut activer par défaut le score
    if (CbCorrection.checked){
        CbScore.checked = true;
    }
})

CbScore.addEventListener('click', () => {
    // si correction activée alors il faut activer par défaut le score
    if (CbCorrection.checked) {
        CbScore.checked = true;
    } else {
        if (CbScore.checked) {
            CbScore.checked = true;
        } else {
            CbScore.checked = false;
        }
    }
})

// Vérification formulaire avant envoi (au moins une énigme sélectionnée)

document.getElementById("btn-creer-enquete").addEventListener("click", function(event) {
    let zoneErreur = document.querySelector('#message-erreur');
    var donnees_formulaire = new FormData(document.getElementById("form"));
    if (!donnees_formulaire.has("enigmes")) {
        event.preventDefault();
        zoneErreur.classList.add("show");
        /* zoneErreur.style.visibility = "visible";
        zoneErreur.style.color = "red"; */
    }
}, false);