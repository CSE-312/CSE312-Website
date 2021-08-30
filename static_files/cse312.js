// Run as soon as the script loads to prevent a white flash
var useDarkTheme = localStorage.getItem("darkTheme") === "true";
setDarkMode(useDarkTheme);

function bodyLoaded() {
    collapse();
    // Set the dark theme checkbox to the correct state
    if (useDarkTheme) {
        document.getElementById("darkThemeCheckbox").checked = true;
    }
}

function setDarkMode(isDark) {
    // Based on https://stackoverflow.com/a/37416531
    var darkCss = document.getElementById("darkThemeCss");
    darkCss.disabled = !isDark;
    localStorage.setItem("darkTheme", isDark)
}

function collapse() {
    for (let x of document.getElementsByClassName("collapse")) {
        if (localStorage.getItem(x.id) === "hide") {
            x.setAttribute("class", "collapse");
        }
    }
    for (let x of document.getElementsByTagName("a")) {
        if (x.getAttribute("data-toggle")) {
            x.addEventListener("click", function () {
                const elem = document.getElementById(x.getAttribute("data-target").replace("#", ""));
                if (elem.classList.contains("show")) {
                    localStorage.setItem(elem.id, "hide");
                } else {
                    localStorage.removeItem(elem.id);
                }
            });
        }
    }
}