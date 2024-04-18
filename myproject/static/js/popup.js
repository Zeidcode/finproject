const popUpEl = document?.querySelector(".popUp");
const closePopUpEl = document?.querySelector(".close-popUp");
closePopUpEl?.addEventListener("click", () => {
    popUpEl.classList.remove("show-popUp");
    window.location.href = '/cooker/';
});