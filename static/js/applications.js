/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   MY APPLICATIONS JAVASCRIPT
========================================================== */


document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* ==================================================
           ELEMENTS
        ================================================== */

        const searchInput =
            document.getElementById(
                "applicationSearch"
            );


        const clearSearchButton =
            document.getElementById(
                "clearApplicationSearch"
            );


        const statusFilter =
            document.getElementById(
                "applicationStatusFilter"
            );


        const applicationCards =
            document.querySelectorAll(
                ".application-card"
            );


        const visibleCount =
            document.getElementById(
                "visibleApplicationCount"
            );


        const filterEmptyState =
            document.getElementById(
                "filterEmptyState"
            );


        const resetFilters =
            document.getElementById(
                "resetApplicationFilters"
            );


        /* ==================================================
           COUNT APPLICATION STATUS
        ================================================== */

        function updateStatusCounters() {

            const statusCounters =
                document.querySelectorAll(
                    ".status-counter"
                );


            statusCounters.forEach(
                function (counter) {

                    const targetStatus =
                        counter.dataset.status;


                    let count = 0;


                    applicationCards.forEach(
                        function (card) {

                            const cardStatus =
                                card.dataset.status;


                            if (
                                cardStatus ===
                                targetStatus
                            ) {

                                count++;

                            }

                        }
                    );


                    counter.textContent =
                        count;

                }
            );

        }


        updateStatusCounters();



        /* ==================================================
           SEARCH CLEAR BUTTON
        ================================================== */

        function updateClearButton() {

            if (!clearSearchButton) {

                return;

            }


            if (
                searchInput &&
                searchInput.value.trim()
            ) {

                clearSearchButton.style.display =
                    "flex";

            }

            else {

                clearSearchButton.style.display =
                    "none";

            }

        }


        if (searchInput) {

            searchInput.addEventListener(
                "input",
                function () {

                    updateClearButton();

                    filterApplications();

                }
            );

        }


        if (clearSearchButton) {

            clearSearchButton.addEventListener(
                "click",
                function () {

                    if (searchInput) {

                        searchInput.value = "";

                        searchInput.focus();

                    }


                    updateClearButton();

                    filterApplications();

                }
            );

        }



        /* ==================================================
           FILTER APPLICATIONS
        ================================================== */

        function filterApplications() {

            const searchTerm =
                searchInput
                    ? searchInput.value
                        .trim()
                        .toLowerCase()
                    : "";


            const selectedStatus =
                statusFilter
                    ? statusFilter.value
                    : "all";


            let visibleApplications = 0;


            applicationCards.forEach(
                function (card) {

                    const company =
                        card.dataset.company || "";


                    const title =
                        card.dataset.title || "";


                    const location =
                        card.dataset.location || "";


                    const status =
                        card.dataset.status || "";


                    const matchesSearch =
                        !searchTerm ||
                        company.includes(
                            searchTerm
                        ) ||
                        title.includes(
                            searchTerm
                        ) ||
                        location.includes(
                            searchTerm
                        );


                    const matchesStatus =
                        selectedStatus ===
                            "all" ||
                        status ===
                            selectedStatus;


                    if (
                        matchesSearch &&
                        matchesStatus
                    ) {

                        card.style.display =
                            "";


                        visibleApplications++;

                    }

                    else {

                        card.style.display =
                            "none";

                    }

                }
            );


            /* ==============================================
               UPDATE VISIBLE COUNT
            ============================================== */

            if (visibleCount) {

                visibleCount.textContent =
                    visibleApplications;

            }


            /* ==============================================
               FILTER EMPTY STATE
            ============================================== */

            if (filterEmptyState) {

                if (
                    visibleApplications === 0 &&
                    applicationCards.length > 0
                ) {

                    filterEmptyState.style.display =
                        "block";

                }

                else {

                    filterEmptyState.style.display =
                        "none";

                }

            }

        }



        /* ==================================================
           STATUS FILTER
        ================================================== */

        if (statusFilter) {

            statusFilter.addEventListener(
                "change",
                function () {

                    filterApplications();

                }
            );

        }



        /* ==================================================
           RESET FILTERS
        ================================================== */

        if (resetFilters) {

            resetFilters.addEventListener(
                "click",
                function () {

                    if (searchInput) {

                        searchInput.value = "";

                    }


                    if (statusFilter) {

                        statusFilter.value =
                            "all";

                    }


                    updateClearButton();

                    filterApplications();

                }
            );

        }



        /* ==================================================
           KEYBOARD SEARCH SHORTCUT
        ================================================== */

        document.addEventListener(
            "keydown",
            function (event) {

                /*
                 * Press "/" to focus application search.
                 */

                if (
                    event.key === "/" &&
                    searchInput &&
                    document.activeElement !==
                        searchInput
                ) {

                    event.preventDefault();

                    searchInput.focus();

                }


                /*
                 * Press Escape to clear search.
                 */

                if (
                    event.key === "Escape" &&
                    searchInput &&
                    document.activeElement ===
                        searchInput
                ) {

                    searchInput.value = "";

                    updateClearButton();

                    filterApplications();

                }

            }
        );



        /* ==================================================
           CARD HOVER / FOCUS
        ================================================== */

        applicationCards.forEach(
            function (card) {

                card.addEventListener(
                    "focusin",
                    function () {

                        card.classList.add(
                            "keyboard-focus"
                        );

                    }
                );


                card.addEventListener(
                    "focusout",
                    function () {

                        card.classList.remove(
                            "keyboard-focus"
                        );

                    }
                );

            }
        );



        /* ==================================================
           COUNTER ANIMATION
        ================================================== */

        const counters =
            document.querySelectorAll(
                ".counter, .status-counter"
            );


        counters.forEach(
            function (counter) {

                const target =
                    parseInt(
                        counter.textContent,
                        10
                    );


                if (
                    Number.isNaN(target) ||
                    target === 0
                ) {

                    counter.textContent = "0";

                    return;

                }


                let current = 0;


                const duration = 600;


                const step =
                    Math.max(
                        20,
                        Math.floor(
                            duration / target
                        )
                    );


                const timer =
                    setInterval(
                        function () {

                            current++;

                            counter.textContent =
                                current;


                            if (
                                current >= target
                            ) {

                                clearInterval(timer);

                                counter.textContent =
                                    target;

                            }

                        },
                        step
                    );

            }
        );



        /* ==================================================
           INITIALIZE
        ================================================== */

        updateClearButton();

        filterApplications();


        const page =
            document.querySelector(
                ".applications-page"
            );


        if (page) {

            page.classList.add(
                "page-ready"
            );

        }

    }
);