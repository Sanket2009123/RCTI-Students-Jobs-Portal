document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("resumeUploadForm");
    const input = document.getElementById("resumeInput");
    const uploadArea = document.getElementById("uploadArea");
    const chooseBtn = document.getElementById("chooseFileBtn");

    const selectedFile = document.getElementById("selectedFile");
    const fileName = document.getElementById("fileName");
    const fileSize = document.getElementById("fileSize");
    const fileTypeIcon = document.getElementById("fileTypeIcon");

    const removeBtn = document.getElementById("removeFileBtn");

    const errorMessage = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");

    const submitBtn = document.getElementById("uploadSubmitBtn");

    const MAX_FILE_SIZE = 5 * 1024 * 1024;

    const ALLOWED_EXTENSIONS = [
        "pdf",
        "doc",
        "docx"
    ];


    /* ======================================================
       CHOOSE FILE
    ====================================================== */

    chooseBtn.addEventListener("click", function (event) {

        event.stopPropagation();

        input.click();

    });


    /* ======================================================
       CLICK DROP AREA
    ====================================================== */

    uploadArea.addEventListener("click", function (event) {

        if (
            event.target === chooseBtn ||
            chooseBtn.contains(event.target)
        ) {
            return;
        }

        input.click();

    });


    /* ======================================================
       FILE SELECTED
    ====================================================== */

    input.addEventListener("change", function () {

        if (input.files.length > 0) {

            handleFile(input.files[0]);

        }

    });


    /* ======================================================
       DRAG ENTER
    ====================================================== */

    uploadArea.addEventListener("dragenter", function (event) {

        event.preventDefault();

        uploadArea.classList.add("drag-over");

    });


    /* ======================================================
       DRAG OVER
    ====================================================== */

    uploadArea.addEventListener("dragover", function (event) {

        event.preventDefault();

        uploadArea.classList.add("drag-over");

    });


    /* ======================================================
       DRAG LEAVE
    ====================================================== */

    uploadArea.addEventListener("dragleave", function (event) {

        event.preventDefault();

        uploadArea.classList.remove("drag-over");

    });


    /* ======================================================
       DROP
    ====================================================== */

    uploadArea.addEventListener("drop", function (event) {

        event.preventDefault();

        uploadArea.classList.remove("drag-over");

        const files = event.dataTransfer.files;

        if (!files || files.length === 0) {
            return;
        }

        const file = files[0];

        handleFile(file);

    });


    /* ======================================================
       HANDLE FILE
    ====================================================== */

    function handleFile(file) {

        clearError();

        const extension = getExtension(file.name);


        /* -----------------------------------------------
           Extension validation
        ------------------------------------------------ */

        if (!ALLOWED_EXTENSIONS.includes(extension)) {

            showError(
                "Only PDF, DOC and DOCX files are allowed."
            );

            resetFile();

            return;

        }


        /* -----------------------------------------------
           Size validation
        ------------------------------------------------ */

        if (file.size > MAX_FILE_SIZE) {

            showError(
                "Resume size must be less than 5 MB."
            );

            resetFile();

            return;

        }


        /* -----------------------------------------------
           Set selected file
        ------------------------------------------------ */

        fileName.textContent = file.name;

        fileSize.textContent = formatFileSize(file.size);

        setFileIcon(extension);

        selectedFile.style.display = "flex";

        submitBtn.disabled = false;

    }


    /* ======================================================
       REMOVE FILE
    ====================================================== */

    removeBtn.addEventListener("click", function () {

        resetFile();

    });


    /* ======================================================
       RESET FILE
    ====================================================== */

    function resetFile() {

        input.value = "";

        selectedFile.style.display = "none";

        submitBtn.disabled = false;

        clearError();

    }


    /* ======================================================
       GET EXTENSION
    ====================================================== */

    function getExtension(filename) {

        return filename
            .split(".")
            .pop()
            .toLowerCase();

    }


    /* ======================================================
       FILE ICON
    ====================================================== */

    function setFileIcon(extension) {

        if (extension === "pdf") {

            fileTypeIcon.innerHTML =
                '<i class="fa-solid fa-file-pdf"></i>';

            fileTypeIcon.style.background = "#feecec";
            fileTypeIcon.style.color = "#dc3545";

        } else {

            fileTypeIcon.innerHTML =
                '<i class="fa-solid fa-file-word"></i>';

            fileTypeIcon.style.background = "#eaf2ff";
            fileTypeIcon.style.color = "#2563eb";

        }

    }


    /* ======================================================
       FORMAT SIZE
    ====================================================== */

    function formatFileSize(bytes) {

        if (bytes === 0) {
            return "0 KB";
        }

        const units = [
            "Bytes",
            "KB",
            "MB",
            "GB"
        ];

        const index =
            Math.floor(
                Math.log(bytes) /
                Math.log(1024)
            );

        const size =
            bytes /
            Math.pow(1024, index);

        return (
            size.toFixed(2)
            + " "
            + units[index]
        );

    }


    /* ======================================================
       ERROR
    ====================================================== */

    function showError(message) {

        errorText.textContent = message;

        errorMessage.style.display = "flex";

    }


    /* ======================================================
       CLEAR ERROR
    ====================================================== */

    function clearError() {

        errorMessage.style.display = "none";

        errorText.textContent = "";

    }


    /* ======================================================
       FORM SUBMIT
    ====================================================== */

    form.addEventListener("submit", function () {

        if (!input.files.length) {

            showError(
                "Please select a resume before uploading."
            );

            return;

        }

        submitBtn.disabled = true;

        submitBtn.querySelector(".button-content").innerHTML =
            `
            <i class="fa-solid fa-spinner fa-spin"></i>
            Uploading Resume...
            `;

    });

});