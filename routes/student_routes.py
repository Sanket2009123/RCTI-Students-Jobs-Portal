from flask import jsonify, render_template, request, redirect, session, flash, url_for
from database.db import get_connection
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

from utils.decorators import student_required
from werkzeug.security import generate_password_hash
from firebase_admin import auth


def register_student_routes(app):
    @app.context_processor
    def inject_current_student():

        if "student_id" not in session:
            return {
                "student": None
            }

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id=?
        """, (session["student_id"],))

        student = cursor.fetchone()

        conn.close()

        return {
            "student": student
        }
    # ==========================
    # Student Dashboard
    # ==========================

    @app.route("/student/dashboard")
    @student_required
    def student_dashboard():

        print("student_id =", session.get("student_id"))
        print("company_id =", session.get("company_id"))

        conn = get_connection()
        cursor = conn.cursor()

        student_id = session["student_id"]

        # ==========================
        # Total Jobs
        # ==========================

        cursor.execute("""
            SELECT COUNT(*) as total
            FROM jobs
            WHERE status='Active'
        """)

        total_jobs = cursor.fetchone()["total"]

        # ==========================
        # Applied Jobs
        # ==========================

        cursor.execute("""
            SELECT COUNT(*) as total
            FROM applications
            WHERE student_id=?
        """, (student_id,))

        applied_jobs = cursor.fetchone()["total"]

        # ==========================
        # Student Details
        # ==========================

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id=?
        """, (student_id,))

        student = cursor.fetchone()

        resume_status = "Not Uploaded"

        if student["resume"]:
            resume_status = "Uploaded"

        # ==========================
        # Profile Strength
        # ==========================

        profile_strength = 0

        if student["firstname"] and student["lastname"]:
            profile_strength += 15

        if student["email"]:
            profile_strength += 10

        if student["mobile"]:
            profile_strength += 10

        if student["branch"]:
            profile_strength += 10

        if student["semester"]:
            profile_strength += 10

        if student["skills"]:
            profile_strength += 20

        if student["about"]:
            profile_strength += 10

        if student["resume"]:
            profile_strength += 15

        # ==========================
        # Latest Jobs
        # ==========================

        cursor.execute("""
            SELECT *
            FROM jobs
            ORDER BY id DESC
            LIMIT 6
        """)

        latest_jobs = cursor.fetchall()

        # ==========================
        # Recent Applications
        # ==========================

        cursor.execute("""
            SELECT
                jobs.title,
                companies.company_name,
                applications.status,
                applications.apply_date

            FROM applications

            JOIN jobs
            ON applications.job_id=jobs.id

            JOIN companies
            ON applications.company_id=companies.id

            WHERE applications.student_id=?

            ORDER BY applications.id DESC

            LIMIT 5
        """, (student_id,))

        recent_applications = cursor.fetchall()

        conn.close()

        return render_template(
            "student_dashboard.html",
            total_jobs=total_jobs,
            applied_jobs=applied_jobs,
            resume_status=resume_status,
            latest_jobs=latest_jobs,
            recent_applications=recent_applications,
            student=student,
            profile_strength=profile_strength
        )

    # ==========================
    # Student Profile
    # ==========================

    @app.route("/student/profile", methods=["GET", "POST"])
    @student_required
    def student_profile():

        conn = get_connection()
        cursor = conn.cursor()

        student_id = session["student_id"]

        if request.method == "POST":

            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            mobile = request.form["mobile"]
            branch = request.form["branch"]
            semester = request.form["semester"]
            skills = request.form["skills"]
            about = request.form["about"]

            cursor.execute("""
                UPDATE students
                SET
                    firstname=?,
                    lastname=?,
                    mobile=?,
                    branch=?,
                    semester=?,
                    skills=?,
                    about=?
                WHERE id=?
            """, (
                firstname,
                lastname,
                mobile,
                branch,
                semester,
                skills,
                about,
                student_id
            ))

            conn.commit()

            # Update session name
            session["student_name"] = firstname + " " + lastname

            flash(
                "Profile Updated Successfully!",
                "success"
            )

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id=?
        """, (student_id,))

        student = cursor.fetchone()

        conn.close()

        return render_template(
            "student_profile.html",
            student=student
        )

    # ==========================
    # Edit Student Profile
    # ==========================

    @app.route("/student/edit-profile", methods=["GET", "POST"])
    @student_required
    def edit_student_profile():

        conn = get_connection()
        cursor = conn.cursor()

        student_id = session["student_id"]

        if request.method == "POST":

            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            mobile = request.form["mobile"]
            branch = request.form["branch"]
            semester = request.form["semester"]
            college = request.form["college"]
            skills = request.form["skills"]
            about = request.form["about"]
            address = request.form["address"]

            cursor.execute("""
                UPDATE students
                SET
                    firstname=?,
                    lastname=?,
                    mobile=?,
                    branch=?,
                    semester=?,
                    college=?,
                    skills=?,
                    about=?,
                    address=?
                WHERE id=?
            """, (
                firstname,
                lastname,
                mobile,
                branch,
                semester,
                college,
                skills,
                about,
                address,
                student_id
            ))

            conn.commit()

            # Update session name
            session["student_name"] = firstname + " " + lastname

            flash(
                "Profile Updated Successfully!",
                "success"
            )

            conn.close()

            return redirect("/student/profile")

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id=?
        """, (student_id,))

        student = cursor.fetchone()

        conn.close()

        return render_template(
            "edit_student_profile.html",
            student=student
        )
    # ==========================
