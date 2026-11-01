from flask import (
    render_template,
    request,
    redirect,
    session,
    flash,
    jsonify,
    current_app,
    url_for
)

from database.db import get_connection
from utils.decorators import company_required

import os
from datetime import datetime
import time as time_module

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from firebase_admin import auth

import smtplib
from email.message import EmailMessage


def ensure_selection_events_table():
    """Create the free interview/test scheduling table if needed."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS selection_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                event_type TEXT NOT NULL CHECK(event_type IN ('Interview', 'Test')),
                title TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                meeting_link TEXT,
                message TEXT,
                status TEXT DEFAULT 'Scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(application_id) REFERENCES applications(id),
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()



def send_new_job_email_to_students(app, job):
    """
    Send a new-job email to registered students who have an email address.

    Uses standard Python SMTP only. No paid API/service is required.
    Configure SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD and
    MAIL_FROM in Flask config/environment.
    """

    smtp_host = app.config.get("SMTP_HOST")
    smtp_port = int(app.config.get("SMTP_PORT", 587))
    smtp_username = app.config.get("SMTP_USERNAME")
    smtp_password = app.config.get("SMTP_PASSWORD")
    mail_from = app.config.get("MAIL_FROM") or smtp_username

    # Email is intentionally skipped until SMTP is configured.
    if not all([smtp_host, smtp_username, smtp_password, mail_from]):
        app.logger.warning(
            "New-job email skipped: SMTP settings are not configured."
        )
        return 0

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT email
            FROM students
            WHERE email IS NOT NULL
              AND TRIM(email) != ''
        """)

        recipients = [
            row["email"].strip()
            for row in cursor.fetchall()
            if row["email"] and row["email"].strip()
        ]

    finally:
        conn.close()

    if not recipients:
        return 0

    host_url = app.config.get("PORTAL_BASE_URL", "http://127.0.0.1:5000")
    job_url = f"{host_url}/student/jobs"

    subject = f"New Job Opportunity: {job['title']}"

    body = f"""Hello,

A new job opportunity has been posted on RCTI Students Jobs Portal.

Job Title: {job['title']}
Category: {job['category']}
Location: {job['location']}
Job Type: {job['job_type']}

You can view the job and apply from your student account:

{job_url}

Please log in to your RCTI Students Jobs Portal account to view
the complete job details.

Regards,
RCTI Students Jobs Portal
"""

    sent = 0

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)

            for recipient in recipients:
                message = EmailMessage()
                message["Subject"] = subject
                message["From"] = mail_from
                message["To"] = recipient
                message.set_content(body)

                smtp.send_message(message)
                sent += 1

    except Exception:
        app.logger.exception("Failed to send new-job notification emails.")

    return sent


