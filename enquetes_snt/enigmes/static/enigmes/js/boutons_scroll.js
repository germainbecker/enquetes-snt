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

    window.scrollTo({
        top: document.body.scrollHeight,
        left: 0,
        behavior: "smooth" 
    })
    
})