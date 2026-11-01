document.addEventListener("DOMContentLoaded", function () {

    const photoInput =
        document.getElementById("profilePhotoInput");

    const uploadPhotoBtn =
        document.getElementById("uploadPhotoBtn");

    const selectedPhotoName =
        document.getElementById("selectedPhotoName");


    // Stop if elements are not available
    if (!photoInput) {
        return;
    }


    // ==========================================
    // PHOTO SELECTED
    // ==========================================

    photoInput.addEventListener("change", function () {

        if (!photoInput.files.length) {
            return;
        }

        const file = photoInput.files[0];


        // ==========================================
        // ALLOWED IMAGE TYPES
        // ==========================================

        const allowedTypes = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ];


        if (!allowedTypes.includes(file.type)) {

            alert(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            );

            photoInput.value = "";

            uploadPhotoBtn.style.display = "none";

            selectedPhotoName.textContent = "";

            return;
        }


        // ==========================================
        // MAXIMUM SIZE - 5 MB
        // ==========================================

        const maxSize =
            5 * 1024 * 1024;


        if (file.size > maxSize) {

            alert(
                "Photo size must be less than 5 MB."
            );

            photoInput.value = "";

            uploadPhotoBtn.style.display = "none";

            selectedPhotoName.textContent = "";

            return;
        }


        // ==========================================
        // SHOW SELECTED FILE
        // ==========================================

        selectedPhotoName.textContent =
            "Selected: " + file.name;


        // ==========================================
        // SHOW UPLOAD BUTTON
        // ==========================================

        uploadPhotoBtn.style.display =
            "inline-block";

    });

});