def register_company_routes(app):
    ensure_selection_events_table()


    # ==========================================================
    # COMPANY DASHBOARD
    # ==========================================================

    @app.route("/company/dashboard")
    @company_required
    def company_dashboard():

        conn = get_connection()
        cursor = conn.cursor()

        company_id = session["company_id"]

        # ------------------------------------------------------
        # Company Profile / Logo
        # ------------------------------------------------------
        cursor.execute("""
            SELECT company_name, email, logo
            FROM companies
            WHERE id = ?
        """, (company_id,))

        company = cursor.fetchone()

        # Keep the session logo synchronized with the database.
        company_logo = (
            company["logo"]
            if company and company["logo"]
            else session.get("company_logo", "default.png")
        )

        company_name = (
            company["company_name"]
            if company and company["company_name"]
            else session.get("company_name", "Company")
        )

        session["company_logo"] = company_logo
        session["company_name"] = company_name

        # ------------------------------------------------------
        # Total Jobs
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM jobs
            WHERE company_id = ?
        """, (company_id,))

        total_jobs = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Total Applications
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM applications
            WHERE company_id = ?
        """, (company_id,))

        total_applications = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Active Jobs
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM jobs
            WHERE company_id = ?
            AND status = 'Active'
        """, (company_id,))

        active_jobs = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Inactive Jobs
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM jobs
            WHERE company_id = ?
            AND status = 'Inactive'
        """, (company_id,))

        inactive_jobs = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Shortlisted Students
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM applications
            WHERE company_id = ?
            AND status = 'Accepted'
        """, (company_id,))

        shortlisted = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Rejected Students
        # ------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM applications
            WHERE company_id = ?
            AND status = 'Rejected'
        """, (company_id,))

        rejected = cursor.fetchone()["total"]

        # ------------------------------------------------------
        # Recent Jobs
        # ------------------------------------------------------

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE company_id = ?
            ORDER BY id DESC
            LIMIT 5
        """, (company_id,))

        recent_jobs = cursor.fetchall()

        # ------------------------------------------------------
        # Recent Applications
        #
        # IMPORTANT:
        # students table contains firstname + lastname,
        # NOT fullname.
        # ------------------------------------------------------

        cursor.execute("""
            SELECT
                students.firstname || ' ' || students.lastname
                    AS fullname,
                jobs.title,
                applications.apply_date,
                applications.status

            FROM applications

            JOIN students
                ON applications.student_id = students.id

            JOIN jobs
                ON applications.job_id = jobs.id

            WHERE applications.company_id = ?

            ORDER BY applications.id DESC

            LIMIT 5
        """, (company_id,))

        recent_applications = cursor.fetchall()

        conn.close()

        return render_template(
            "company_dashboard.html",
            total_jobs=total_jobs,
            active_jobs=active_jobs,
            inactive_jobs=inactive_jobs,
            total_applications=total_applications,
            shortlisted=shortlisted,
            rejected=rejected,
            recent_jobs=recent_jobs,
            recent_applications=recent_applications,
            company=company,
            company_name=company_name,
            company_logo=company_logo
        )


    # ==========================================================
    # POST JOB
    # ==========================================================

    @app.route("/company/post-job", methods=["GET", "POST"])
    @company_required
    def post_job():

        if request.method == "POST":

            title = request.form.get("title", "").strip()
            category = request.form.get("category", "").strip()
            location = request.form.get("location", "").strip()
            job_type = request.form.get("job_type", "").strip()
            salary = request.form.get("salary", "").strip()
            experience = request.form.get("experience", "").strip()
            vacancies = request.form.get("vacancies", "").strip()
            last_date = request.form.get("last_date", "").strip()
            skills = request.form.get("skills", "").strip()
            responsibilities = request.form.get("responsibilities", "").strip()
            description = request.form.get("description", "").strip()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO jobs
                (
                    company_id,
                    title,
                    category,
                    location,
                    job_type,
                    salary,
                    experience,
                    vacancies,
                    last_date,
                    skills,
                    responsibilities,
                    description,
                    status,
                    post_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session["company_id"],
                title,
                category,
                location,
                job_type,
                salary,
                experience,
                vacancies,
                last_date,
                skills,
                responsibilities,
                description,
                "Active",
                datetime.now().strftime("%d-%m-%Y")
            ))

            conn.commit()

            # Get the newly-created job for the email notification.
            job_id = cursor.lastrowid

            cursor.execute("""
                SELECT
                    id,
                    title,
                    category,
                    location,
                    job_type
                FROM jobs
                WHERE id = ?
                AND company_id = ?
            """, (
                job_id,
                session["company_id"]
            ))

            new_job = cursor.fetchone()

            conn.close()

            # Free SMTP email notification.
            # If SMTP is not configured, the job is still posted normally.
            if new_job:
                sent_count = send_new_job_email_to_students(
                    current_app,
                    new_job
                )

                if sent_count:
                    flash(
                        f"Job Posted Successfully! "
                        f"Email sent to {sent_count} student(s).",
                        "success"
                    )
                else:
                    flash(
                        "Job Posted Successfully!",
                        "success"
                    )
            else:
                flash(
                    "Job Posted Successfully!",
                    "success"
                )

            return redirect("/company/my-jobs")

        return render_template("post_job.html")


    # ==========================================================
    # MANAGE JOBS
    # ==========================================================

    @app.route("/company/my-jobs")
    @company_required
    def company_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE company_id = ?
            ORDER BY id DESC
        """, (session["company_id"],))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "manage_jobs.html",
            jobs=jobs
        )


    # ==========================================================
    # ACTIVE JOBS
    # ==========================================================

    @app.route("/company/active-jobs")
    @company_required
    def active_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE company_id = ?
            AND status = 'Active'
            ORDER BY id DESC
        """, (session["company_id"],))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "active_jobs.html",
            jobs=jobs
        )


    # ==========================================================
    # INACTIVE JOBS
    # ==========================================================

    @app.route("/company/inactive-jobs")
    @company_required
    def inactive_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE company_id = ?
            AND status = 'Inactive'
            ORDER BY id DESC
        """, (session["company_id"],))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "inactive_jobs.html",
            jobs=jobs
        )


    # ==========================================================
    # EDIT JOB
    # ==========================================================

    @app.route(
        "/company/edit-job/<int:job_id>",
        methods=["GET", "POST"]
    )
    @company_required
    def edit_job(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE id = ?
            AND company_id = ?
        """, (
            job_id,
            session["company_id"]
        ))

        job = cursor.fetchone()

        if job is None:

            conn.close()

            flash(
                "Job Not Found!",
                "danger"
            )

            return redirect("/company/my-jobs")

        if request.method == "POST":

            title = request.form.get("title", "").strip()
            category = request.form.get("category", "").strip()
            location = request.form.get("location", "").strip()
            job_type = request.form.get("job_type", "").strip()
            salary = request.form.get("salary", "").strip()
            experience = request.form.get("experience", "").strip()
            vacancies = request.form.get("vacancies", "").strip()
            last_date = request.form.get("last_date", "").strip()
            skills = request.form.get("skills", "").strip()
            description = request.form.get("description", "").strip()

            cursor.execute("""
                UPDATE jobs

                SET
                    title = ?,
                    category = ?,
                    location = ?,
                    job_type = ?,
                    salary = ?,
                    experience = ?,
                    vacancies = ?,
                    last_date = ?,
                    skills = ?,
                    description = ?

                WHERE id = ?
                AND company_id = ?
            """, (
                title,
                category,
                location,
                job_type,
                salary,
                experience,
                vacancies,
                last_date,
                skills,
                description,
                job_id,
                session["company_id"]
            ))

            conn.commit()
            conn.close()

            flash(
                "Job Updated Successfully!",
                "success"
            )

            return redirect("/company/my-jobs")

        conn.close()

        return render_template(
            "edit_job.html",
            job=job
        )


    # ==========================================================
    # DELETE JOB
    # ==========================================================

    @app.route("/company/delete-job/<int:job_id>")
    @company_required
    def delete_job(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM jobs
            WHERE id = ?
            AND company_id = ?
        """, (
            job_id,
            session["company_id"]
        ))

        job = cursor.fetchone()

        if job is None:

            conn.close()

            flash(
                "Job Not Found!",
                "danger"
            )

            return redirect("/company/my-jobs")

        cursor.execute("""
            DELETE FROM jobs
            WHERE id = ?
            AND company_id = ?
        """, (
            job_id,
            session["company_id"]
        ))

        conn.commit()
        conn.close()

        flash(
            "Job Deleted Successfully!",
            "success"
        )

        return redirect("/company/my-jobs")


    # ==========================================================
    # CHANGE JOB STATUS
    # ==========================================================

    @app.route(
        "/company/job-status/<int:job_id>/<status>"
    )
    @company_required
    def job_status(job_id, status):

        if status not in ["Active", "Inactive"]:

            flash(
                "Invalid Status!",
                "danger"
            )

            return redirect("/company/my-jobs")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE jobs

            SET status = ?

            WHERE id = ?
            AND company_id = ?
        """, (
            status,
            job_id,
            session["company_id"]
        ))

        conn.commit()
        conn.close()

        flash(
            f"Job marked as {status}.",
            "success"
        )

        return redirect("/company/my-jobs")


    # ==========================================================
    # COMPANY APPLICANTS
    # ==========================================================

    @app.route("/company/applicants")
    @company_required
    def company_applicants():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.id,
                applications.status,
                applications.apply_date,

                students.firstname || ' ' ||
                students.lastname AS fullname,

                students.email,
                students.mobile,
                students.resume,

                jobs.title

            FROM applications

            JOIN students
                ON applications.student_id = students.id

            JOIN jobs
                ON applications.job_id = jobs.id

            WHERE applications.company_id = ?

            ORDER BY applications.id DESC
        """, (session["company_id"],))

        applicants = cursor.fetchall()

        conn.close()

        return render_template(
            "company_applicants.html",
            applicants=applicants
        )


    # ==========================================================
    # JOB APPLICANTS
    # ==========================================================

    @app.route(
        "/company/job-applicants/<int:job_id>"
    )
    @company_required
    def job_applicants(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.id,
                applications.status,
                applications.apply_date,

                students.firstname || ' ' ||
                students.lastname AS fullname,

                students.email,
                students.mobile,
                students.resume,

                jobs.title

            FROM applications

            JOIN students
                ON applications.student_id = students.id

            JOIN jobs
                ON applications.job_id = jobs.id

            WHERE applications.company_id = ?
            AND applications.job_id = ?

            ORDER BY applications.id DESC
        """, (
            session["company_id"],
            job_id
        ))

        applicants = cursor.fetchall()

        conn.close()

        return render_template(
            "company_applicants.html",
            applicants=applicants
        )


    # ==========================================================
    # SHORTLISTED STUDENTS
    # ==========================================================

    @app.route("/company/shortlisted")
    @company_required
    def shortlisted_students():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.id,
                applications.status,
                applications.apply_date,

                students.firstname || ' ' ||
                students.lastname AS fullname,

                students.email,
                students.mobile,
                students.resume,

                jobs.title

            FROM applications

            JOIN students
                ON applications.student_id = students.id

            JOIN jobs
                ON applications.job_id = jobs.id

            WHERE applications.company_id = ?
            AND applications.status = 'Accepted'

            ORDER BY applications.id DESC
        """, (session["company_id"],))

        applicants = cursor.fetchall()

        conn.close()

        return render_template(
            "shortlisted.html",
            applicants=applicants
        )


    # ==========================================================
    # REJECTED STUDENTS
    # ==========================================================

    @app.route("/company/rejected")
    @company_required
    def rejected_students():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.id,
                applications.status,
                applications.apply_date,

                students.firstname || ' ' ||
                students.lastname AS fullname,

                students.email,
                students.mobile,
                students.resume,

                jobs.title

            FROM applications

            JOIN students
                ON applications.student_id = students.id

            JOIN jobs
                ON applications.job_id = jobs.id

            WHERE applications.company_id = ?
            AND applications.status = 'Rejected'

            ORDER BY applications.id DESC
        """, (session["company_id"],))

        applicants = cursor.fetchall()

        conn.close()

        return render_template(
            "rejected.html",
            applicants=applicants
        )


    # ==========================================================
    # SCHEDULE TEST / INTERVIEW
    # ==========================================================

    @app.route(
        "/company/schedule-selection/<int:application_id>",
        methods=["GET", "POST"]
    )
    @company_required
    def schedule_selection(application_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                applications.id,
                applications.status,
                applications.student_id,
                applications.job_id,
                students.firstname || ' ' || students.lastname AS fullname,
                students.email,
                jobs.title
            FROM applications
            JOIN students ON applications.student_id = students.id
            JOIN jobs ON applications.job_id = jobs.id
            WHERE applications.id = ?
            AND applications.company_id = ?
        """, (application_id, session["company_id"]))

        application = cursor.fetchone()

        if application is None:
            conn.close()
            flash("Application Not Found!", "danger")
            return redirect("/company/applicants")

        if application["status"] != "Accepted":
            conn.close()
            flash("Only accepted students can be scheduled.", "warning")
            return redirect("/company/applicants")

        if request.method == "POST":
            event_type = request.form.get("event_type", "").strip()
            title = request.form.get("title", "").strip()
            event_date = request.form.get("event_date", "").strip()
            event_time = request.form.get("event_time", "").strip()
            meeting_link = request.form.get("meeting_link", "").strip()
            message = request.form.get("message", "").strip()

            if event_type not in ("Interview", "Test"):
                flash("Please select Interview or Test.", "danger")
                conn.close()
                return redirect(url_for("schedule_selection", application_id=application_id))

            if not title or not event_date or not event_time:
                flash("Title, date and time are required.", "danger")
                conn.close()
                return redirect(url_for("schedule_selection", application_id=application_id))

            cursor.execute("""
                INSERT INTO selection_events
                (
                    application_id,
                    company_id,
                    student_id,
                    job_id,
                    event_type,
                    title,
                    event_date,
                    event_time,
                    meeting_link,
                    message,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Scheduled')
            """, (
                application_id,
                session["company_id"],
                application["student_id"],
                application["job_id"],
                event_type,
                title,
                event_date,
                event_time,
                meeting_link,
                message
            ))

            conn.commit()
            conn.close()

            flash(
                f"{event_type} scheduled successfully for {application['fullname']}.",
                "success"
            )
            return redirect("/company/applicants")

        cursor.execute("""
            SELECT *
            FROM selection_events
            WHERE application_id = ?
            AND company_id = ?
            ORDER BY id DESC
        """, (application_id, session["company_id"]))

        events = cursor.fetchall()
        conn.close()

        return render_template(
            "schedule_selection.html",
            application=application,
            events=events
        )


    # ==========================================================
    # UPDATE APPLICATION STATUS
    # ==========================================================

    @app.route(
        "/company/application-status/"
        "<int:application_id>/<status>"
    )
    @company_required
    def application_status(
        application_id,
        status
    ):

        if status not in ["Accepted", "Rejected"]:

            flash(
                "Invalid Status!",
                "danger"
            )

            return redirect(
                "/company/applicants"
            )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM applications
            WHERE id = ?
            AND company_id = ?
        """, (
            application_id,
            session["company_id"]
        ))

        application = cursor.fetchone()

        if application is None:

            conn.close()

            flash(
                "Application Not Found!",
                "danger"
            )

            return redirect(
                "/company/applicants"
            )

        cursor.execute("""
            UPDATE applications

            SET status = ?

            WHERE id = ?
        """, (
            status,
            application_id
        ))

        conn.commit()
        conn.close()

        flash(
            f"Application {status} Successfully!",
            "success"
        )

        return redirect(
            "/company/applicants"
        )


    # ==========================================================
    # COMPANY PROFILE
    # ==========================================================

    @app.route(
        "/company/profile",
        methods=["GET", "POST"]
    )
    @company_required
    def company_profile():

        conn = get_connection()
        cursor = conn.cursor()

        company_id = session["company_id"]

        # ------------------------------------------------------
        # Load Company
        # ------------------------------------------------------

        cursor.execute("""
            SELECT *
            FROM companies
            WHERE id = ?
        """, (company_id,))

        company = cursor.fetchone()

        # ------------------------------------------------------
        # Update Profile
        # ------------------------------------------------------

        if request.method == "POST":

            # --------------------------------------------------
            # Company Logo
            # --------------------------------------------------

            if "logo" in request.files:

                logo = request.files["logo"]

                if logo and logo.filename != "":

                    filename = (
                        f"{company_id}_"
                        f"{int(time_module.time())}_"
                        f"{secure_filename(logo.filename)}"
                    )

                    upload_folder = os.path.join(
                        current_app.root_path,
                        "static",
                        "uploads",
                        "company_logos"
                    )

                    os.makedirs(
                        upload_folder,
                        exist_ok=True
                    )

                    logo.save(
                        os.path.join(
                            upload_folder,
                            filename
                        )
                    )

                    cursor.execute("""
                        UPDATE companies
                        SET logo = ?
                        WHERE id = ?
                    """, (
                        filename,
                        company_id
                    ))

                    conn.commit()

                    session["company_logo"] = filename

                    flash(
                        "Company Logo Uploaded Successfully!",
                        "success"
                    )

                    return redirect(
                        "/company/profile"
                    )

            # --------------------------------------------------
            # Company Information
            # --------------------------------------------------

            if "company_name" in request.form:

                company_name = request.form.get(
                    "company_name",
                    ""
                ).strip()

                email = request.form.get(
                    "email",
                    ""
                ).strip()

                website = request.form.get(
                    "website",
                    ""
                ).strip()

                phone = request.form.get(
                    "phone",
                    ""
                ).strip()

                address = request.form.get(
                    "address",
                    ""
                ).strip()

                description = request.form.get(
                    "description",
                    ""
                ).strip()

                cursor.execute("""
                    UPDATE companies

                    SET
                        company_name = ?,
                        email = ?,
                        website = ?,
                        phone = ?,
                        address = ?,
                        description = ?

                    WHERE id = ?
                """, (
                    company_name,
                    email,
                    website,
                    phone,
                    address,
                    description,
                    company_id
                ))

                conn.commit()

                flash(
                    "Company Profile Updated Successfully!",
                    "success"
                )

                # Reload updated company

                cursor.execute("""
                    SELECT *
                    FROM companies
                    WHERE id = ?
                """, (company_id,))

                company = cursor.fetchone()

        conn.close()

        return render_template(
            "company_profile.html",
            company=company
        )


    # ==========================================================
    # COMPANY GOOGLE LOGIN
    # ==========================================================

    @app.route(
        "/company/google-login",
        methods=["POST"]
    )
    def company_google_login():

        data = request.get_json(
            silent=True
        ) or {}

        token = data.get("token")

        if not token:

            return jsonify({
                "success": False,
                "message": "Google token is required."
            }), 400

        try:

            decoded = auth.verify_id_token(
                token
            )

            google_id = decoded["uid"]

            email = decoded["email"]

            company_name = decoded.get(
                "name",
                "Company"
            )

            conn = get_connection()
            cursor = conn.cursor()

            # --------------------------------------------------
            # Find Company By Email
            # --------------------------------------------------

            cursor.execute("""
                SELECT *
                FROM companies
                WHERE email = ?
            """, (email,))

            company = cursor.fetchone()

            # --------------------------------------------------
            # Existing Company
            # --------------------------------------------------

            if company:

                if not company["google_id"]:

                    cursor.execute("""
                        UPDATE companies

                        SET google_id = ?

                        WHERE id = ?
                    """, (
                        google_id,
                        company["id"]
                    ))

                    conn.commit()

                session.clear()

                session["company_id"] = company["id"]

                session["company_name"] = (
                    company["company_name"]
                )

                session["company_email"] = (
                    company["email"]
                )

                session["company_logo"] = (
                    company["logo"]
                )

            # --------------------------------------------------
            # New Company
            # --------------------------------------------------

            else:

                cursor.execute("""
                    INSERT INTO companies
                    (
                        company_name,
                        email,
                        password,
                        google_id
                    )

                    VALUES (?, ?, ?, ?)
                """, (
                    company_name,
                    email,
                    generate_password_hash(
                        "GOOGLE_LOGIN"
                    ),
                    google_id
                ))

                conn.commit()

                company_id = cursor.lastrowid

                session.clear()

                session["company_id"] = company_id

                session["company_name"] = (
                    company_name
                )

                session["company_email"] = (
                    email
                )

                session["company_logo"] = (
                    "default.png"
                )

            conn.close()

            return jsonify({
                "success": True,
                "redirect": "/company/dashboard"
            })

        except Exception as e:

            return jsonify({
                "success": False,
                "message": str(e)
            }), 500