const btn_haut = document.querySelector('#btn-scroll-haut');
btn_haut.addEventListener('click', () => {

    window.scrollTo({
        top: 0,
        left: 0,
        behavior: "smooth" 
    })

})

const btn_bas = document.querySelector('#btn-scroll-bas');
btn_bas.addEventListener('click', () => {
    let container = document.querySelector('.content-container');
    let footer = document.querySelector('footer');
    window.scrollTo({
        top: document.body.scrollHeight - footer.offsetHeight - window.innerHeight - 20,
        left: 0,
        behavior: "smooth" 
    })
    
})