# View Uploaded Resume
# ==========================

    @app.route("/student/view-resume")
    @student_required
    def view_uploaded_resume():

        from flask import send_from_directory

        student_id = session["student_id"]

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT resume
                FROM students
                WHERE id=?
            """, (student_id,))

            student = cursor.fetchone()

        finally:
            conn.close()

        if not student or not student["resume"]:
            flash(
                "No resume uploaded.",
                "warning"
            )
            return redirect(
                url_for("student_profile")
            )

        resume_filename = student["resume"]

        resume_folder = app.config["RESUME_FOLDER"]

        resume_path = os.path.join(
            resume_folder,
            resume_filename
        )

        if not os.path.isfile(resume_path):
            flash(
                "Resume file could not be found.",
                "danger"
            )
            return redirect(
                url_for("student_profile")
            )

        return send_from_directory(
            resume_folder,
            resume_filename,
            as_attachment=False
        )

    # ==========================
    # Download Uploaded Resume
    # ==========================

    @app.route("/student/download-resume")
    @student_required
    def download_uploaded_resume():

        from flask import send_from_directory

        student_id = session["student_id"]

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT resume
                FROM students
                WHERE id=?
            """, (student_id,))

            student = cursor.fetchone()

        finally:
            conn.close()

        if not student or not student["resume"]:
            flash(
                "No resume uploaded.",
                "warning"
            )
            return redirect(
                url_for("student_profile")
            )

        resume_filename = student["resume"]
        resume_folder = app.config["RESUME_FOLDER"]

        resume_path = os.path.join(
            resume_folder,
            resume_filename
        )

        if not os.path.isfile(resume_path):
            flash(
                "Resume file could not be found.",
                "danger"
            )
            return redirect(
                url_for("student_profile")
            )

        return send_from_directory(
            resume_folder,
            resume_filename,
            as_attachment=True
        )

    # ==========================
    # Change Profile Photo
    # ==========================

    @app.route("/student/change-photo", methods=["POST"])
    @student_required
    def change_photo():

        photo = request.files.get("photo")

        if not photo or photo.filename == "":
            flash("Please select a photo.", "danger")
            return redirect(url_for("student_profile"))

        # ----------------------------------------------------------
        # Allowed image types
        # ----------------------------------------------------------

        allowed_extensions = {
            "jpg",
            "jpeg",
            "png",
            "webp"
        }

        if "." not in photo.filename:
            flash("Invalid image file.", "danger")
            return redirect(url_for("student_profile"))

        extension = photo.filename.rsplit(".", 1)[1].lower()

        if extension not in allowed_extensions:
            flash(
                "Only JPG, JPEG, PNG and WEBP images are allowed.",
                "danger"
            )
            return redirect(url_for("student_profile"))

        # ----------------------------------------------------------
        # Secure filename
        # ----------------------------------------------------------

        original_name = secure_filename(photo.filename)

        if not original_name:
            flash("Invalid photo filename.", "danger")
            return redirect(url_for("student_profile"))

        # ----------------------------------------------------------
        # Generate unique filename
        # ----------------------------------------------------------

        filename = f"{uuid.uuid4().hex}.{extension}"

        profile_folder = app.config["PROFILE_FOLDER"]

        os.makedirs(
            profile_folder,
            exist_ok=True
        )

        filepath = os.path.join(
            profile_folder,
            filename
        )

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # ------------------------------------------------------
            # Get old photo
            # ------------------------------------------------------

            cursor.execute(
                """
                SELECT profile_photo
                FROM students
                WHERE id = ?
                """,
                (session["student_id"],)
            )

            student = cursor.fetchone()

            old_photo = None

            if student:
                old_photo = student["profile_photo"]

            # ------------------------------------------------------
            # Save NEW photo
            # ------------------------------------------------------

            photo.save(filepath)

            # ------------------------------------------------------
            # Update database
            # ------------------------------------------------------

            cursor.execute(
                """
                UPDATE students
                SET profile_photo = ?
                WHERE id = ?
                """,
                (
                    filename,
                    session["student_id"]
                )
            )

            conn.commit()

            # ------------------------------------------------------
            # Update session
            # ------------------------------------------------------

            session["student_photo"] = filename

            # ------------------------------------------------------
            # Delete OLD photo
            # ------------------------------------------------------

            if old_photo and old_photo != "default.png":

                old_path = os.path.join(
                    profile_folder,
                    old_photo
                )

                if os.path.isfile(old_path):

                    try:
                        os.remove(old_path)

                    except OSError as e:
                        print(
                            "Old profile photo delete error:",
                            e
                        )

            flash(
                "Profile photo updated successfully!",
                "success"
            )

        except Exception as e:

            conn.rollback()

            # If database update failed,
            # remove newly uploaded file.

            if os.path.isfile(filepath):

                try:
                    os.remove(filepath)

                except OSError:
                    pass

            print(
                "Profile photo upload error:",
                e
            )

            flash(
                "Unable to update profile photo.",
                "danger"
            )

        finally:

            conn.close()

        return redirect(
            url_for("student_profile")
        )

    # ==========================
    # Upload Resume
    # ==========================

    # ==========================
