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