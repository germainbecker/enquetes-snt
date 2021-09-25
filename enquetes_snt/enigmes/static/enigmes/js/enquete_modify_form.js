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
    let num = item.id.split("_").pop();
    let id_case = "case_" + num;
    let id_enigme = "id_enigme_" + num;
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
        let num = elt.id.split("_").pop();
        let id_case = "case_" + num;
        let conteneurCase = document.getElementById(id_case);
        if (elt.checked) {
            conteneurCase.style.backgroundColor = "var(--main)";
        }
    })
}

function changeListeCle(item) {
    let num = item.id.split("_").pop();
    if (liste_num_enigmes.includes(num)) {
        index_enigme = liste_num_enigmes.indexOf(num);
        liste_num_enigmes.splice(index_enigme, 1);
    } else {
        liste_num_enigmes.push(num);
    }
}

function changeCle() {
    chaine = liste_num_enigmes.join(";");
    let para = document.getElementById("cle-enquete-contenu");
    if (chaine === "") {
        para.innerHTML = "Vous n'avez sélectionné aucune énigme.";
    } else {
        let nb_enigmes = liste_num_enigmes.length.toString();
        para.innerHTML = "Vous avez sélectionné " + nb_enigmes + " énigme(s)." + " La clé de votre enquête est : " + chaine;
        // on efface les messages d'erreur si une enquete est sélectionnée
        let zonesErreur = document.querySelectorAll('.message-erreur');
        zonesErreur.forEach(item => {
            item.style.display = "none";
        })
    }

    // on recopie le tout en bas de page
    let zoneCle = document.getElementById('cle-enquete');
    let paraCopie = document.getElementById("copie-cle-enquete");
    paraCopie.innerHTML = zoneCle.innerHTML;

    // on met à jour la valeur du champ clé caché
    document.getElementById('id_cle').value = chaine;
}


/* génération de la clé initiale */

function creerCleInitiale() {
    let cle = document.getElementById('liste-enigmes').dataset.cle;
    liste_num_enigmes = cle.split(";")
    changeCle();
}

let liste_num_enigmes = [];
creerCleInitiale();
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
    let zonesErreur = document.querySelectorAll('.message-erreur');
    var donnees_formulaire = new FormData(document.getElementById("form"));
    if (!donnees_formulaire.has("enigmes")) {
        event.preventDefault();
        zonesErreur.forEach(item => {
            item.style.display = "block";
            item.style.color = "red";
        })
        
    }
}, false);