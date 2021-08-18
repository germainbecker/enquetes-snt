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
    console.log(CbCorrection.checked)
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
