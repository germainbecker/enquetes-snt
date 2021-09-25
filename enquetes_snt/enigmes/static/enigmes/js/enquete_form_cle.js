// Gestion bouton aperçu

// on initialise l'attribut value du btn d'aperçu avec la clé initiale
let cleEnquete = document.getElementById('id_cle');
let btnApercu = document.getElementById("btn-apercu-enquete");
btnApercu.value = cleEnquete.value;

// on met à jour à l'attribut value du btn d'aperçu à chaque changement de clé
cleEnquete.addEventListener("keyup", function() {
    btnApercu.value = this.value;
})

let btnValidation = document.getElementById("btn-validation");

btnValidation.addEventListener("click", () => {
    let champDescription = document.getElementById('id_description');
    if (!(champDescription.required)) {
        champDescription.setAttribute("required","");
    }
})

btnApercu.addEventListener("click", () => {
    // au premier clic, le formulaire n'est pas directement envoyé si les champs clé et description (requis tous
    // les deux) sont vides tous les deux

    // le code suivant s'exécute

    // si le champ description est vide, on retire l'attribut required et on déclenche un autre clic
    let champDescription = document.getElementById('id_description');
    if (champDescription.value === '') {
        champDescription.removeAttribute("required");
        btnApercu.click();
        // qui enverra le formulaire seulement si le champ clé est rempli
    }
})

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
