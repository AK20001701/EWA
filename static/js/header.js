function onProfileClick() {
        let dropdown = document.getElementById("user__dropdown");

        let closedMenu = document.getElementById("header__closed__menu");
        let openedMenu = document.getElementById("header__opened__menu");

        if (dropdown.style.display === "none") {
            dropdown.style.display = "flex"
            closedMenu.style.display = "none";
            openedMenu.style.display = "block";
        } else {
            dropdown.style.display = "none"
            closedMenu.style.display = "block";
            openedMenu.style.display = "none";
        }
    }

    function onMenuClick() {
        let menu = document.getElementById("right__part");
        if (menu.style.display === "none") {
            menu.style.display = "flex"
        } else {
            menu.style.display = "none"
        }

        let burger = document.getElementById("menu__burger");
        let x = document.getElementById("menu__x");

        if (burger.style.display === "block") {
            burger.style.display = "none"
            x.style.display = "block"
        } else {
            burger.style.display = "block"
            x.style.display = "none"
        }

    }