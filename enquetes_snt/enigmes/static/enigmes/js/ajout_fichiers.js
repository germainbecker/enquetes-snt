// VALIDATION DES FICHIERS A TELEVERSER

// Image

document.getElementById("id_image").addEventListener("change", validationImage);

function validationImage(){

    const extensionsAcceptees =  ['jpeg','jpg','png'],
            tailleMax = 1024*300; // 300 Kio

    
    // si un fichier image a été choisi
    if (this.files.length == 1 && this.files[0]) {
                
        // récupération du nom et de la taille à partir de l'objet fichier
        const {name: nomFichier, size: tailleFichier} = this.files[0];

        // récupération de l'extension de l'image
        const extensionFichier = nomFichier.split(".").pop();

        // vérification de l'extension et de la taille de l'image
        if (!extensionsAcceptees.includes(extensionFichier)){
            alert("Extension non acceptée. Seules les images aux formats .jpg ou .png sont acceptées.");
            this.value = null;            
            return false;
        } else if (tailleFichier > tailleMax){
            alert("Fichier trop volumineux. Assurez-vous que l'image ait une taille inférieure à 300 Kio.")
            this.value = null;
            return false;
        } else {
            return true;
        }
    } else {
        this.value = "";
        return false;
    }
}

// Pièce jointe

document.getElementById("id_fichier").addEventListener("change", validationPieceJointe);

function validationPieceJointe(){

    const extensionsAcceptees =  ['csv', 'xls', 'ods', 'xlsx' ,'py', 'html', 'css', 'txt', 'jpeg', 'jpg', 'png', 'json'],
            tailleMax = 1024 * 1000; // 1 Mio
    
    // si un fichier a été choisi
    if (this.files.length == 1 && this.files[0]) {
        
        // récupération du nom et de la taille à partir de l'objet fichier
        const { name:nomFichier, size:tailleFichier } = this.files[0];
        
        // récupération de l'extension du fichier
        const extensionFichier = nomFichier.split(".").pop();

        // vérification de l'extension et de la taille du fichier
        if (!extensionsAcceptees.includes(extensionFichier)){
            alert("Extension non acceptée. Seuls les fichiers aux formats .csv, .ods, .xls, .xlsx, .py, .html, .css, .jpg, .png et .json sont acceptés.");
            this.value = null;

            return false;
        } else if (tailleFichier > tailleMax){
            alert("Fichier trop volumineux. Assurez-vous que le fichier joint ait une taille inférieure à 1 Mio.")
            this.value = '';
            return false;
        } else {
            
            return true;
        }
    } else {
        
        return true;
    }  
}