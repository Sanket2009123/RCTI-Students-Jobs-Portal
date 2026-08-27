/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   STUDENT DASHBOARD JAVASCRIPT
========================================================== */


document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* ==================================================
           ELEMENTS
        ================================================== */

        const refreshButton =
            document.getElementById(
                "quickRefresh"
            );


        const statNumbers =
            document.querySelectorAll(
                ".stat-number"
            );


        const progressBars =
            document.querySelectorAll(
                ".progress-fill"
            );


        /* ==================================================
           REFRESH BUTTON
        ================================================== */

        if (refreshButton) {

            refreshButton.addEventListener(
                "click",
                function () {

                    const icon =
                        refreshButton.querySelector(
                            "i"
                        );


                    refreshButton.disabled =
                        true;


                    if (icon) {

                        icon.classList.add(
                            "fa-spin"
                        );

                    }


                    /*
                     * Small visual refresh effect.
                     * After animation the current page
                     * is reloaded so dashboard data is
                     * fetched again from Flask.
                     */

                    setTimeout(
                        function () {

                            window.location.reload();

                        },
                        500
                    );

                }
            );

        }


        /* ==================================================
           STAT NUMBER ANIMATION
        ================================================== */

        statNumbers.forEach(
            function (element) {

                const target =
                    parseInt(
                        element.dataset.value,
                        10
                    );


                if (
                    Number.isNaN(target) ||
                    target < 0
                ) {

                    return;

                }


                let current = 0;


                const duration = 650;

                const stepTime =
                    Math.max(
                        20,
                        Math.floor(
                            duration /
                            Math.max(
                                target,
                                1
                            )
                        )
                    );


                /*
                 * Avoid unnecessary animation
                 * for very large values.
                 */

                if (target > 1000) {

                    element.textContent =
                        target.toLocaleString();

                    return;

                }


                const counter =
                    setInterval(
                        function () {

                            current += 1;


                            element.textContent =
                                current;


                            if (
                                current >= target
                            ) {

                                clearInterval(
                                    counter
                                );

                                element.textContent =
                                    target;

                            }

                        },
                        stepTime
                    );

            }
        );


        /* ==================================================
           APPLICATION PROGRESS
        ================================================== */

        progressBars.forEach(
            function (bar) {

                const applications =
                    parseInt(
                        bar.dataset.progress,
                        10
                    );


                if (
                    Number.isNaN(
                        applications
                    )
                ) {

                    return;

                }


                /*
                 * Dashboard visual indicator.
                 * It is intentionally capped so a large
                 * application count doesn't overflow.
                 */

                const percentage =
                    Math.min(
                        Math.max(
                            applications * 10,
                            applications > 0
                                ? 10
                                : 0
                        ),
                        100
                    );


                setTimeout(
                    function () {

                        bar.style.width =
                            percentage + "%";

                    },
                    250
                );

            }
        );


        /* ==================================================
           QUICK ACTION HOVER
        ================================================== */

        const quickActions =
            document.querySelectorAll(
                ".quick-action"
            );


        quickActions.forEach(
            function (action) {

                action.addEventListener(
                    "mouseenter",
                    function () {

                        action.classList.add(
                            "is-hovered"
                        );

                    }
                );


                action.addEventListener(
                    "mouseleave",
                    function () {

                        action.classList.remove(
                            "is-hovered"
                        );

                    }
                );

            }
        );


        /* ==================================================
           CURRENT TIME / PAGE READY
        ================================================== */

        document.body.classList.add(
            "dashboard-ready"
        );


    }
);