document.addEventListener("DOMContentLoaded", function () {

    // =========================================================
    // DATA FROM FLASK / SQLITE
    // =========================================================

    const categories = window.categories || [];
    const categoryCount = window.categoryCount || [];

    const analyticsDates = window.analyticsDates || [];
    const studentCounts = window.studentCounts || [];
    const companyCounts = window.companyCounts || [];
    const jobCounts = window.jobCounts || [];
    const applicationCounts = window.applicationCounts || [];


    // =========================================================
    // JOB CATEGORY CHART
    // =========================================================

    const categoryCanvas = document.getElementById("categoryChart");

    if (categoryCanvas) {

        let categoryChart;

        function createCategoryChart(type = "bar") {

            if (categoryChart) {
                categoryChart.destroy();
            }

            categoryChart = new Chart(categoryCanvas, {
                type: type,

                data: {
                    labels: categories,

                    datasets: [{
                        label: "Jobs",
                        data: categoryCount,

                        borderWidth: 2,

                        backgroundColor: [
                            "rgba(59, 130, 246, 0.75)",
                            "rgba(16, 185, 129, 0.75)",
                            "rgba(245, 158, 11, 0.75)",
                            "rgba(239, 68, 68, 0.75)",
                            "rgba(139, 92, 246, 0.75)",
                            "rgba(14, 165, 233, 0.75)"
                        ],

                        borderColor: [
                            "#3b82f6",
                            "#10b981",
                            "#f59e0b",
                            "#ef4444",
                            "#8b5cf6",
                            "#0ea5e9"
                        ]
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: type === "pie" || type === "doughnut"
                        }
                    },

                    scales: {
                        y: {
                            beginAtZero: true,

                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        }

        createCategoryChart("bar");


        // Chart type selector
        const chartTypeSelect =
            document.getElementById("chartTypeSelect");

        if (chartTypeSelect) {

            chartTypeSelect.addEventListener("change", function () {

                createCategoryChart(this.value);

            });
        }
    }


    // =========================================================
    // ANALYTICS CHART
    // =========================================================

    const analyticsCanvas =
        document.getElementById("analyticsChart");

    if (analyticsCanvas) {

        let analyticsChart;

        function prepareAnalytics(period) {

            const grouped = {};

            for (let i = 0; i < analyticsDates.length; i++) {

                const date = new Date(analyticsDates[i]);

                let key;

                // -------------------------
                // DAY
                // -------------------------

                if (period === "day") {

                    key = analyticsDates[i];
                }


                // -------------------------
                // WEEK
                // -------------------------

                else if (period === "week") {

                    const firstDay =
                        new Date(date);

                    const day =
                        firstDay.getDay();

                    const difference =
                        firstDay.getDate() - day;

                    firstDay.setDate(difference);

                    key =
                        firstDay.toISOString()
                            .split("T")[0];
                }


                // -------------------------
                // MONTH
                // -------------------------

                else if (period === "month") {

                    key =
                        date.getFullYear() +
                        "-" +
                        String(date.getMonth() + 1)
                            .padStart(2, "0");
                }


                // -------------------------
                // YEAR
                // -------------------------

                else if (period === "year") {

                    key =
                        String(date.getFullYear());
                }

                if (!grouped[key]) {
                    grouped[key] = i;
                }
            }

            return Object.keys(grouped);
        }


        function aggregateData(period, dates, values) {

            const result = {};

            for (let i = 0; i < dates.length; i++) {

                const date =
                    new Date(dates[i]);

                let key;

                if (period === "day") {

                    key = dates[i];

                } else if (period === "week") {

                    const weekStart =
                        new Date(date);

                    const day =
                        weekStart.getDay();

                    weekStart.setDate(
                        weekStart.getDate() - day
                    );

                    key =
                        weekStart
                            .toISOString()
                            .split("T")[0];

                } else if (period === "month") {

                    key =
                        date.getFullYear() +
                        "-" +
                        String(date.getMonth() + 1)
                            .padStart(2, "0");

                } else {

                    key =
                        String(date.getFullYear());
                }

                if (!result[key]) {
                    result[key] = 0;
                }

                result[key] += Number(values[i] || 0);
            }

            return result;
        }


        function createAnalyticsChart(period = "month") {

            if (analyticsChart) {
                analyticsChart.destroy();
            }

            const studentData =
                aggregateData(
                    period,
                    analyticsDates,
                    studentCounts
                );

            const companyData =
                aggregateData(
                    period,
                    analyticsDates,
                    companyCounts
                );

            const jobData =
                aggregateData(
                    period,
                    analyticsDates,
                    jobCounts
                );

            const applicationData =
                aggregateData(
                    period,
                    analyticsDates,
                    applicationCounts
                );

            const labels =
                Object.keys(studentData);


            analyticsChart = new Chart(
                analyticsCanvas,
                {
                    type: "line",

                    data: {

                        labels: labels,

                        datasets: [

                            {
                                label: "Students",
                                data: labels.map(
                                    x => studentData[x] || 0
                                ),
                                borderWidth: 3,
                                tension: 0.35,
                                fill: false
                            },

                            {
                                label: "Companies",
                                data: labels.map(
                                    x => companyData[x] || 0
                                ),
                                borderWidth: 3,
                                tension: 0.35,
                                fill: false
                            },

                            {
                                label: "Jobs",
                                data: labels.map(
                                    x => jobData[x] || 0
                                ),
                                borderWidth: 3,
                                tension: 0.35,
                                fill: false
                            },

                            {
                                label: "Applications",
                                data: labels.map(
                                    x => applicationData[x] || 0
                                ),
                                borderWidth: 3,
                                tension: 0.35,
                                fill: false
                            }
                        ]
                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        interaction: {
                            intersect: false,
                            mode: "index"
                        },

                        plugins: {

                            legend: {
                                position: "bottom"
                            }

                        },

                        scales: {

                            y: {

                                beginAtZero: true,

                                ticks: {
                                    precision: 0
                                }

                            }

                        }

                    }
                }
            );
        }


        createAnalyticsChart("month");


        const analyticsPeriod =
            document.getElementById(
                "analyticsPeriod"
            );

        if (analyticsPeriod) {

            analyticsPeriod.addEventListener(
                "change",
                function () {

                    createAnalyticsChart(
                        this.value
                    );

                }
            );
        }
    }

});