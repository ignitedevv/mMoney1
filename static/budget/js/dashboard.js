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