# Upload Resume
# ==========================

    @app.route("/student/upload-resume", methods=["GET", "POST"])
    @student_required
    def upload_resume():

        conn = get_connection()
        cursor = conn.cursor()

        student_id = session["student_id"]

        # ==========================================================
        # GET REQUEST
        # ==========================================================

        if request.method == "GET":

            conn.close()

            return render_template(
                "upload_resume.html"
            )

        # ==========================================================
        # POST REQUEST
        # ==========================================================

        resume = request.files.get("resume")

        # ----------------------------------------------------------
        # Check file
        # ----------------------------------------------------------

        if not resume or resume.filename == "":
            conn.close()

            flash(
                "Please select a resume file.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        # ----------------------------------------------------------
        # Allowed extensions
        # ----------------------------------------------------------

        allowed_extensions = {
            "pdf",
            "doc",
            "docx"
        }

        original_filename = resume.filename

        if "." not in original_filename:

            conn.close()

            flash(
                "Invalid resume file.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        extension = (
            original_filename
        .rsplit(".", 1)[1]
        .lower()
        )

        if extension not in allowed_extensions:

            conn.close()

            flash(
                "Only PDF, DOC and DOCX files are allowed.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        # ----------------------------------------------------------
        # File size validation
        # Maximum = 5 MB
        # ----------------------------------------------------------

        resume.seek(0, os.SEEK_END)

        file_size = resume.tell()

        resume.seek(0)

        max_size = 5 * 1024 * 1024

        if file_size > max_size:

            conn.close()

            flash(
                "Resume size must be less than 5 MB.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        # ----------------------------------------------------------
        # Secure filename
        # ----------------------------------------------------------

        safe_filename = secure_filename(
            original_filename
        )

        if not safe_filename:

            conn.close()

            flash(
                "Invalid filename.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        filename = (
            str(uuid.uuid4())
            + "_"
            + safe_filename
        )

        # ----------------------------------------------------------
        # Resume folder
        # ----------------------------------------------------------

        resume_folder = app.config["RESUME_FOLDER"]

        os.makedirs(
            resume_folder,
            exist_ok=True
        )

        filepath = os.path.join(
            resume_folder,
            filename
        )

        # ----------------------------------------------------------
        # Get old resume
        # ----------------------------------------------------------

        cursor.execute(
            """
            SELECT resume
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        old_filename = None

        if student:

            old_filename = student["resume"]

        try:

            # ======================================================
            # SAVE NEW FILE
            # ======================================================

            resume.save(filepath)

            # ======================================================
            # UPDATE DATABASE
            # ======================================================

            cursor.execute(
                """
                UPDATE students
                SET resume = ?
                WHERE id = ?
                """,
                (
                    filename,
                    student_id
                )
            )

            conn.commit()

            # ======================================================
            # DELETE OLD FILE
            # ======================================================

            if old_filename:

                old_filepath = os.path.join(
                    resume_folder,
                    old_filename
                )

                if (
                    old_filename != filename
                    and os.path.exists(old_filepath)
                ):

                    try:
                        os.remove(old_filepath)

                    except OSError as e:
                        print(
                            "Old Resume Delete Error:",
                            e
                        )

            flash(
                "Resume uploaded successfully!",
                "success"
            )

            return redirect(
                url_for("upload_resume")
            )

        except Exception as e:

            conn.rollback()

            # ------------------------------------------------------
            # Delete newly saved file if database failed
            # ------------------------------------------------------

            if os.path.exists(filepath):

                try:
                    os.remove(filepath)

                except OSError:
                    pass

            print(
                "Resume Upload Error:",
                e
            )

            flash(
                "Something went wrong while uploading your resume.",
                "danger"
            )

            return redirect(
                url_for("upload_resume")
            )

        finally:

            conn.close()    # ==========================
    # Student Jobs
    # ==========================

    @app.route("/student/jobs")
    @student_required
    def student_jobs():

        search = request.args.get("search", "")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                jobs.*,
                companies.company_name

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            WHERE
                jobs.title LIKE ?
                OR jobs.category LIKE ?
                OR jobs.location LIKE ?

            ORDER BY jobs.id DESC
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "student_jobs.html",
            jobs=jobs,
            search=search
        )

    # ==========================
    # Job Details
    # ==========================

    @app.route("/student/job/<int:job_id>")
    @student_required
    def job_details(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                jobs.*,
                companies.company_name

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            WHERE jobs.id=?
        """, (job_id,))

        job = cursor.fetchone()

        conn.close()

        if job is None:
            return "Job Not Found"

        return render_template(
            "job_details.html",
            job=job
        )

    # ==========================
    # Apply Job
    # ==========================

    @app.route("/student/apply/<int:job_id>")
    @student_required
    def apply_job(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        # ==========================
        # Check Job
        # ==========================

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE id=?
        """, (job_id,))

        job = cursor.fetchone()

        if job is None:

            conn.close()

            return "Job Not Found"

        # ==========================
        # Check Already Applied
        # ==========================

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE student_id=? AND job_id=?
        """, (
            session["student_id"],
            job_id
        ))

        already = cursor.fetchone()

        if already:

            conn.close()

            flash(
                "You have already applied for this job.",
                "warning"
            )

            return redirect("/student/jobs")

        # ==========================
        # Insert Application
        # ==========================

        cursor.execute("""
            INSERT INTO applications
            (
                student_id,
                job_id,
                company_id,
                apply_date
            )

            VALUES
            (?, ?, ?, ?)
        """, (
            session["student_id"],
            job_id,
            job["company_id"],
            datetime.now().strftime("%d-%m-%Y")
        ))

        conn.commit()
        conn.close()

        flash(
            "Application Submitted Successfully!",
            "success"
        )

        return redirect("/student/my-applications")

    # ==========================
    # My Applications
    # ==========================

    @app.route("/student/my-applications")
    @student_required
    def my_applications():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.*,
                jobs.title,
                companies.company_name

            FROM applications

            JOIN jobs
            ON applications.job_id = jobs.id

            JOIN companies
            ON applications.company_id = companies.id

            WHERE applications.student_id=?

            ORDER BY applications.id DESC
        """, (
            session["student_id"],
        ))

        applications = cursor.fetchall()

        conn.close()

        return render_template(
            "applications.html",
            applications=applications
        )

    # ==========================
    # Student Google Login
    # ==========================

    @app.route("/student/google-login", methods=["POST"])
    def student_google_login():

        data = request.get_json()

        token = data.get("token")

        try:

            decoded = auth.verify_id_token(token)

            google_id = decoded["uid"]
            email = decoded["email"]
            name = decoded.get("name", "Student")

            # ==========================
            # Split Google Name
            # ==========================

            name_parts = name.strip().split()

            if len(name_parts) >= 2:

                firstname = name_parts[0]
                lastname = " ".join(name_parts[1:])

            else:

                firstname = name
                lastname = "Student"

            conn = get_connection()
            cursor = conn.cursor()

            # ==========================
            # Search Student by Email
            # ==========================

            cursor.execute("""
                SELECT *
                FROM students
                WHERE email=?
            """, (email,))

            student = cursor.fetchone()

            # ==========================
            # Existing Student
            # ==========================

            if student:

                if not student["google_id"]:

                    cursor.execute("""
                        UPDATE students
                        SET google_id=?
                        WHERE id=?
                    """, (
                        google_id,
                        student["id"]
                    ))

                    conn.commit()

                session.clear()

                session["student_id"] = student["id"]

                session["student_name"] = (
                    student["firstname"]
                    + " "
                    + student["lastname"]
                )

                session["student_email"] = student["email"]

                session["student_photo"] = student["profile_photo"]

            # ==========================
            # New Student
            # ==========================

            else:

                cursor.execute("""
                    INSERT INTO students
                    (
                        firstname,
                        lastname,
                        email,
                        password,
                        google_id
                    )

                    VALUES
                    (?, ?, ?, ?, ?)
                """, (
                    firstname,
                    lastname,
                    email,
                    generate_password_hash("GOOGLE_LOGIN"),
                    google_id
                ))

                conn.commit()

                student_id = cursor.lastrowid

                session.clear()

                session["student_id"] = student_id

                session["student_name"] = (
                    firstname
                    + " "
                    + lastname
                )

                session["student_email"] = email

                session["student_photo"] = "default.png"

            conn.close()

            return jsonify({
                "success": True,
                "redirect": "/student/dashboard"
            })

        except Exception as e:

            return jsonify({
                "success": False,
                "message": str(e)
            })
    @app.route("/student/profile-photo/<filename>")
    @student_required
    def student_profile_photo(filename):

        from flask import send_from_directory

        profile_folder = app.config["PROFILE_FOLDER"]

        return send_from_directory(
            profile_folder,
            filename
        )