document.querySelector('#btn-hamburger').addEventListener('click', changeIcone);

function changeIcone() {
    
    let btnMenu = document.querySelector('#btn-hamburger');
    let iconeBurger = document.querySelector('#hamburger');
    let iconeCroix = document.querySelector('#croix');

    if (btnMenu.checked) {
        iconeBurger.style.display = "none";
        iconeCroix.style.display = "block";
    } else {
        iconeBurger.style.display = "block";
        iconeCroix.style.display = "none";
    }
}