/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   STUDENT JOBS PAGE JAVASCRIPT
========================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* ==================================================
           ELEMENTS
        ================================================== */

        const searchForm =
            document.getElementById(
                "jobSearchForm"
            );


        const searchInput =
            document.getElementById(
                "jobSearchInput"
            );


        const clearSearch =
            document.getElementById(
                "clearJobSearch"
            );


        const locationSelect =
            document.getElementById(
                "jobLocation"
            );


        const jobTypeSelect =
            document.getElementById(
                "jobType"
            );


        const jobCards =
            document.querySelectorAll(
                ".job-card"
            );


        const popularButtons =
            document.querySelectorAll(
                ".popular-job-searches button"
            );


        const saveButtons =
            document.querySelectorAll(
                ".save-job"
            );



        /* ==================================================
           CLEAR SEARCH
        ================================================== */

        function updateClearButton() {

            if (!clearSearch || !searchInput) {

                return;

            }


            clearSearch.style.display =
                searchInput.value.trim()
                    ? "flex"
                    : "none";

        }


        if (clearSearch && searchInput) {

            clearSearch.addEventListener(
                "click",
                function () {

                    searchInput.value = "";

                    updateClearButton();

                    searchInput.focus();

                }
            );


            searchInput.addEventListener(
                "input",
                updateClearButton
            );


            updateClearButton();

        }



        /* ==================================================
           SEARCH FORM
        ================================================== */

        if (searchForm) {

            searchForm.addEventListener(
                "submit",
                function () {

                    if (searchInput) {

                        searchInput.value =
                            searchInput.value.trim();

                    }

                }
            );

        }



        /* ==================================================
           POPULAR SEARCHES
        ================================================== */

        popularButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const value =
                            button.dataset.search ||
                            "";


                        if (!searchInput) {

                            return;

                        }


                        searchInput.value =
                            value;


                        updateClearButton();


                        if (searchForm) {

                            searchForm.submit();

                        }

                    }
                );

            }
        );



        /* ==================================================
           SAVE JOB
        ================================================== */

        saveButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const icon =
                            button.querySelector(
                                "i"
                            );


                        if (!icon) {

                            return;

                        }


                        const saved =
                            button.classList.contains(
                                "saved"
                            );


                        if (saved) {

                            button.classList.remove(
                                "saved"
                            );


                            icon.classList.remove(
                                "fa-solid"
                            );


                            icon.classList.add(
                                "fa-regular"
                            );


                            button.setAttribute(
                                "aria-label",
                                "Save job"
                            );


                            button.setAttribute(
                                "title",
                                "Save job"
                            );

                        }

                        else {

                            button.classList.add(
                                "saved"
                            );


                            icon.classList.remove(
                                "fa-regular"
                            );


                            icon.classList.add(
                                "fa-solid"
                            );


                            button.setAttribute(
                                "aria-label",
                                "Remove saved job"
                            );


                            button.setAttribute(
                                "title",
                                "Remove saved job"
                            );

                        }

                    }
                );

            }
        );



        /* ==================================================
           CARD KEYBOARD ACCESSIBILITY
        ================================================== */

        jobCards.forEach(
            function (card) {

                card.addEventListener(
                    "focus",
                    function () {

                        card.classList.add(
                            "keyboard-focus"
                        );

                    }
                );


                card.addEventListener(
                    "blur",
                    function () {

                        card.classList.remove(
                            "keyboard-focus"
                        );

                    }
                );

            }
        );



        /* ==================================================
           "/" SEARCH SHORTCUT
        ================================================== */

        if (searchInput) {

            document.addEventListener(
                "keydown",
                function (event) {

                    if (
                        event.key === "/" &&
                        document.activeElement !==
                            searchInput
                    ) {

                        event.preventDefault();

                        searchInput.focus();

                    }

                }
            );

        }



        /* ==================================================
           FILTER STATE
        ================================================== */

        function updateFilterState(
            selectElement
        ) {

            if (!selectElement) {

                return;

            }


            if (selectElement.value) {

                selectElement.classList.add(
                    "filter-active"
                );

            }

            else {

                selectElement.classList.remove(
                    "filter-active"
                );

            }

        }



        if (locationSelect) {

            locationSelect.addEventListener(
                "change",
                function () {

                    updateFilterState(
                        locationSelect
                    );

                }
            );


            updateFilterState(
                locationSelect
            );

        }



        if (jobTypeSelect) {

            jobTypeSelect.addEventListener(
                "change",
                function () {

                    updateFilterState(
                        jobTypeSelect
                    );

                }
            );


            updateFilterState(
                jobTypeSelect
            );

        }



        /* ==================================================
           SEARCH LOADING STATE
        ================================================== */

        if (searchForm) {

            searchForm.addEventListener(
                "submit",
                function () {

                    const button =
                        searchForm.querySelector(
                            ".jobs-search-button"
                        );


                    if (!button) {

                        return;

                    }


                    button.classList.add(
                        "is-loading"
                    );


                    button.innerHTML =
                        `
                        <i class="fa-solid fa-spinner fa-spin"></i>
                        Searching...
                        `;

                }
            );

        }



        /* ==================================================
           PAGE READY
        ================================================== */

        document
            .querySelector(
                ".student-jobs-page"
            )
            ?.classList.add(
                "page-ready"
            );

    }
);