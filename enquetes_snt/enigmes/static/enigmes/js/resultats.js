// Gestion des affichages/masquages

let identifiantAffiches = false;
let reponsesAffichees = false;
let afficherResultats = true;
let ordreAlpha = false;

gestionIdentifiants();
gestionReponses();
gestionResultats();

document.getElementById("switch-id").addEventListener("change", gestionIdentifiants);
document.getElementById("switch-reponses").addEventListener("change", gestionReponses);
document.getElementById("switch-resultats").addEventListener("change", gestionResultats);
document.getElementById("switch-tri").addEventListener("change", gestionTri);

function gestionIdentifiants() {
    var identifiantsElevesBefore = document.querySelectorAll(".cache-eleve");
    var identifiantsEleves = document.querySelectorAll(".id-eleve");
    if (document.getElementById("switch-id-checkbox").checked) {
        // si le slider est activé on affiche les identifiants
        for (var i = 0; i < identifiantsEleves.length; i++) {
            identifiantsElevesBefore[i].dataset.cache = "";
            identifiantsEleves[i].style.display = "block";
        }
    } else {
        // sinon on les masque par des ●●●●
        for (var i = 0; i < identifiantsEleves.length; i++) {
            identifiantsElevesBefore[i].dataset.cache = "●●●●";
            identifiantsEleves[i].style.display = "none";
        }
    }
    identifiantAffiches = !identifiantAffiches;
}

function gestionReponses() {
    var reponsesEleves = document.querySelectorAll(".reponse");
    if (document.getElementById("switch-reponses-checkbox").checked) {
        for (var i = 0; i < reponsesEleves.length; i++) {
            reponsesEleves[i].classList.remove("hidden");
        }
    } else {
        for (var i = 0; i < reponsesEleves.length; i++) {
            reponsesEleves[i].classList.add("hidden");
        }
    }
}

function gestionResultats() {
    var zoneReponsesEleves = document.querySelectorAll(".correct, .incorrect, .libre");
    var svgReponses = document.querySelectorAll(".correct svg, .incorrect svg, .libre svg");
    var nbReponsesEleves = document.querySelectorAll(".case-reponse").length;
    console.log(nbReponsesEleves);
    var scoreEleves = document.querySelectorAll(".score-eleve");
    var pourcentagesReussite = document.querySelectorAll(".pourcentage");
    if (document.getElementById("switch-resultats-checkbox").checked) {
        for (var i = 0; i < nbReponsesEleves; i++) {
            zoneReponsesEleves[i].classList.remove("masque-resultat");
            svgReponses[i].classList.remove("hidden");
        }
        for (var j = 0; j < scoreEleves.length; j++) {
            scoreEleves[j].classList.remove("hidden");
        }
        for (var k = 0; k < pourcentagesReussite.length; k++) {
            pourcentagesReussite[k].style.visibility = "initial";
        }
    } else {
        for (var i = 0; i < nbReponsesEleves; i++) {
            zoneReponsesEleves[i].classList.add("masque-resultat");
            svgReponses[i].classList.add("hidden");
        }
        for (var j = 0; j < scoreEleves.length; j++) {
            scoreEleves[j].classList.add("hidden");
        }
        for (var k = 0; k < pourcentagesReussite.length; k++) {
            pourcentagesReussite[k].style.visibility = "hidden";
        }
    }
    
    afficherResultats = !afficherResultats;
}

function triAlphabetique() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("tableau-de-resultats");
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* On boucle sur toutes les lignes du tableau sauf la première (head)
        et la denière qui contient les pourcentages de réussite */
        for (i = 1; i < (rows.length - 2); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].querySelector("span").innerHTML.toLowerCase();  /*le nom est dans le premier span*/
            y = rows[i + 1].querySelector("span").innerHTML.toLowerCase();
            // Check if the two rows should switch place:
            if (x > y) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }    
}

function triChronologique() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("tableau-de-resultats");
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* On boucle sur toutes les lignes du tableau sauf la première (head)
        et la denière qui contient les pourcentages de réussite */
        for (i = 1; i < (rows.length - 2); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = parseInt(rows[i].querySelector("span").dataset.resultats);  /*le numéro de l'élève (chronologique) est l'attribut resultats du premier span*/
            y = parseInt(rows[i + 1].querySelector("span").dataset.resultats);
            // Check if the two rows should switch place:
            if (x > y) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }    
}

function gestionTri() {    
    if (document.getElementById("switch-tri-checkbox").checked) {
        triAlphabetique();
    } else {
        triChronologique();
    }
    ordreAlpha = !ordreAlpha;        
}

// on lance l'animation de chargement au moment de la requête HTMX (si actualisation manuelle)
document.body.addEventListener('htmx:xhr:loadstart', () => {
    if (!(checkboxActualisationAuto.checked)) {
        voirAnimationChargement();
    } else {
        cacherAnimationChargement();
    }
});

// on applique les choix pour l'affichage après la réponse à la requête HTMX 
document.body.addEventListener('htmx:afterOnLoad', () => {
    gestionIdentifiants();
    gestionReponses();
    gestionResultats();
    gestionTri();
    cacherAnimationChargement(); // et on cache l'anim de chargement
});



// Requête fetch pour actualiser les résultats sans recharger toute la page

