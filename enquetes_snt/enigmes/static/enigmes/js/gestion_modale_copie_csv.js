// Affichage modale pour copie des liens dans le presse papier

let liensPressePapier = document.querySelectorAll(".lien-url-enquete");
liensPressePapier.forEach(item => {
    item.addEventListener("click", function(){
        ouvertureModale(item) ;
    });
})


function ouvertureModale(item) {
    // on récupère et construit l'url complète
    let cheminURL = item.dataset.lien;
    let domaineURL = window.location.host;
    let url = domaineURL + cheminURL;

    // on l'écrit dans la zone de texte de la modale
    

    // on affiche la modale
    if (item.classList.contains('partage')) {
        let inputLienPartage = document.getElementById('input-lien-partage');
        inputLienPartage.value = url;
        let modaleLienPartage = document.getElementById('modale-lien-partage');
        modaleLienPartage.classList.add("show");
    } else {
        let inputLien = document.getElementById('input-lien');
        inputLien.value = url;
        let modaleLienEleve = document.getElementById('modale-lien-eleve');
        modaleLienEleve.classList.add("show");
    }  
}


// Fermeture modale

let boutonsFermeture = document.querySelectorAll('.close-lien');
boutonsFermeture.forEach(item => {
    item.addEventListener("click", () => {
        if (item.classList.contains('partage')) {
            let modaleLienPartage = document.getElementById('modale-lien-partage');
            modaleLienPartage.classList.remove("show");
        } else {
            let modaleLienEleve = document.getElementById('modale-lien-eleve');
            modaleLienEleve.classList.remove("show");
        }
    })
})

// Copie du lien

let boutonsCopie = document.querySelectorAll('.icone-copie-lien');
boutonsCopie.forEach(item => {
    item.addEventListener('click', function() {
        if (item.classList.contains('partage')) {
            // on récupère l'url
            let url = document.getElementById('input-lien-partage').value;
            // on la copie dans le presse papier
            navigator.clipboard.writeText(url);
            // on affiche le message "Lien copié" pendant 3 secondes
            let paraMessage = document.getElementById('message-lien-partage');
            paraMessage.classList.add("show");
            setTimeout(function(){
                paraMessage.classList.remove("show");
            }, 3000);
        } else {
            // on récupère l'url
            let url = document.getElementById('input-lien').value;
            // on la copie dans le presse papier
            navigator.clipboard.writeText(url);
            // on affiche le message "Lien copié" pendant 3 secondes
            let paraMessage = document.getElementById('message-lien-eleve');
            paraMessage.classList.add("show");
            setTimeout(function(){
                paraMessage.classList.remove("show");
            }, 3000);
        }
        
    })
})


let textInputs = document.querySelectorAll('#input-lien, #input-lien-partage');
textInputs.forEach(item => {
    item.addEventListener('click', function() {
        item.select();
    })
})


// Affichage modale pour création du fichier CSV

boutonsCSV = document.querySelectorAll('.telecharger-csv');
boutonsCSV.forEach(item => {
    item.addEventListener("click", modaleGenerationCSV);
})

function modaleGenerationCSV() {
    let paraTexte = document.querySelector('.texte-modale');
    paraTexte.innerHTML = "Création en cours ...";
    let modale = document.querySelector('#lien-csv');
    modale.classList.add("show");
    setTimeout(function(){
        modale.classList.remove("show");
        paraTexte.innerHTML = "";
    }, 2000);
}