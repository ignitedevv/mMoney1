function changeTransaction(a) {
    const correctButton = a.closest(".div-block-4").querySelector(".correct-button");
    if (correctButton.style.display === 'none') {
        correctButton.style.display = 'block'
    }
}


function sendTransaction(a, tran_id, cat1, cat2) {
    console.log('send transaction')
    console.log(a.closest(".white-item.transaction"))
    var mainkid = a.closest(".white-item.transaction")
    var transaction_title = mainkid.children[0].children[1].innerText
    var transaction_cost = mainkid.children[0].children[2].innerText
    var csrf = mainkid.children[0].children[3].children[0].value

    var transaction_date = mainkid.children[1].children[0].innerText
    var selected_budget_index = mainkid.children[1].children[1].children[0].selectedIndex
    var selected_budget = mainkid.children[1].children[1].children[0].options[selected_budget_index].value
    var selected_budget_title = mainkid.children[1].children[1].children[0].options[selected_budget_index].innerText


    console.log(csrf)



    $.ajax({
      type: "POST",
      url: '/budget/transactions',
      data: {
        csrfmiddlewaretoken: csrf,
        action: "post",

        budget: selected_budget,
        transaction_date: transaction_date,
        tran_title: transaction_title,
        the_id: tran_id,
        amount: transaction_cost,
        category1: cat1,
        category2: cat2
        }
    })
}


// functionality for filtering transactions on transactions page
function transactionsToggle(a, target) {
    var element = a.className
    var currentSelected = document.getElementsByClassName('transaction-button selected')

    currentSelected[0].className = 'transaction-button unselected'
    a.className = 'transaction-button selected'
    console.log(element)
    console.log(target)

}



function display_under(a) {
    a.children[1].style.display = 'block'

}









