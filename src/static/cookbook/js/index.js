// Calendar
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = mm + '-' + dd + '-' + yyyy;
hashToday = '#' + today
// console.log(today)
window.addEventListener('load', function() {
    const element = document.getElementById(today);
    // console.log(element)
    if (element) {
      element.scrollIntoView();
    }
    this.window.scrollTo(0, element.offsetTop-200)
    const headerBG = element.querySelector(".l_date_container");
    // headerBG.style.backgroundColor = 'orange';
    document.getElementById(element.id).style.borderLeft = "thick solid orange";
  });

  
const dateBoxes = document.querySelectorAll('.date_box');

dateBoxes.forEach(box => {
    const dayHeader = box.querySelector('.calendar_day');
    
    if (dayHeader && dayHeader.textContent.trim().toLowerCase() === 'sunday') {
        box.style.marginTop = '5rem';
    }
});

// Home, Categories 

function catShowHide(element) {
    console.log(element);
    let parentArray = Array.from(element.parentNode.children);
    let base = parentArray.indexOf(element);
    let target = parentArray[base+1];
    console.log(target)
    if (target.classList.contains('recipe_list') && target.style.display === 'none') {
        target.style.display = 'flex';
        target.scrollIntoView();
        window.scrollTo(0, target.offsetTop-100)
    }
    else if (target.classList.contains('recipe_list') && target.style.display === 'flex') {
        target.style.display = 'none';
        window.scrollTo(0, document.getElementById('cb_home_menu').offsetTop-10)
    }
};