/* document.querySelector("#fetch-call").addEventListener("click", event => {
    event.preventDefault(); // le formulaire ne doit pas être envoyé (sinon rafraichissement page)
    if (!(checkboxActualisationAuto.checked)) {
        voirAnimationChargement();
    } else {
        cacherAnimationChargement();
    }
    
    // Création d'une requête à envoyer au serveur
    let formData = new FormData();
    formData.append('maj', 'true');
    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': csrfTokenValue}
    });
    // envoi de la requête asynchrone (avec fetch), attente de la promesse  et traitement de la réponse
    fetch(request)
        .then(response => response.json())
        .then(result => {
            majResultats(result);
            // fin de l'animation
            modale.classList.remove("show");
            iconeModale.classList.remove("rotate");   
        });
}); */

const modale = document.querySelector("#modale-actualisation");
const iconeModale = document.querySelector(".modal-actualisation-content img");

function voirAnimationChargement() {
    // animation icone de chargement
    modale.classList.add("show");
    iconeModale.classList.add("rotate");
}

function cacherAnimationChargement() {
    modale.classList.remove("show");
    iconeModale.classList.remove("rotate");
}

var actualisationAuto;

var checkboxActualisationAuto = document.querySelector("#case-actualisation-automatique");

checkboxActualisationAuto.addEventListener('change', function() {
  if (this.checked) {
    actualisationAuto = setInterval(clicBoutonActualiser, 15000);
  } else {
    clearInterval(actualisationAuto);
  }
});

function clicBoutonActualiser() {
    document.querySelector("#fetch-call").click();
}



function majResultats(result) {
    const nbResultats = result['resultats'].length;
    let numEnigmes = result["enigmes"];

    // ajout des lignes avec les nouveaux résultats
    let resultatsEleves = document.querySelector("#resultats-eleves");
    let nbResultatsAffiches = resultatsEleves.childElementCount - 1;
    let ligneReussite = document.querySelector("#ligne-reussite");
    for (let i=nbResultatsAffiches; i<nbResultats; i++) {
        let nouvResultat = document.createElement('tr');
        nouvResultat.innerHTML = creationLigne(result['resultats'][i], i);
        resultatsEleves.insertBefore(nouvResultat, ligneReussite);
    }

    // ajout des nouveaux pourcentages de réussite
    var pourcentagesReussite = document.querySelectorAll(".pourcentage");
    let pourcentages_bonnes_reponses = Object.values(result['pourcentage']); // conversion en un tableau
    let nbEnigmes = result['enigmes'].length;
    for (let i=0; i<nbEnigmes; i++) {
        pourcentagesReussite[i].innerHTML = String(pourcentages_bonnes_reponses[i]) + ' %';
    }
    
    gestionIdentifiants();
    gestionReponses();
    gestionResultats();
    gestionTri();

    function creationLigne(resultat, numResultat) {
        /*
        result est un objet du type 
            {
                "id": "id_eleve",
                "score": <score_eleve>,
                "enigmes": [<id_enigme1>, <id_enigme2>, ...], 
                "reponses": {
                    <id_enigme1>: {rep_eleve: "rep_eleve", correct: true/false},
                    <id_enigme2>: {rep_eleve: "rep_eleve", correct: true/false},
                    ...
                },
                "date": date
            }
        */
        let idEleve = resultat["id"];
        let scoreEleve = resultat["score"];
        let date = conversionDate(resultat["date"]);
        let nbEnigme = Object.keys(resultat["reponses"]).length;
        let htmlLigne = '<td class="zone-eleve-score cache-eleve" data-cache="●●●●">' +
                        '<span class="flex-grow id-eleve" data-resultats=' + String(numResultat) + '>' + idEleve + '</span>' +
                        '<span class="score-eleve">' + String(scoreEleve) + ' / ' + String(nbEnigme) + '</span></td>';
        
        let reponsesEleve = resultat["reponses"];

        numEnigmes.forEach(function(num) {
            if (reponsesEleve[num]["correct"] == true) {
                htmlLigne += '<td class="correct">' +
                '<div class="reponse-eleve">' +
                    '<svg width="15" height="15" viewBox="0 0 15 15" focusable="false" fill="currentColor" aria-hidden="true">' +
                        '<path d="M13.475 5.464a.75.75 0 011.123.989l-.073.083-6.13 6a.75.75 0 01-.965.07l-.084-.07-3.87-3.79a.75.75 0 01.964-1.143l.085.072L7.87 10.95l5.604-5.487z"></path>' +
                    '</svg>'
            } else {
                htmlLigne += '<td class="incorrect">' +
                '<div class="reponse-eleve">' +
                    '<svg width="15" height="15" viewBox="0 0 15 15" focusable="false" fill="currentColor" aria-hidden="true">' +
                        '<path fill-rule="evenodd" d="M13.53 5.53a.75.75 0 00-1.06-1.06L9 7.94 5.53 4.47a.75.75 0 00-1.06 1.06L7.94 9l-3.47 3.47a.75.75 0 001.06 1.06L9 10.06l3.47 3.47a.75.75 0 001.06-1.06L10.06 9l3.47-3.47z"></path>' +
                    '</svg>'
            }
            htmlLigne += '<span class="reponse hidden">' + reponsesEleve[num]["rep_eleve"] + '</span>'
        });
        htmlLigne += '<td class="date-resultat">' + date + '</td>'
        return htmlLigne;
        }
    
        function conversionDate(date) {
            d1 = new Date(date);
            let locale = 'fr-FR';
            let opts = {hour: '2-digit', minute: '2-digit'};
            return d1.toLocaleDateString(locale) + ' ' + d1.toLocaleTimeString(locale, opts);
        }
}





