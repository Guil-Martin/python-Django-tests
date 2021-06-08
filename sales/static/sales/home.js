const reportBtn = document.getElementById('report-btn')
const modalBody = document.getElementById('modal-body')
const img = document.getElementById('img')

reportBtn.addEventListener('click', (e) => {
    img.setAttribute('class', "w-100")
    modalBody.prepend(img)
})