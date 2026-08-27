/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   COMPANIES PAGE JAVASCRIPT
========================================================== */

document.addEventListener("DOMContentLoaded", function () {


    /* ======================================================
       ELEMENTS
    ====================================================== */

    const searchInput =
        document.getElementById("companySearch");

    const locationSelect =
        document.getElementById("companyLocation");

    const searchButton =
        document.getElementById("searchCompanyBtn");

    const clearButton =
        document.getElementById("clearSearch");

    const resetButton =
        document.getElementById("resetCompanySearch");

    const companyCount =
        document.getElementById("companyCount");

    const noResults =
        document.getElementById("noCompanies");

    const companyCards =
        document.querySelectorAll(".company-card");

    const popularButtons =
        document.querySelectorAll(
            ".popular-searches button"
        );

    const saveButtons =
        document.querySelectorAll(
            ".save-company"
        );


    /* ======================================================
       SAFETY CHECK
    ====================================================== */

    if (!searchInput || !companyCards.length) {

        return;

    }


    /* ======================================================
       FILTER COMPANIES
    ====================================================== */

    function filterCompanies() {

        const searchValue =
            searchInput.value
                .trim()
                .toLowerCase();

        const locationValue =
            locationSelect
                ? locationSelect.value
                    .trim()
                    .toLowerCase()
                : "";


        let visibleCompanies = 0;


        companyCards.forEach(function (card) {


            const companyName =
                (
                    card.dataset.company ||
                    card.querySelector("h3")?.textContent ||
                    ""
                )
                .toLowerCase();


            const companyLocation =
                (
                    card.dataset.location ||
                    card.querySelector(".company-location")
                        ?.textContent ||
                    ""
                )
                .toLowerCase();


            const matchesName =
                searchValue === "" ||
                companyName.includes(searchValue);


            const matchesLocation =
                locationValue === "" ||
                companyLocation.includes(locationValue);


            if (
                matchesName &&
                matchesLocation
            ) {

                card.style.display = "";

                visibleCompanies++;

            } else {

                card.style.display = "none";

            }

        });


        /* ==================================================
           UPDATE COMPANY COUNT
        ================================================== */

        if (companyCount) {

            companyCount.textContent =
                visibleCompanies;

        }


        /* ==================================================
           NO RESULT MESSAGE
        ================================================== */

        if (noResults) {

            if (visibleCompanies === 0) {

                noResults.classList.add("show");

            } else {

                noResults.classList.remove("show");

            }

        }


        /* ==================================================
           CLEAR BUTTON
        ================================================== */

        if (clearButton) {

            if (
                searchValue !== "" ||
                locationValue !== ""
            ) {

                clearButton.classList.add("show");

            } else {

                clearButton.classList.remove("show");

            }

        }

    }


    /* ======================================================
       SEARCH BUTTON
    ====================================================== */

    if (searchButton) {

        searchButton.addEventListener(
            "click",
            function () {

                filterCompanies();

            }
        );

    }


    /* ======================================================
       LIVE SEARCH
    ====================================================== */

    searchInput.addEventListener(
        "input",
        function () {

            filterCompanies();

        }
    );


    /* ======================================================
       ENTER KEY SEARCH
    ====================================================== */

    searchInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                filterCompanies();

            }

        }
    );


    /* ======================================================
       LOCATION FILTER
    ====================================================== */

    if (locationSelect) {

        locationSelect.addEventListener(
            "change",
            function () {

                filterCompanies();

            }
        );

    }


    /* ======================================================
       CLEAR SEARCH
    ====================================================== */

    if (clearButton) {

        clearButton.addEventListener(
            "click",
            function () {

                searchInput.value = "";


                if (locationSelect) {

                    locationSelect.value = "";

                }


                filterCompanies();

                searchInput.focus();

            }
        );

    }


    /* ======================================================
       RESET SEARCH
    ====================================================== */

    if (resetButton) {

        resetButton.addEventListener(
            "click",
            function () {

                searchInput.value = "";


                if (locationSelect) {

                    locationSelect.value = "";

                }


                filterCompanies();

                searchInput.focus();

            }
        );

    }


    /* ======================================================
       POPULAR SEARCH BUTTONS
    ====================================================== */

    popularButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const searchValue =
                        button.dataset.search || "";


                    searchInput.value =
                        searchValue;


                    filterCompanies();


                    searchInput.focus();

                }
            );

        }
    );


    /* ======================================================
       SAVE COMPANY BUTTON
    ====================================================== */

    saveButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const icon =
                        button.querySelector("i");


                    if (!icon) {

                        return;

                    }


                    const isSaved =
                        button.classList.contains(
                            "saved"
                        );


                    if (isSaved) {

                        button.classList.remove(
                            "saved"
                        );

                        icon.classList.remove(
                            "fa-solid"
                        );

                        icon.classList.add(
                            "fa-regular"
                        );

                    } else {

                        button.classList.add(
                            "saved"
                        );

                        icon.classList.remove(
                            "fa-regular"
                        );

                        icon.classList.add(
                            "fa-solid"
                        );

                    }

                }
            );

        }
    );


    /* ======================================================
       INITIAL LOAD
    ====================================================== */

    filterCompanies();

});