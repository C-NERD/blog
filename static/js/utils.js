var darkMode = false;
const checkedStr = (darkMode) => {

    if (darkMode){

        return `checked = "true"`;
    }else{

        return ``;
    }
};
const menuDom = (darkMode) => `
<span id = "overlay_container">
    <span id = "menu">
        <nav id = "menubar">
            <div id = "cancelbox" class = "iconbox" onclick = "rmMenu()">
                <img class = "icon" src = "../images/icons/xmark.svg" alt = "cancel_icon">
            </div>
        </nav>
        <span id = "menu_content">
            <div class = "menubtn">
                <label class = "switch">
                    <input type = "checkbox" id = "theme_changer" ${checkedStr(darkMode)} onchange = "toggleTheme()">
                    <span class = "slider">
                    </span>
                </label>

                Dark Mode
            </div>
            <div class = "menubtn">
                <div class = "iconbox">
                    <img class = "icon" src = "../images/icons/book.svg">
                </div>
                Articles
            </div>
            <a target="_blank" href = "../docs/cv.pdf" class = "menubtn">
                <div class = "iconbox">
                    <img class = "icon" src = "../images/icons/file-pdf.svg">
                </div>
                My CV
            </a>
            <hr>
            <div class = "menubtn">
                <a target="_blank" href = "mailto:cnerd694@gmail.com">
                    <div class = "iconbox">
                        <img class = "icon" src = "../images/icons/gmail.svg">
                    </div>
                </a>
                <a target="_blank" href = "https://t.me/cnerd694">
                    <div class = "iconbox">
                        <img class = "icon" src = "../images/icons/telegram.svg">
                    </div>
                </a>
                <a target="_blank" href = "https://github.com/C-NERD">
                    <div class = "iconbox">
                        <img class = "icon" src = "../images/icons/github.svg">
                    </div>
                </a>
                <a target="_blank" href = "mailto:cnerd694@outlook.com">
                    <div class = "iconbox">
                        <img class = "icon" src = "../images/icons/outlook.svg">
                    </div>
                </a>
            </div>
            © Blog by C-NERD
        </span>
    </span>
</span>
`;
const articleDom = (name, link) => `
<a href = "${link}" class = "menu_article">
    ${name}
</a>
`
const articleContainer = (articles) => {

    var opening = `
<span id = "overlay_container">
    <span id = "menu">
        <nav id = "menubar">
            <div id = "cancelbox" class = "iconbox" onclick = "rmMenu()">
                <img class = "icon" src = "../images/icons/xmark.svg" alt = "cancel_icon">
            </div>
        </nav>
        <span id = "menu_content">
    `;
    for (article in articles) {

        opening = opening.concat(`\n${article}`);
    }

    opening = opening.concat(`
        </span>
    </span>
</span>
    `);
    return opening;
}

function toggleTheme() {
    
    if (document.getElementById("theme_changer").checked) {

        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
    }else{

        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    }
}

function rmMenu() {

    let body = document.getElementsByTagName("body")[0];
    let overlayContainer =  document.getElementById("overlay_container");
    if (overlayContainer !== null) {

        body.removeChild(overlayContainer);
    }
}

function showMenu() {

    let body = document.getElementsByTagName("body")[0];
    let overlayContainer =  document.getElementById("overlay_container");
    if (overlayContainer !== null) {

        body.removeChild(overlayContainer);
    }

    body.innerHTML = `${body.innerHTML}\n${menuDom(darkMode)}`;
}

function loadCallback() {

    let theme = localStorage.getItem("theme");
    if (theme !== null && (theme === "dark" || theme === "light")) {

        if (theme === "dark") {

            darkMode = true;
        }else{

            darkMode = false;
        }

        document.documentElement.setAttribute("data-theme", theme);
    }
}