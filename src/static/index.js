function menuClick(x) {

    const media = window.matchMedia("(max-width: 1000px)");

    if (media.matches) {
        x.classList.toggle("change");
        console.log("CHANGE")
    }
    
}