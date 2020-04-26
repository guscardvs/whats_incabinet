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

const upDown = {
    plus: document.querySelector('#plus'),
    minus: document.querySelector('#minus'),
    input: document.querySelector('#up-down')
}

if (upDown.plus && upDown.minus && upDown.input) {
    upDown.plus.onclick = () => upDown.input.value = parseInt(upDown.input.value) + 1

    upDown.minus.onclick = () => {
        if (parseInt(upDown.input.value) > 0) {
            upDown.input.value = parseInt(upDown.input.value) - 1
        }
    }

}
