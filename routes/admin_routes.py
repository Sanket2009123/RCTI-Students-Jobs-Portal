from flask import render_template, request, redirect, session, flash
from database.db import get_connection
from utils.decorators import admin_required


def register_admin_routes(app):
        # ==========================
    # Admin Dashboard
    # ==========================

    @app.route("/admin/dashboard")
    @admin_required
    def admin_dashboard():

        conn = get_connection()
        cursor = conn.cursor()

        # Total Students
        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

        # Total Companies
        cursor.execute("SELECT COUNT(*) AS total FROM companies")
        total_companies = cursor.fetchone()["total"]

        # Total Jobs
        cursor.execute("SELECT COUNT(*) AS total FROM jobs")
        total_jobs = cursor.fetchone()["total"]

        # Total Applications
        cursor.execute("SELECT COUNT(*) AS total FROM applications")
        total_applications = cursor.fetchone()["total"]
    # ==========================
    # Recent Activities
    # ==========================

        cursor.execute("""
            SELECT
                activity_date,
                activity,
                user_name,
                status
            FROM (

                SELECT
                    students.created_at AS activity_date,
                    'Student Registered' AS activity,
                    students.firstname || ' ' || students.lastname AS user_name,
                    'Registered' AS status
                FROM students

                UNION ALL

                SELECT
                    companies.created_at AS activity_date,
                    'New Company Registered' AS activity,
                    companies.company_name AS user_name,
                    companies.status AS status
                FROM companies

                UNION ALL

                SELECT
                    jobs.created_at AS activity_date,
                    'New Job Posted' AS activity,
                    companies.company_name AS user_name,
                    jobs.status AS status
                FROM jobs
                JOIN companies
                    ON jobs.company_id = companies.id

                UNION ALL

                SELECT
                    applications.apply_date AS activity_date,
                    'Application Submitted' AS activity,
                    students.firstname || ' ' || students.lastname AS user_name,
                    applications.status AS status
                FROM applications
                JOIN students
                    ON applications.student_id = students.id

            )
            ORDER BY datetime(activity_date) DESC
            LIMIT 5
        """)

        recent_activities = cursor.fetchall()
        # ==========================
        # Jobs by Category
        # ==========================

        cursor.execute("""

            SELECT
                category,
                COUNT(*) AS total

            FROM jobs

            GROUP BY category

        """)

        category_data = cursor.fetchall()

        categories = []
        category_count = []

        for row in category_data:
            categories.append(row["category"])
            category_count.append(row["total"])
    # ==========================
    # ANALYTICS DATA
    # ==========================

        # Student registrations by date
        cursor.execute("""
            SELECT
                DATE(created_at) AS date,
                COUNT(*) AS total
            FROM students
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """)

        student_data = cursor.fetchall()

        analytics_dates = []
        student_counts = []

        for row in student_data:
            analytics_dates.append(row["date"])
            student_counts.append(row["total"])


        # Company registrations by date
        cursor.execute("""
            SELECT
                DATE(created_at) AS date,
                COUNT(*) AS total
            FROM companies
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """)

        company_data = cursor.fetchall()

        company_counts = []

        for row in company_data:
            company_counts.append(row["total"])


        # Jobs posted by date
        cursor.execute("""
            SELECT
                DATE(created_at) AS date,
                COUNT(*) AS total
            FROM jobs
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """)

        job_data = cursor.fetchall()

        job_counts = []

        for row in job_data:
            job_counts.append(row["total"])


        # Applications by date
        cursor.execute("""
            SELECT
                DATE(apply_date) AS date,
                COUNT(*) AS total
            FROM applications
            WHERE apply_date IS NOT NULL
            GROUP BY DATE(apply_date)
            ORDER BY DATE(apply_date)
        """)

        application_data = cursor.fetchall()

        application_counts = []

        for row in application_data:
            application_counts.append(row["total"])
        conn.close()

        return render_template(
            "admin_dashboard.html",

            total_students=total_students,
            total_companies=total_companies,
            total_jobs=total_jobs,
            total_applications=total_applications,

            categories=categories,
            category_count=category_count,

            analytics_dates=analytics_dates,
            student_counts=student_counts,
            company_counts=company_counts,
            job_counts=job_counts,
            application_counts=application_counts
        )
        # ==========================
    # Manage Students
    # ==========================

    @app.route("/admin/students")
    @admin_required
    def manage_students():

        conn = get_connection()
        cursor = conn.cursor()

        search = request.args.get("search", "").strip()

        if search:

            cursor.execute("""

                SELECT *

                FROM students

                WHERE

                    fullname LIKE ?
                    OR email LIKE ?
                    OR mobile LIKE ?

                ORDER BY id DESC

            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""

                SELECT *

                FROM students

                ORDER BY id DESC

            """)

        students = cursor.fetchall()

        conn.close()

        return render_template(
            "manage_students.html",
            students=students,
            search=search
        )
        # ==========================
    # Delete Student
    # ==========================

    @app.route("/admin/delete-student/<int:student_id>")
    @admin_required
    def delete_student(student_id):

        conn = get_connection()
        cursor = conn.cursor()

        # Check Student Exists
        cursor.execute("""
            SELECT id
            FROM students
            WHERE id=?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            conn.close()
            flash("Student Not Found!", "danger")
            return redirect("/admin/students")

        # Delete Student Applications
        cursor.execute("""
            DELETE FROM applications
            WHERE student_id=?
        """, (student_id,))

        # Delete Student
        cursor.execute("""
            DELETE FROM students
            WHERE id=?
        """, (student_id,))

        conn.commit()
        conn.close()

        flash("Student Deleted Successfully!", "success")

        return redirect("/admin/students")
        # ==========================
    # Manage Companies
    # ==========================

    @app.route("/admin/companies")
    @admin_required
    def manage_companies():

        conn = get_connection()
        cursor = conn.cursor()

        search = request.args.get("search", "").strip()

        if search:

            cursor.execute("""

                SELECT *

                FROM companies

                WHERE

                    company_name LIKE ?
                    OR email LIKE ?
                    OR location LIKE ?

                ORDER BY id DESC

            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""

                SELECT *

                FROM companies

                ORDER BY id DESC

            """)

        companies = cursor.fetchall()

        conn.close()

        return render_template(
            "manage_companies.html",
            companies=companies,
            search=search
        )
        # ==========================
    # Delete Company
    # ==========================

    @app.route("/admin/delete-company/<int:company_id>")
    @admin_required
    def delete_company(company_id):

        conn = get_connection()
        cursor = conn.cursor()

        # Check Company Exists
        cursor.execute("""
            SELECT id
            FROM companies
            WHERE id=?
        """, (company_id,))

        company = cursor.fetchone()

        if company is None:
            conn.close()
            flash("Company Not Found!", "danger")
            return redirect("/admin/companies")

        # Delete Applications of Company
        cursor.execute("""
            DELETE FROM applications
            WHERE company_id=?
        """, (company_id,))

        # Delete Jobs of Company
        cursor.execute("""
            DELETE FROM jobs
            WHERE company_id=?
        """, (company_id,))

        # Delete Company
        cursor.execute("""
            DELETE FROM companies
            WHERE id=?
        """, (company_id,))

        conn.commit()
        conn.close()

        flash("Company Deleted Successfully!", "success")

        return redirect("/admin/companies")
    # ==========================
    # Manage Jobs
    # ==========================

    @app.route("/admin/jobs")
    @admin_required
    def manage_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        search = request.args.get("search", "").strip()

        if search:

            cursor.execute("""

                SELECT

                    jobs.*,
                    companies.company_name

                FROM jobs

                JOIN companies
                ON jobs.company_id = companies.id

                WHERE

                    jobs.title LIKE ?
                    OR companies.company_name LIKE ?
                    OR jobs.location LIKE ?

                ORDER BY jobs.id DESC

            """, (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cursor.execute("""

                SELECT

                    jobs.*,
                    companies.company_name

                FROM jobs

                JOIN companies
                ON jobs.company_id = companies.id

                ORDER BY jobs.id DESC

            """)

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "manage_jobs.html",
            jobs=jobs,
            search=search
        )
        # ==========================
    # Delete Job (Admin)
    # ==========================

    @app.route("/admin/delete-job/<int:job_id>")
    @admin_required
    def delete_job_admin(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        # Check Job Exists
        cursor.execute("""
            SELECT id
            FROM jobs
            WHERE id=?
        """, (job_id,))

        job = cursor.fetchone()

        if job is None:
            conn.close()
            flash("Job Not Found!", "danger")
            return redirect("/admin/jobs")

        # Delete Applications of this Job
        cursor.execute("""
            DELETE FROM applications
            WHERE job_id=?
        """, (job_id,))

        # Delete Job
        cursor.execute("""
            DELETE FROM jobs
            WHERE id=?
        """, (job_id,))

        conn.commit()
        conn.close()

        flash("Job Deleted Successfully!", "success")

        return redirect("/admin/jobs")
        # ==========================
    # Manage Applications
    # ==========================

    @app.route("/admin/applications")
    @admin_required
    def manage_applications():

        conn = get_connection()
        cursor = conn.cursor()

        search = request.args.get("search", "").strip()

        query = """

            SELECT
                applications.id,
                applications.apply_date,
                applications.status,

                students.firstname,
                students.lastname,
                students.email,

                companies.company_name,

                jobs.title

            FROM applications

            JOIN students
            ON applications.student_id = students.id

            JOIN companies
            ON applications.company_id = companies.id

            JOIN jobs
            ON applications.job_id = jobs.id

        """

        if search:

            query += """

                WHERE
                    students.firstname LIKE ?
                    OR students.lastname LIKE ?
                    OR students.email LIKE ?
                    OR companies.company_name LIKE ?
                    OR jobs.title LIKE ?

            """

            cursor.execute(
                query + " ORDER BY applications.id DESC",
                (
                    (
                        f"%{search}%",
                        f"%{search}%",
                        f"%{search}%",
                        f"%{search}%",
                        f"%{search}%"
)
                )
            )

        else:

            cursor.execute(query + " ORDER BY applications.id DESC")

        applications = cursor.fetchall()

        conn.close()

        return render_template(
            "manage_applications.html",
            applications=applications,
            search=search
        )
        # ==========================
    # Admin Reports
    # ==========================

    @app.route("/admin/reports")
    @admin_required
    def reports():

        conn = get_connection()
        cursor = conn.cursor()

        # --------------------------
        # Overall Statistics
        # --------------------------

        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM companies")
        total_companies = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM jobs")
        total_jobs = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM applications")
        total_applications = cursor.fetchone()["total"]

        # --------------------------
        # Recent Students
        # --------------------------

        cursor.execute("""
            SELECT
                id,
                firstname,
                lastname,
                email,
                created_at
            FROM students
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_students = cursor.fetchall()

        # --------------------------
        # Recent Companies
        # --------------------------

        cursor.execute("""
            SELECT
                id,
                company_name,
                email,
                status,
                created_at
            FROM companies
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_companies = cursor.fetchall()

        # --------------------------
        # Recent Jobs
        # --------------------------

        cursor.execute("""
            SELECT
                jobs.id,
                jobs.title,
                companies.company_name,
                jobs.status,
                jobs.created_at
            FROM jobs
            LEFT JOIN companies
                ON jobs.company_id = companies.id
            ORDER BY jobs.id DESC
            LIMIT 10
        """)

        recent_jobs = cursor.fetchall()

        # --------------------------
        # Recent Applications
        # --------------------------

        cursor.execute("""
            SELECT
                applications.id,
                students.firstname || ' ' || students.lastname AS student_name,
                jobs.title AS job_title,
                companies.company_name,
                applications.status,
                applications.apply_date
            FROM applications

            LEFT JOIN students
                ON applications.student_id = students.id

            LEFT JOIN jobs
                ON applications.job_id = jobs.id

            LEFT JOIN companies
                ON jobs.company_id = companies.id

            ORDER BY applications.id DESC
            LIMIT 10
        """)

        recent_applications = cursor.fetchall()

        conn.close()

        return render_template(
            "reports.html",

            total_students=total_students,
            total_companies=total_companies,
            total_jobs=total_jobs,
            total_applications=total_applications,

            recent_students=recent_students,
            recent_companies=recent_companies,
            recent_jobs=recent_jobs,
            recent_applications=recent_applications
        )
        # ==========================
    # Admin Logout
    # ==========================

    @app.route("/admin/logout")
    def admin_logout():

        session.pop("admin_id", None)

        flash("Admin logged out successfully!", "success")

        return redirect("/admin/login")
    # ==========================
    # Admin Home
    # ==========================

    @app.route("/admin")
    def admin_home():

        if "admin_id" in session:
            return redirect("/admin/dashboard")

        return redirect("/admin/login")