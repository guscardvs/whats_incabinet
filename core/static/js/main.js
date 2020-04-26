copyright = document.querySelector('.copyright')
curdate = new Date
copyright.textContent = `© Copyright ${curdate.getFullYear()}`


function modalOpen(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('show');
}


function modalClose(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('show');
}
