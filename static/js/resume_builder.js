/* ==========================================================
   RCTI STUDENTS JOBS PORTAL
   RESUME BUILDER - FINAL JAVASCRIPT
   ========================================================== */

"use strict";

document.addEventListener("DOMContentLoaded", function () {

    console.log("RCTI Resume Builder loaded.");

    /* ======================================================
       ELEMENT HELPERS
       ====================================================== */

    const $ = (selector, parent = document) =>
        parent.querySelector(selector);

    const $$ = (selector, parent = document) =>
        Array.from(parent.querySelectorAll(selector));

    const byId = (id) =>
        document.getElementById(id);


    /* ======================================================
       BASIC HELPERS
       ====================================================== */

    function escapeHTML(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    function getValue(id) {
        const element = byId(id);

        if (!element) {
            return "";
        }

        return element.value.trim();
    }


    function getValues(name) {
        return $$(`[name="${name}"]`)
            .map(element => element.value.trim())
            .filter(Boolean);
    }


    function normalizeTemplate(template) {

        const allowed = [
            "ats",
            "modern",
            "executive",
            "creative",
            "developer",
            "data",
            "minimal",
            "fresher"
        ];

        template = String(template || "ats")
            .toLowerCase()
            .trim();

        return allowed.includes(template)
            ? template
            : "ats";
    }


    function getTemplateLabel(template) {

        const labels = {
            ats: "ATS Professional",
            modern: "Modern",
            executive: "Executive",
            creative: "Creative",
            developer: "Developer",
            data: "Data Analyst",
            minimal: "Minimal",
            fresher: "Fresher"
        };

        return labels[normalizeTemplate(template)];
    }


    /* ======================================================
       TEMPLATE SELECTION
       ====================================================== */

    const templateSelect = byId("templateSelect");
    const templateGallery = byId("templateGallery");
    const resumePreview = byId("resumePreview");

    const selectedTemplateName =
        byId("selectedTemplateName");

    const previewTemplateName =
        byId("previewTemplateName");


    function applyTemplate(template, scrollToPreview = false) {

        template = normalizeTemplate(template);

        /* Select dropdown */
        if (templateSelect) {
            templateSelect.value = template;
        }


        /* Remove selected state */
        $$(".template-card").forEach(card => {

            const cardTemplate =
                normalizeTemplate(card.dataset.template);

            card.classList.toggle(
                "is-selected",
                cardTemplate === template
            );
        });


        /* Update selected template information */
        if (selectedTemplateName) {
            selectedTemplateName.textContent =
                getTemplateLabel(template);
        }


        if (previewTemplateName) {
            previewTemplateName.textContent =
                getTemplateLabel(template);
        }


        /* Apply template to preview */
        if (resumePreview) {

            resumePreview.dataset.template =
                template;

            resumePreview.classList.remove(
                "template-ats",
                "template-modern",
                "template-executive",
                "template-creative",
                "template-developer",
                "template-data",
                "template-minimal",
                "template-fresher"
            );

            resumePreview.classList.add(
                `template-${template}`
            );
        }


        /* Save selected template locally */
        try {
            localStorage.setItem(
                "rcti_resume_template",
                template
            );
        } catch (error) {
            console.warn(
                "Could not save template.",
                error
            );
        }


        updatePreview();


        if (scrollToPreview && resumePreview) {

            setTimeout(() => {

                resumePreview.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });

            }, 120);
        }
    }


    /* ======================================================
       LOAD SAVED TEMPLATE
       ====================================================== */

    function loadSavedTemplate() {

        let template = "ats";

        try {

            const saved =
                localStorage.getItem(
                    "rcti_resume_template"
                );

            if (saved) {
                template = normalizeTemplate(saved);
            }

        } catch (error) {
            console.warn(
                "Could not load saved template.",
                error
            );
        }


        /* Existing server-selected template has priority */
        if (
            templateSelect &&
            templateSelect.value
        ) {
            template =
                normalizeTemplate(
                    templateSelect.value
                );
        }


        applyTemplate(template, false);
    }


    /* ======================================================
       TEMPLATE CLICK EVENTS
       ====================================================== */

    if (templateGallery) {

        templateGallery.addEventListener(
            "click",
            function (event) {

                const previewButton =
                    event.target.closest(
                        ".template-preview-btn"
                    );

                if (previewButton) {

                    event.preventDefault();
                    event.stopPropagation();

                    const template =
                        previewButton.dataset.template;

                    applyTemplate(
                        template,
                        true
                    );

                    return;
                }


                const useButton =
                    event.target.closest(
                        ".template-use-btn"
                    );

                if (useButton) {

                    event.preventDefault();
                    event.stopPropagation();

                    const template =
                        useButton.dataset.template;

                    applyTemplate(
                        template,
                        false
                    );

                    /* Visual feedback */
                    useButton.classList.add(
                        "template-used"
                    );

                    setTimeout(() => {
                        useButton.classList.remove(
                            "template-used"
                        );
                    }, 700);

                    return;
                }


                /* Card click */
                const card =
                    event.target.closest(
                        ".template-card"
                    );

                if (card) {

                    const template =
                        card.dataset.template;

                    applyTemplate(
                        template,
                        false
                    );
                }

            }
        );
    }


    /* ======================================================
       TEMPLATE FILTERS
       ====================================================== */

    $$(".template-filter").forEach(button => {

        button.addEventListener(
            "click",
            function () {

                $$(".template-filter").forEach(
                    item =>
                        item.classList.remove("active")
                );

                this.classList.add("active");

                const filter =
                    this.dataset.filter || "all";


                $$(".template-card").forEach(
                    card => {

                        const categories =
                            (
                                card.dataset.category ||
                                ""
                            ).toLowerCase();

                        const template =
                            (
                                card.dataset.template ||
                                ""
                            ).toLowerCase();

                        if (filter === "all") {

                            card.style.display = "";

                        } else {

                            const matches =
                                categories
                                    .split(/\s+/)
                                    .includes(filter) ||
                                template === filter;

                            card.style.display =
                                matches ? "" : "none";
                        }

                    }
                );

            }
        );

    });


    /* ======================================================
       DROPDOWN CHANGE
       ====================================================== */

    if (templateSelect) {

        templateSelect.addEventListener(
            "change",
            function () {

                applyTemplate(
                    this.value,
                    false
                );

            }
        );
    }


    /* ======================================================
       PERSONAL DETAILS PREVIEW
       ====================================================== */

    function updatePersonalPreview() {

        const fullName =
            getValue("fullname") ||
            "Your Name";

        const email =
            getValue("email") ||
            "your@email.com";

        const mobile =
            getValue("mobile") ||
            "Your mobile number";

        const address =
            getValue("address") ||
            "City, State";

        const branch =
            getValue("branch");

        const previewName =
            byId("previewFullName");

        const previewEmail =
            byId("previewEmail");

        const previewMobile =
            byId("previewMobile");

        const previewAddress =
            byId("previewAddress");

        const previewJobTitle =
            byId("previewJobTitle");


        if (previewName) {
            previewName.textContent =
                fullName;
        }


        if (previewEmail) {

            previewEmail.innerHTML =
                `<i class="fas fa-envelope"></i> ${
                    escapeHTML(email)
                }`;
        }


        if (previewMobile) {

            previewMobile.innerHTML =
                `<i class="fas fa-phone"></i> ${
                    escapeHTML(mobile)
                }`;
        }


        if (previewAddress) {

            previewAddress.innerHTML =
                `<i class="fas fa-location-dot"></i> ${
                    escapeHTML(address)
                }`;
        }


        if (previewJobTitle) {

            previewJobTitle.textContent =
                branch || "Professional Title";
        }
    }


    /* ======================================================
       SOCIAL LINKS
       ====================================================== */

    function updateSocialLinks() {

        const linkedin =
            $('[name="linkedin"]');

        const github =
            $('[name="github"]');

        const portfolio =
            $('[name="portfolio"]');


        const previewLinkedIn =
            byId("previewLinkedIn");

        const previewGitHub =
            byId("previewGitHub");

        const previewPortfolio =
            byId("previewPortfolio");

        const previewLinksRow =
            byId("previewLinksRow");


        function updateLink(
            input,
            preview
        ) {

            if (!input || !preview) {
                return false;
            }

            const value =
                input.value.trim();

            if (!value) {

                preview.hidden = true;
                preview.removeAttribute("href");

                return false;
            }


            preview.hidden = false;

            preview.href = value;

            return true;
        }


        const hasLinkedIn =
            updateLink(
                linkedin,
                previewLinkedIn
            );

        const hasGitHub =
            updateLink(
                github,
                previewGitHub
            );

        const hasPortfolio =
            updateLink(
                portfolio,
                previewPortfolio
            );


        if (previewLinksRow) {

            previewLinksRow.hidden =
                !(
                    hasLinkedIn ||
                    hasGitHub ||
                    hasPortfolio
                );
        }
    }


    /* ======================================================
       OBJECTIVE
       ====================================================== */

    function updateObjectivePreview() {

        const objective =
            getValue("objective");

        const section =
            byId("previewObjectiveSection");

        const preview =
            byId("previewObjective");


        if (!section || !preview) {
            return;
        }


        if (objective) {

            section.hidden = false;

            preview.textContent =
                objective;

        } else {

            section.hidden = false;

            preview.textContent =
                "Write your career objective...";
        }
    }


    /* ======================================================
       EDUCATION
       ====================================================== */

    function updateEducationPreview() {

        const container =
            byId("previewEducation");

        const section =
            byId("previewEducationSection");

        if (!container || !section) {
            return;
        }


        const degrees =
            getValues("education_degree[]");

        const colleges =
            getValues("education_college[]");

        const years =
            getValues("education_year[]");

        const cgpas =
            getValues("education_cgpa[]");


        const max =
            Math.max(
                degrees.length,
                colleges.length,
                years.length,
                cgpas.length
            );


        if (!max) {

            container.innerHTML =
                `<div class="preview-empty">
                    No education added yet.
                 </div>`;

            return;
        }


        let html = "";


        for (let i = 0; i < max; i++) {

            const degree =
                degrees[i] || "";

            const college =
                colleges[i] || "";

            const year =
                years[i] || "";

            const cgpa =
                cgpas[i] || "";


            if (
                !degree &&
                !college &&
                !year &&
                !cgpa
            ) {
                continue;
            }


            html += `
                <div class="preview-education-item">

                    <div class="preview-education-degree">
                        ${escapeHTML(
                            degree ||
                            "Education"
                        )}
                    </div>

                    <div class="preview-education-college">
                        ${escapeHTML(
                            college
                        )}
                    </div>

                    <div class="preview-education-meta">
                        ${
                            escapeHTML(year)
                        }
                        ${
                            year && cgpa
                                ? " • "
                                : ""
                        }
                        ${
                            escapeHTML(cgpa)
                        }
                    </div>

                </div>
            `;
        }


        container.innerHTML =
            html ||
            `<div class="preview-empty">
                No education added yet.
             </div>`;
    }


    /* ======================================================
       SKILLS
       ====================================================== */

    function updateSkillsPreview() {

        const container =
            byId("previewSkills");

        if (!container) {
            return;
        }


        const skillsText =
            getValue("skills");


        const skills =
            skillsText
                .split(",")
                .map(skill => skill.trim())
                .filter(Boolean);


        if (!skills.length) {

            container.innerHTML =
                `<span class="preview-empty">
                    No skills added yet.
                 </span>`;

            return;
        }


        container.innerHTML =
            skills
                .map(skill =>
                    `<span class="preview-skill">
                        ${escapeHTML(skill)}
                     </span>`
                )
                .join("");
    }


    /* ======================================================
       PROJECTS
       ====================================================== */

    function updateProjectsPreview() {

        const container =
            byId("previewProjects");

        const section =
            byId("previewProjectsSection");

        if (!container || !section) {
            return;
        }


        const titles =
            getValues("project_title[]");

        const technologies =
            getValues("project_technology[]");

        const descriptions =
            getValues("project_description[]");


        const max =
            Math.max(
                titles.length,
                technologies.length,
                descriptions.length
            );


        let html = "";


        for (let i = 0; i < max; i++) {

            const title =
                titles[i] || "";

            const technology =
                technologies[i] || "";

            const description =
                descriptions[i] || "";


            if (
                !title &&
                !technology &&
                !description
            ) {
                continue;
            }


            html += `
                <article class="preview-project">

                    <h3 class="preview-project-title">
                        ${escapeHTML(
                            title ||
                            "Project"
                        )}
                    </h3>

                    ${
                        technology
                            ? `
                            <div class="preview-project-tech">
                                ${escapeHTML(
                                    technology
                                )}
                            </div>
                            `
                            : ""
                    }

                    ${
                        description
                            ? `
                            <div class="preview-project-description">
                                ${escapeHTML(
                                    description
                                )}
                            </div>
                            `
                            : ""
                    }

                </article>
            `;
        }


        container.innerHTML =
            html ||
            `<div class="preview-empty">
                No projects added yet.
             </div>`;
    }


    /* ======================================================
       EXPERIENCE
       ====================================================== */

    function updateExperiencePreview() {

        const container =
            byId("previewExperience");

        if (!container) {
            return;
        }


        const companies =
            getValues("company[]");

        const roles =
            getValues("role[]");

        const durations =
            getValues("duration[]");

        const descriptions =
            getValues(
                "experience_description[]"
            );


        const max =
            Math.max(
                companies.length,
                roles.length,
                durations.length,
                descriptions.length
            );


        let html = "";


        for (let i = 0; i < max; i++) {

            const company =
                companies[i] || "";

            const role =
                roles[i] || "";

            const duration =
                durations[i] || "";

            const description =
                descriptions[i] || "";


            if (
                !company &&
                !role &&
                !duration &&
                !description
            ) {
                continue;
            }


            html += `
                <article class="preview-experience">

                    <div class="preview-experience-top">

                        <div>

                            <h3 class="preview-experience-role">
                                ${escapeHTML(
                                    role ||
                                    "Job Role"
                                )}
                            </h3>

                            <div class="preview-experience-company">
                                ${escapeHTML(
                                    company
                                )}
                            </div>

                        </div>

                        ${
                            duration
                                ? `
                                <div class="preview-experience-duration">
                                    ${escapeHTML(
                                        duration
                                    )}
                                </div>
                                `
                                : ""
                        }

                    </div>

                    ${
                        description
                            ? `
                            <div class="preview-experience-description">
                                ${escapeHTML(
                                    description
                                )}
                            </div>
                            `
                            : ""
                    }

                </article>
            `;
        }


        container.innerHTML =
            html ||
            `<div class="preview-empty">
                No work experience added yet.
             </div>`;
    }


    /* ======================================================
       CERTIFICATES
       ====================================================== */

    function updateCertificatesPreview() {

        const container =
            byId("previewCertificates");

        if (!container) {
            return;
        }


        const names =
            getValues("certificate_name[]");

        const organizations =
            getValues("certificate_org[]");

        const years =
            getValues("certificate_year[]");


        const max =
            Math.max(
                names.length,
                organizations.length,
                years.length
            );


        let html = "";


        for (let i = 0; i < max; i++) {

            const name =
                names[i] || "";

            const organization =
                organizations[i] || "";

            const year =
                years[i] || "";


            if (
                !name &&
                !organization &&
                !year
            ) {
                continue;
            }


            html += `
                <div class="preview-certificate">

                    <div class="preview-certificate-name">
                        ${escapeHTML(
                            name ||
                            "Certificate"
                        )}
                    </div>

                    ${
                        organization
                            ? `
                            <div class="preview-certificate-org">
                                ${escapeHTML(
                                    organization
                                )}
                            </div>
                            `
                            : ""
                    }

                    ${
                        year
                            ? `
                            <div class="preview-certificate-org">
                                ${escapeHTML(
                                    year
                                )}
                            </div>
                            `
                            : ""
                    }

                </div>
            `;
        }


        container.innerHTML =
            html ||
            `<div class="preview-empty">
                No certificates added yet.
             </div>`;
    }


    /* ======================================================
       LANGUAGES
       ====================================================== */

    function updateLanguagesPreview() {

        const container =
            byId("previewLanguages");

        if (!container) {
            return;
        }


        const languages =
            getValues("language[]");


        if (!languages.length) {

            container.innerHTML =
                `<span class="preview-empty">
                    No languages added yet.
                 </span>`;

            return;
        }


        container.innerHTML =
            languages
                .map(language =>
                    `<span class="preview-skill">
                        ${escapeHTML(language)}
                     </span>`
                )
                .join("");
    }


    /* ======================================================
       ACHIEVEMENTS
       ====================================================== */

    function updateAchievementsPreview() {

        const container =
            byId("previewAchievements");

        if (!container) {
            return;
        }


        const achievements =
            getValues("achievement[]");


        if (!achievements.length) {

            container.innerHTML =
                `<div class="preview-empty">
                    No achievements added yet.
                 </div>`;

            return;
        }


        container.innerHTML = `
            <ul class="preview-list">

                ${
                    achievements
                        .map(item =>
                            `<li>
                                ${escapeHTML(item)}
                             </li>`
                        )
                        .join("")
                }

            </ul>
        `;
    }


    /* ======================================================
       HOBBIES
       ====================================================== */

    function updateHobbiesPreview() {

        const container =
            byId("previewHobbies");

        if (!container) {
            return;
        }


        const hobbies =
            getValues("hobby[]");


        if (!hobbies.length) {

            container.innerHTML =
                `<span class="preview-empty">
                    No hobbies added yet.
                 </span>`;

            return;
        }


        container.innerHTML =
            hobbies
                .map(hobby =>
                    `<span class="preview-skill">
                        ${escapeHTML(hobby)}
                     </span>`
                )
                .join("");
    }


    /* ======================================================
       PROFILE PHOTO
       ====================================================== */

    function updateProfilePhoto() {

        const preview =
            byId("previewProfilePhoto");

        const source =
            byId("profilePhotoPreview");

        if (!preview || !source) {
            return;
        }


        if (source.src) {
            preview.src =
                source.src;
        }
    }


    /* ======================================================
       COMPLETION
       ====================================================== */

    function updateCompletion() {

        const fields = [

            getValue("fullname"),
            getValue("email"),
            getValue("mobile"),
            getValue("address"),
            getValue("objective"),
            getValue("skills"),
            $('[name="linkedin"]')?.value.trim(),
            $('[name="github"]')?.value.trim(),
            $('[name="portfolio"]')?.value.trim()

        ];


        const education =
            getValues(
                "education_degree[]"
            ).length > 0;

        const project =
            getValues(
                "project_title[]"
            ).length > 0;

        const experience =
            getValues(
                "role[]"
            ).length > 0;


        if (education) {
            fields.push("education");
        }

        if (project) {
            fields.push("project");
        }

        if (experience) {
            fields.push("experience");
        }


        const total =
            fields.length;

        const completed =
            fields.filter(Boolean).length;


        const percentage =
            total
                ? Math.round(
                    (completed / total) * 100
                )
                : 0;


        const completion =
            byId("resumeCompletion");

        const fill =
            byId("completionFill");


        if (completion) {
            completion.textContent =
                `${percentage}%`;
        }


        if (fill) {
            fill.style.width =
                `${percentage}%`;
        }
    }


    /* ======================================================
       UPDATE EVERYTHING
       ====================================================== */

    function updatePreview() {

        updatePersonalPreview();
        updateSocialLinks();
        updateObjectivePreview();
        updateEducationPreview();
        updateSkillsPreview();
        updateProjectsPreview();
        updateExperiencePreview();
        updateCertificatesPreview();
        updateLanguagesPreview();
        updateAchievementsPreview();
        updateHobbiesPreview();
        updateProfilePhoto();
        updateCompletion();
    }


    /* ======================================================
       LIVE INPUT LISTENERS
       ====================================================== */

    const form =
        byId("resumeForm");


    if (form) {

        form.addEventListener(
            "input",
            function (event) {

                if (
                    event.target.matches(
                        "input, textarea, select"
                    )
                ) {
                    updatePreview();
                }

            }
        );


        form.addEventListener(
            "change",
            function (event) {

                if (
                    event.target.matches(
                        "input, textarea, select"
                    )
                ) {
                    updatePreview();
                }

            }
        );
    }


    /* ======================================================
       PROFILE PHOTO CHANGE
       ====================================================== */

    const photoInput =
        byId("profilePhoto");

    if (photoInput) {

        photoInput.addEventListener(
            "change",
            function () {

                const file =
                    this.files &&
                    this.files[0];

                if (!file) {
                    return;
                }


                const reader =
                    new FileReader();


                reader.onload =
                    function (event) {

                        const preview =
                            byId(
                                "previewProfilePhoto"
                            );

                        if (preview) {
                            preview.src =
                                event.target.result;
                        }

                    };


                reader.readAsDataURL(file);
            }
        );
    }


    /* ======================================================
       REFRESH PREVIEW
       ====================================================== */

    const refreshButton =
        byId("refreshPreview");


    if (refreshButton) {

        refreshButton.addEventListener(
            "click",
            function () {

                updatePreview();

                this.classList.add(
                    "is-refreshing"
                );

                setTimeout(() => {

                    this.classList.remove(
                        "is-refreshing"
                    );

                }, 500);
            }
        );
    }


    /* ======================================================
       DOWNLOAD PDF
       ====================================================== */

    const downloadButton =
        byId("downloadPdf");


    if (downloadButton) {

        downloadButton.addEventListener(
            "click",
            async function () {

                if (
                    typeof html2pdf ===
                    "undefined"
                ) {

                    alert(
                        "PDF library could not be loaded. Please refresh the page."
                    );

                    return;
                }


                if (!resumePreview) {
                    return;
                }


                updatePreview();


                const resumeName =
                    getValue("resumeName") ||
                    "RCTI_Resume";


                const safeFileName =
                    resumeName
                        .replace(
                            /[^a-z0-9]/gi,
                            "_"
                        )
                        .replace(
                            /_+/g,
                            "_"
                        );


                const options = {

                    margin: 0,

                    filename:
                        `${safeFileName}.pdf`,

                    image: {
                        type: "jpeg",
                        quality: 0.98
                    },

                    html2canvas: {
                        scale: 2,
                        useCORS: true,
                        backgroundColor: "#ffffff"
                    },

                    jsPDF: {
                        unit: "mm",
                        format: "a4",
                        orientation: "portrait"
                    },

                    pagebreak: {
                        mode: [
                            "css",
                            "legacy"
                        ]
                    }
                };


                const originalText =
                    this.innerHTML;


                this.disabled = true;

                this.innerHTML =
                    `<i class="fas fa-spinner fa-spin"></i>
                     Generating...`;


                try {

                    await html2pdf()
                        .set(options)
                        .from(resumePreview)
                        .save();

                } catch (error) {

                    console.error(
                        "PDF generation failed:",
                        error
                    );

                    alert(
                        "Unable to generate PDF. Please try again."
                    );

                } finally {

                    this.disabled = false;

                    this.innerHTML =
                        originalText;
                }

            }
        );
    }


    /* ======================================================
       DYNAMIC SECTION HELPERS
       ====================================================== */

    function updateItemNumbers(
        containerSelector,
        itemSelector
    ) {

        const container =
            byId(containerSelector);

        if (!container) {
            return;
        }


        $$(itemSelector, container)
            .forEach(
                (item, index) => {

                    const number =
                        $(".item-number", item);

                    if (number) {
                        number.textContent =
                            index + 1;
                    }
                }
            );
    }


    function createEducationItem() {

        return `
            <div class="dynamic-item education-item">

                <div class="item-number"></div>

                <div class="dynamic-item-content">

                    <div class="form-grid">

                        <div class="field-group">
                            <label>Degree</label>
                            <input
                                type="text"
                                name="education_degree[]"
                                class="form-control"
                                placeholder="B.E / Diploma / B.Tech">
                        </div>

                        <div class="field-group">
                            <label>College / Institute</label>
                            <input
                                type="text"
                                name="education_college[]"
                                class="form-control"
                                placeholder="College name">
                        </div>

                        <div class="field-group">
                            <label>Passing Year</label>
                            <input
                                type="text"
                                name="education_year[]"
                                class="form-control"
                                placeholder="2026">
                        </div>

                        <div class="field-group">
                            <label>CGPA / Percentage</label>
                            <input
                                type="text"
                                name="education_cgpa[]"
                                class="form-control"
                                placeholder="8.5 CGPA">
                        </div>

                    </div>

                </div>

            </div>
        `;
    }


    function createProjectItem() {

        return `
            <div class="dynamic-item project-item">

                <div class="item-number"></div>

                <div class="dynamic-item-content">

                    <div class="field-group">
                        <label>Project Title</label>
                        <input
                            type="text"
                            name="project_title[]"
                            class="form-control"
                            placeholder="Project name">
                    </div>

                    <div class="field-group">
                        <label>Technology Used</label>
                        <input
                            type="text"
                            name="project_technology[]"
                            class="form-control"
                            placeholder="Python, Flask, SQLite">
                    </div>

                    <div class="field-group">
                        <label>Project Description</label>
                        <textarea
                            name="project_description[]"
                            rows="4"
                            class="form-control"
                            placeholder="Describe your project..."></textarea>
                    </div>

                </div>

            </div>
        `;
    }


    function createExperienceItem() {

        return `
            <div class="dynamic-item experience-item">

                <div class="item-number"></div>

                <div class="dynamic-item-content">

                    <div class="form-grid">

                        <div class="field-group">
                            <label>Company Name</label>
                            <input
                                type="text"
                                name="company[]"
                                class="form-control"
                                placeholder="Company name">
                        </div>

                        <div class="field-group">
                            <label>Job Role</label>
                            <input
                                type="text"
                                name="role[]"
                                class="form-control"
                                placeholder="Software Developer Intern">
                        </div>

                    </div>

                    <div class="field-group">
                        <label>Duration</label>
                        <input
                            type="text"
                            name="duration[]"
                            class="form-control"
                            placeholder="June 2025 - August 2025">
                    </div>

                    <div class="field-group">
                        <label>Description</label>
                        <textarea
                            name="experience_description[]"
                            rows="4"
                            class="form-control"
                            placeholder="Describe your responsibilities..."></textarea>
                    </div>

                </div>

            </div>
        `;
    }


    function createCertificateItem() {

        return `
            <div class="dynamic-item certificate-item">

                <div class="item-number"></div>

                <div class="dynamic-item-content">

                    <div class="certificate-grid">

                        <div class="field-group">
                            <label>Certificate Name</label>
                            <input
                                type="text"
                                name="certificate_name[]"
                                class="form-control"
                                placeholder="Python Certificate">
                        </div>

                        <div class="field-group">
                            <label>Organization</label>
                            <input
                                type="text"
                                name="certificate_org[]"
                                class="form-control"
                                placeholder="Organization">
                        </div>

                        <div class="field-group">
                            <label>Year</label>
                            <input
                                type="text"
                                name="certificate_year[]"
                                class="form-control"
                                placeholder="2026">
                        </div>

                    </div>

                </div>

            </div>
        `;
    }


    function createLanguageItem() {

        return `
            <div class="field-group language-item">

                <input
                    type="text"
                    name="language[]"
                    class="form-control"
                    placeholder="English">

            </div>
        `;
    }


    function createAchievementItem() {

        return `
            <div class="field-group">

                <textarea
                    name="achievement[]"
                    rows="2"
                    class="form-control"
                    placeholder="Achievement or award"></textarea>

            </div>
        `;
    }


    function createHobbyItem() {

        return `
            <div class="field-group">

                <input
                    type="text"
                    name="hobby[]"
                    class="form-control"
                    placeholder="Reading Books">

            </div>
        `;
    }


    /* ======================================================
       ADD BUTTONS
       ====================================================== */

    function addDynamicItem(
        buttonId,
        containerId,
        html,
        itemSelector
    ) {

        const button =
            byId(buttonId);

        const container =
            byId(containerId);


        if (!button || !container) {
            return;
        }


        button.addEventListener(
            "click",
            function () {

                container.insertAdjacentHTML(
                    "beforeend",
                    html()
                );


                updateItemNumbers(
                    containerId,
                    itemSelector
                );

                updatePreview();

                const items =
                    $$(itemSelector, container);

                const lastItem =
                    items[items.length - 1];


                if (lastItem) {

                    const input =
                        $("input, textarea", lastItem);

                    if (input) {
                        input.focus();
                    }
                }

            }
        );
    }


    addDynamicItem(
        "addEducation",
        "educationContainer",
        createEducationItem,
        ".education-item"
    );


    addDynamicItem(
        "addProject",
        "projectContainer",
        createProjectItem,
        ".project-item"
    );


    addDynamicItem(
        "addExperience",
        "experienceContainer",
        createExperienceItem,
        ".experience-item"
    );


    addDynamicItem(
        "addCertificate",
        "certificateContainer",
        createCertificateItem,
        ".certificate-item"
    );


    addDynamicItem(
        "addLanguage",
        "languageContainer",
        createLanguageItem,
        ".language-item"
    );


    addDynamicItem(
        "addAchievement",
        "achievementContainer",
        createAchievementItem,
        "textarea"
    );


    addDynamicItem(
        "addHobby",
        "hobbyContainer",
        createHobbyItem,
        "input"
    );


    /* ======================================================
       TOGGLE SECTION
       ====================================================== */

    window.toggleSection =
        function (
            containerId,
            show
        ) {

            const container =
                byId(containerId);

            if (!container) {
                return;
            }


            container.style.display =
                show ? "block" : "none";


            updatePreview();
        };


    /* ======================================================
       INITIAL NUMBERING
       ====================================================== */

    updateItemNumbers(
        "educationContainer",
        ".education-item"
    );

    updateItemNumbers(
        "projectContainer",
        ".project-item"
    );

    updateItemNumbers(
        "experienceContainer",
        ".experience-item"
    );

    updateItemNumbers(
        "certificateContainer",
        ".certificate-item"
    );


    /* ======================================================
       FORM SUBMIT
       ====================================================== */

    if (form) {

        form.addEventListener(
            "submit",
            function () {

                /*
                 * Make sure selected template is
                 * present in the hidden select.
                 */

                if (templateSelect) {

                    const current =
                        normalizeTemplate(
                            templateSelect.value
                        );

                    templateSelect.value =
                        current;
                }

            }
        );
    }


    /* ======================================================
       INITIALIZE
       ====================================================== */

    loadSavedTemplate();

    updatePreview();


    console.log(
        "Template system ready."
    );

    console.log(
        "Available templates:",
        [
            "ats",
            "modern",
            "executive",
            "creative",
            "developer",
            "data",
            "minimal",
            "fresher"
        ]
    );

});