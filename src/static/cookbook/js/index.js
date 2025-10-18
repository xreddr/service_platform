
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = mm + '-' + dd + '-' + yyyy;
hashToday = '#' + today
console.log(today)
window.addEventListener('load', function() {
    const element = document.getElementById(today);
    console.log(element)
    if (element) {
      element.scrollIntoView();
    }
    this.window.scrollTo(0, element.offsetTop-200)
    document.getElementById(element.id).style.border = "thick solid orange";
  });

var catShowHide = function(element) {
  console.log(element)
}