// Affichage modale pour copie dans presse papier

let liensPressePapier = document.querySelectorAll(".lien-url-enquete");
liensPressePapier.forEach(item => {
    item.addEventListener("click", function(){
        copiePressePapier(item) ;
    });
})

function copiePressePapier(item) {
    let cheminURL = item.dataset.lien;
    console.log(cheminURL);
    let domaineURL = window.location.host;
    let url = domaineURL + cheminURL;
    console.log(url);
    navigator.clipboard.writeText(url);
    let paraTexte = document.querySelector('.texte-modale');
    paraTexte.innerHTML = "Lien copié";
    let modale = document.querySelector('.modal-lien-content');
    modale.classList.add("show");
    setTimeout(function(){
        modale.classList.remove("show");
        paraTexte.innerHTML = "";
    }, 1200);
}

// Affichage modale pour création du fichier CSV

if (document.querySelector(".telecharger-csv")){
    document.querySelector(".telecharger-csv").addEventListener("click", modaleGenerationCSV);
}

function modaleGenerationCSV() {
    let paraTexte = document.querySelector('.texte-modale');
    paraTexte.innerHTML = "Création en cours ...";
    let modale = document.querySelector('.modal-lien-content');
    modale.classList.add("show");
    setTimeout(function(){
        modale.classList.remove("show");
        paraTexte.innerHTML = "";
    }, 2000);
}