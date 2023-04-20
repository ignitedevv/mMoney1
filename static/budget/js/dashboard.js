var elements = document.getElementsByClassName('_16px _10-padding-left light company right updated')

for (let i = 0; i < elements.length; i++) {
    var elm = elements[i]
    var elm_time = elm.innerHTML

}


// Update the difference every minute
setInterval(() => {
    for (let i = 0; i < elements.length; i++) {
        var elm = elements[i]
        var newe = (Number(elm.innerHTML.split(" ")[0]) + 1)
        elements[i].innerHTML = newe + ' ' + 'minutes'

}





}, 60000); // Update every minute (60000 milliseconds)




function backHide() {
    var recWrapper = document.getElementById('specific-payment-wrapper')
    recWrapper.style.display = 'none'
}

function upcomingPaymentsShow(a, merchant_name, category, payment, status, frequency, icon) {
    var average_payment = document.getElementById('average-payment')
    var spent_this_year = document.getElementById('spent-this-year')
    var rec_frequency = document.getElementById('rec-frequency')
    var rec_icon = document.getElementById('rec-icon')
    rec_icon.src = icon
    console.log(rec_icon)

    var title = document.getElementById('rec-title')
    var subtitle = document.getElementById('rec_category')

    title.innerHTML = merchant_name
    subtitle.innerHTML = category
    average_payment.innerHTML = payment
    rec_frequency.innerHTML = frequency
    var recWrapper = document.getElementById('specific-payment-wrapper')
    recWrapper.style.display = 'flex'

}