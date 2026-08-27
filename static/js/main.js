document.addEventListener("DOMContentLoaded", function () {

    /* ===============================
       MOBILE NAVBAR
    =============================== */

    const menu = document.querySelector("#mobileMenuToggle");
    const nav = document.querySelector(".nav-links");

    if (menu && nav) {

        menu.addEventListener("click", function () {

            nav.classList.toggle("show");

            const isOpen = nav.classList.contains("show");

            menu.setAttribute(
                "aria-expanded",
                isOpen ? "true" : "false"
            );

            const icon = menu.querySelector("i");

            if (icon) {

                if (isOpen) {

                    icon.classList.remove("fa-bars");
                    icon.classList.add("fa-xmark");

                } else {

                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");

                }

            }

        });


        /* Close menu after clicking link */

        nav.querySelectorAll("a").forEach(function (link) {

            link.addEventListener("click", function () {

                nav.classList.remove("show");

                menu.setAttribute(
                    "aria-expanded",
                    "false"
                );

                const icon = menu.querySelector("i");

                if (icon) {

                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");

                }

            });

        });

    }


    /* ===============================
       NAVBAR SCROLL EFFECT
    =============================== */

    const navbar = document.querySelector(".navbar");

    if (navbar) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 20) {

                navbar.classList.add("scrolled");

            } else {

                navbar.classList.remove("scrolled");

            }

        });

    }

});
/* ==========================================================
   DASHBOARD MOBILE MENU
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const menuButton =
        document.getElementById("dashboardMenuBtn");

    const sidebar =
        document.querySelector(".sidebar, .admin-sidebar");


    /* Stop if this is not a dashboard page */

    if (!menuButton || !sidebar) {
        return;
    }


    /* ===============================
       OPEN / CLOSE SIDEBAR
    =============================== */

    menuButton.addEventListener("click", function () {

        sidebar.classList.toggle("active");

        const isOpen =
            sidebar.classList.contains("active");


        menuButton.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );


        /* Change hamburger icon */

        const icon =
            menuButton.querySelector("i");

        if (icon) {

            if (isOpen) {

                icon.classList.remove("fa-bars");
                icon.classList.add("fa-xmark");

            } else {

                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");

            }

        }

    });


    /* ===============================
       CLOSE SIDEBAR AFTER LINK CLICK
    =============================== */

    sidebar.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 992) {

                sidebar.classList.remove("active");


                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );


                const icon =
                    menuButton.querySelector("i");

                if (icon) {

                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");

                }

            }

        });

    });

});