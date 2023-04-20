function createFreeAccount() {

}

function doneBtn(a) {
    var gobtn2 = document.getElementById('go-btn2')
    var accounts_group = document.getElementById('accounts-group')
    var check1 = document.getElementById('check1')
    var editbtn = document.getElementById('edit-btn')
    var linkbtn = document.getElementById('link-button')

    linkbtn.style.display = 'none'
    editbtn.style.display = 'flex'
    a.style.display = 'none'
    check1.className = 'image-5'

    gobtn2.style.display = 'flex'
    accounts_group.style.display = 'none'
}
