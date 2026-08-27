/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   STUDENT REGISTRATION JAVASCRIPT
   ========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");

    if (!form) {
        return;
    }


    /* ======================================================
       ELEMENTS
       ====================================================== */

    const firstname =
        document.getElementById("firstname");

    const lastname =
        document.getElementById("lastname");

    const email =
        document.getElementById("email");

    const mobile =
        document.getElementById("mobile");

    const college =
        document.getElementById("college");

    const branch =
        document.getElementById("branch");

    const semester =
        document.getElementById("semester");

    const skills =
        document.getElementById("skills");

    const password =
        document.getElementById("password");

    const confirmPassword =
        document.getElementById("confirmPassword");

    const terms =
        document.getElementById("terms");

    const registerButton =
        document.getElementById("registerButton");


    /* ======================================================
       MOBILE NUMBER
       ====================================================== */

    if (mobile) {

        mobile.addEventListener("input", function () {

            this.value =
                this.value.replace(/\D/g, "").slice(0, 10);

        });

    }


    /* ======================================================
       REMOVE ERROR WHEN USER TYPES
       ====================================================== */

    const fields = [
        firstname,
        lastname,
        email,
        mobile,
        college,
        branch,
        semester,
        skills,
        password,
        confirmPassword
    ];

    fields.forEach(function (field) {

        if (!field) {
            return;
        }

        field.addEventListener("input", function () {

            this.classList.remove("input-error");

        });

        field.addEventListener("change", function () {

            this.classList.remove("input-error");

        });

    });


    /* ======================================================
       PASSWORD LIVE CHECK
       ====================================================== */

    if (password && confirmPassword) {

        confirmPassword.addEventListener(
            "input",
            function () {

                if (
                    confirmPassword.value !== "" &&
                    password.value !== confirmPassword.value
                ) {

                    confirmPassword.classList.add(
                        "input-error"
                    );

                    confirmPassword.classList.remove(
                        "input-success"
                    );

                } else if (
                    confirmPassword.value !== "" &&
                    password.value === confirmPassword.value
                ) {

                    confirmPassword.classList.remove(
                        "input-error"
                    );

                    confirmPassword.classList.add(
                        "input-success"
                    );

                } else {

                    confirmPassword.classList.remove(
                        "input-error"
                    );

                    confirmPassword.classList.remove(
                        "input-success"
                    );
                }

            }
        );

    }


    /* ======================================================
       FORM SUBMIT VALIDATION
       ====================================================== */

    form.addEventListener("submit", function (e) {

        let valid = true;


        /* ----------------------------------------------
           FIRST NAME
           ---------------------------------------------- */

        if (
            firstname &&
            firstname.value.trim() === ""
        ) {

            firstname.classList.add("input-error");

            firstname.focus();

            alert("Please enter your First Name.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           LAST NAME
           ---------------------------------------------- */

        if (
            lastname &&
            lastname.value.trim() === ""
        ) {

            lastname.classList.add("input-error");

            lastname.focus();

            alert("Please enter your Last Name.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           EMAIL
           ---------------------------------------------- */

        if (email) {

            const emailPattern =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (
                !emailPattern.test(
                    email.value.trim()
                )
            ) {

                email.classList.add("input-error");

                email.focus();

                alert(
                    "Please enter a valid Email Address."
                );

                e.preventDefault();

                return;
            }

        }


        /* ----------------------------------------------
           MOBILE
           ---------------------------------------------- */

        if (mobile) {

            const mobilePattern =
                /^[0-9]{10}$/;

            if (
                !mobilePattern.test(
                    mobile.value.trim()
                )
            ) {

                mobile.classList.add("input-error");

                mobile.focus();

                alert(
                    "Mobile Number must contain exactly 10 digits."
                );

                e.preventDefault();

                return;
            }

        }


        /* ----------------------------------------------
           COLLEGE
           ---------------------------------------------- */

        if (
            college &&
            college.value.trim() === ""
        ) {

            college.classList.add("input-error");

            college.focus();

            alert("Please enter your College Name.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           BRANCH
           ---------------------------------------------- */

        if (
            branch &&
            branch.value.trim() === ""
        ) {

            branch.classList.add("input-error");

            branch.focus();

            alert("Please enter your Branch.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           SEMESTER
           ---------------------------------------------- */

        if (
            semester &&
            semester.value === ""
        ) {

            semester.classList.add("input-error");

            semester.focus();

            alert("Please select your Semester.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           SKILLS
           ---------------------------------------------- */

        if (
            skills &&
            skills.value.trim() === ""
        ) {

            skills.classList.add("input-error");

            skills.focus();

            alert("Please enter your Skills.");

            e.preventDefault();

            return;
        }


        /* ----------------------------------------------
           PASSWORD
           ---------------------------------------------- */

        if (password) {

            if (password.value.length < 6) {

                password.classList.add("input-error");

                password.focus();

                alert(
                    "Password must be at least 6 characters long."
                );

                e.preventDefault();

                return;
            }

        }


        /* ----------------------------------------------
           CONFIRM PASSWORD
           ---------------------------------------------- */

        if (password && confirmPassword) {

            if (
                password.value !==
                confirmPassword.value
            ) {

                confirmPassword.classList.add(
                    "input-error"
                );

                confirmPassword.focus();

                alert("Passwords do not match.");

                e.preventDefault();

                return;
            }

        }


        /* ----------------------------------------------
           TERMS
           ---------------------------------------------- */

        if (terms && !terms.checked) {

            alert(
                "Please agree to the Terms & Conditions."
            );

            e.preventDefault();

            terms.focus();

            return;
        }


        /* ----------------------------------------------
           SUBMIT BUTTON LOADING
           ---------------------------------------------- */

        if (registerButton) {

            registerButton.disabled = true;

            registerButton.innerHTML =
                `
                <span class="button-content">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    <span>Creating Account...</span>
                </span>
                `;

        }

    });


    /* ======================================================
       BROWSER VALIDATION
       ====================================================== */

    form.addEventListener("invalid", function (event) {

        event.target.classList.add("input-error");

    }, true);

});


/* ==========================================================
   SHOW / HIDE PASSWORD
   ========================================================== */

function togglePassword(inputId, button) {

    const password =
        document.getElementById(inputId);

    if (!password || !button) {
        return;
    }

    const icon =
        button.querySelector("i");

    if (!icon) {
        return;
    }


    /* SHOW PASSWORD */

    if (password.type === "password") {

        password.type = "text";

        icon.classList.remove("fa-eye");

        icon.classList.add("fa-eye-slash");

        button.setAttribute(
            "aria-label",
            "Hide password"
        );


    /* HIDE PASSWORD */

    } else {

        password.type = "password";

        icon.classList.remove("fa-eye-slash");

        icon.classList.add("fa-eye");

        button.setAttribute(
            "aria-label",
            "Show password"
        );

    }

}