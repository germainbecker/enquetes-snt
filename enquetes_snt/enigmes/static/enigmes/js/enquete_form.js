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
    //console.log(cases);
    cases.forEach(elt => {
        let num = elt.id.split("-")[1];
        let id_case = "case-" + num;
        let conteneurCase = document.getElementById(id_case);
        if (elt.checked) {
            console.log(num);
            conteneurCase.style.backgroundColor = "var(--main)";
        }
    })
}

function changeListeCle(item) {
    let num = item.id.split("-")[1];
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
    }
}

let liste_num_enigmes = [];
const couleurFond = document.querySelector(".checkbox-container").style.backgroundColor;
initialisationCouleur();

// Gestion boutons radio pour la correction et le score

let btnCorrection = document.getElementById("correction_oui");

btnCorrection.addEventListener("click", () => {
    // si correction activée alors il faut activer par défaut le score
    let btnScore = document.getElementById("score_oui");
    btnScore.checked = true;
})


let btnPasDeScore = document.getElementById("score_non");

btnPasDeScore.addEventListener("click", () => {
    // si correction activée le bouton de score ne peut pas être mis à non
    if (btnCorrection.checked) {
        let btnScore = document.getElementById("score_oui");
        btnScore.checked = true;
    } else {
        btnPasDeScore.checked = true;
    }
})

// Vérification formulaire avant envoi (au moins une énigme sélectionnée)

document.getElementById("btn-creer-enquete").addEventListener("click", function(event) {
    console.log(document.getElementById("form"));
    let zoneErreur = document.querySelector('#message-erreur');
    var donnees_formulaire = new FormData(document.getElementById("form"));
    if (!donnees_formulaire.has("enigmes")) {
        event.preventDefault();
        zoneErreur.style.visibility = "visible";
        zoneErreur.style.color = "red";
    }
}, false);