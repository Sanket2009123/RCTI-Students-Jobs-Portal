// ===============================
// Dashboard JavaScript
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.querySelector(".sidebar");
    const menuToggle = document.getElementById("menuToggle");

    // ==========================
    // Sidebar Toggle
    // ==========================

    if (menuToggle && sidebar) {

        menuToggle.addEventListener("click", function () {

            if (window.innerWidth <= 992) {

                sidebar.classList.toggle("show");

            } else {

                sidebar.classList.toggle("collapsed");

            }

        });

    }

    // ==========================
    // Close Sidebar on Mobile
    // ==========================

    document.addEventListener("click", function (e) {

        if (
            window.innerWidth <= 992 &&
            sidebar.classList.contains("show") &&
            !sidebar.contains(e.target) &&
            !menuToggle.contains(e.target)
        ) {

            sidebar.classList.remove("show");

        }

    });

    // ==========================
    // Active Menu
    // ==========================

    const currentPage = window.location.pathname;

    const menuLinks = document.querySelectorAll(".sidebar ul li a");

    menuLinks.forEach(link => {

        if (link.getAttribute("href") === currentPage) {

            link.classList.add("active");

        }

    });

});

// ===============================
// Counter Animation
// ===============================

const counters = document.querySelectorAll(".card-info h3");

counters.forEach(counter => {

    const target = Number(counter.innerText);

    let count = 0;

    const speed = target / 40;

    const updateCounter = () => {

        if (count < target) {

            count += speed;

            counter.innerText = Math.ceil(count);

            requestAnimationFrame(updateCounter);

        } else {

            counter.innerText = target;

        }

    };

    updateCounter();

});

// ===============================
// Monthly Job Chart
// ===============================

const jobChartCanvas = document.getElementById("jobChart");

if(jobChartCanvas){

new Chart(jobChartCanvas,{

type:'bar',

data:{

labels:["Jan","Feb","Mar","Apr","May","Jun"],

datasets:[{

label:"Jobs Posted",

data:[5,8,12,10,15,18],

backgroundColor:"#0f4cdb",

borderRadius:8

}]

},

options:{

responsive:true,

plugins:{

legend:{

display:false

}

}

}

});

}

// ===============================
// Status Chart
// ===============================

const statusChartCanvas = document.getElementById("statusChart");

if(statusChartCanvas){

new Chart(statusChartCanvas,{

type:'doughnut',

data:{

labels:["Selected","Pending","Rejected"],

datasets:[{

data:[35,40,25],

backgroundColor:[

"#28a745",

"#ff9800",

"#dc3545"

]

}]

},

options:{

responsive:true

}

});

}

// ===============================
// Dark Mode
// ===============================

const themeToggle = document.getElementById("themeToggle");

if(themeToggle){

    // Load saved theme
    if(localStorage.getItem("theme") === "dark"){

        document.body.classList.add("dark-mode");

        themeToggle.innerHTML =
        '<i class="fa-solid fa-sun"></i>';

    }

    themeToggle.addEventListener("click",function(){

        document.body.classList.toggle("dark-mode");

        if(document.body.classList.contains("dark-mode")){

            localStorage.setItem("theme","dark");

            themeToggle.innerHTML =
            '<i class="fa-solid fa-sun"></i>';

        }else{

            localStorage.setItem("theme","light");

            themeToggle.innerHTML =
            '<i class="fa-solid fa-moon"></i>';

        }

    });

}
const studentChart = document.getElementById("studentChart");

if (studentChart) {

    new Chart(studentChart, {

        type: "bar",

        data: {

            labels: ["Jan","Feb","Mar","Apr","May","Jun"],

            datasets: [{

                label: "Students",

                data: [25,40,32,55,70,60]

            }]

        }

    });

}

const jobChart = document.getElementById("jobChart");

if (jobChart) {

    new Chart(jobChart, {

        type: "line",

        data: {

            labels: ["Jan","Feb","Mar","Apr","May","Jun"],

            datasets: [{

                label: "Jobs",

                data: [5,8,12,15,18,20]

            }]

        }

    });

}