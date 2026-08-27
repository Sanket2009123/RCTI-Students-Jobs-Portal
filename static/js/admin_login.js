document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTS
       ===================================================== */

    const form =
        document.getElementById("adminLoginForm");

    const password =
        document.getElementById("adminPassword");

    const toggle =
        document.getElementById("toggleAdminPassword");

    const loginButton =
        document.getElementById("adminLoginButton");


    /* =====================================================
       PASSWORD SHOW / HIDE
       ===================================================== */

    if (password && toggle) {

        toggle.addEventListener("click", function () {

            const icon =
                toggle.querySelector("i");

            if (password.type === "password") {

                password.type = "text";

                icon.classList.remove(
                    "fa-eye"
                );

                icon.classList.add(
                    "fa-eye-slash"
                );

                toggle.setAttribute(
                    "aria-label",
                    "Hide password"
                );

                toggle.setAttribute(
                    "title",
                    "Hide password"
                );

            } else {

                password.type = "password";

                icon.classList.remove(
                    "fa-eye-slash"
                );

                icon.classList.add(
                    "fa-eye"
                );

                toggle.setAttribute(
                    "aria-label",
                    "Show password"
                );

                toggle.setAttribute(
                    "title",
                    "Show password"
                );

            }

        });

    }


    /* =====================================================
       LOGIN BUTTON LOADING
       ===================================================== */

    if (form && loginButton) {

        form.addEventListener(
            "submit",
            function (event) {

                if (!form.checkValidity()) {

                    event.preventDefault();

                    return;
                }

                loginButton.disabled = true;

                loginButton.innerHTML =
                    '<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>' +
                    '<span>Signing in...</span>';

            }
        );

    }


    /* =====================================================
       INPUT FOCUS EFFECT
       ===================================================== */

    const inputs =
        document.querySelectorAll(
            ".admin-login-page .admin-input"
        );


    inputs.forEach(function (input) {

        input.addEventListener(
            "focus",
            function () {

                const wrapper =
                    input.closest(
                        ".admin-input-wrapper"
                    );

                if (wrapper) {

                    wrapper.classList.add(
                        "admin-input-focused"
                    );

                }

            }
        );


        input.addEventListener(
            "blur",
            function () {

                const wrapper =
                    input.closest(
                        ".admin-input-wrapper"
                    );

                if (wrapper) {

                    wrapper.classList.remove(
                        "admin-input-focused"
                    );

                }

            }
        );

    });

});