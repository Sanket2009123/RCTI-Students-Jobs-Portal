// ==========================================
// NAVBAR SCROLL EFFECT
// ==========================================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 80) {

        navbar.style.background = "#111";

        navbar.style.padding = "10px 0";

        navbar.style.boxShadow = "0 5px 20px rgba(0,0,0,.25)";

    } else {

        navbar.style.background = "rgba(0,0,0,.15)";

        navbar.style.padding = "15px 0";

        navbar.style.boxShadow = "none";

    }

});



// ==========================================
// COUNTER ANIMATION
// ==========================================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const updateCounter = () => {

        const target = parseInt(counter.innerText);

        const count = +counter.getAttribute("data-count") || 0;

        const speed = Math.ceil(target / 80);

        if (count < target) {

            counter.setAttribute("data-count", count + speed);

            counter.innerText = Math.min(count + speed, target) + "+";

            setTimeout(updateCounter, 30);

        }

    };

    updateCounter();

});



// ==========================================
// SMOOTH SCROLL
// ==========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
            .scrollIntoView({

                behavior: "smooth"

            });

    });

});



// ==========================================
// CARD HOVER EFFECT
// ==========================================

const cards = document.querySelectorAll(

".job-card,.category-card,.company-card,.feature-card,.testimonial-card,.stat-card"

);

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-10px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});



// ==========================================
// HERO BUTTON RIPPLE
// ==========================================

document.querySelectorAll(".btn").forEach(button => {

    button.addEventListener("click", function (e) {

        let x = e.clientX - e.target.offsetLeft;

        let y = e.clientY - e.target.offsetTop;

        let ripple = document.createElement("span");

        ripple.style.left = x + "px";

        ripple.style.top = y + "px";

        ripple.classList.add("ripple");

        this.appendChild(ripple);

        setTimeout(() => {

            ripple.remove();

        }, 600);

    });

});



// ==========================================
// SCROLL REVEAL
// ==========================================

const reveal = () => {

    const reveals = document.querySelectorAll(

        ".stat-card,.category-card,.job-card,.company-card,.feature-card,.testimonial-card"

    );

    reveals.forEach(item => {

        const windowHeight = window.innerHeight;

        const revealTop = item.getBoundingClientRect().top;

        const revealPoint = 120;

        if (revealTop < windowHeight - revealPoint) {

            item.classList.add("active");

        }

    });

};

window.addEventListener("scroll", reveal);

reveal();



// ==========================================
// PAGE LOADER
// ==========================================

window.onload = function () {

    document.body.classList.add("loaded");

};



// ==========================================
// CURRENT YEAR
// ==========================================

const year = document.getElementById("year");

if (year) {

    year.innerHTML = new Date().getFullYear();

}