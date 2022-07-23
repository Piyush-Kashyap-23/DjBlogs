const userBtn = document.querySelector(".user-btn");
if (userBtn) {
userBtn.addEventListener("click", (e) => {
    e.preventDefault()
    const dropdown = document.querySelector(".dropdown");
    console.log(dropdown);
    if (dropdown.classList.contains("transform-remove")) {
        dropdown.classList.remove("transform-remove")
    } else {
        dropdown.classList.add("transform-remove")
    }
})
}