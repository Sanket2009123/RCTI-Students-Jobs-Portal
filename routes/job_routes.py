from flask import render_template, request
from database.db import get_connection
import math
def register_job_routes(app):
        # ==========================
    # All Jobs
    # ==========================

    @app.route("/jobs")
    def all_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        page = request.args.get("page", 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        search = request.args.get("search", "").strip()

        if search:

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM jobs
                WHERE status='Active'
                AND
                (
                    title LIKE ?
                    OR location LIKE ?
                )
            """, (
                f"%{search}%",
                f"%{search}%"
            ))

            total_jobs = cursor.fetchone()["total"]

            cursor.execute("""

                SELECT jobs.*, companies.company_name

                FROM jobs

                JOIN companies
                ON jobs.company_id = companies.id

                WHERE jobs.status='Active'

                AND
                (
                    jobs.title LIKE ?
                    OR jobs.location LIKE ?
                )

                ORDER BY jobs.id DESC

                LIMIT ? OFFSET ?

            """, (
                f"%{search}%",
                f"%{search}%",
                per_page,
                offset
            ))

        else:

            cursor.execute("""
                SELECT COUNT(*) AS total
                FROM jobs
                WHERE status='Active'
            """)
            total_jobs = cursor.fetchone()["total"]

            cursor.execute("""

                SELECT jobs.*, companies.company_name

                FROM jobs

                JOIN companies
                ON jobs.company_id = companies.id

                WHERE jobs.status='Active'

                ORDER BY jobs.id DESC

                LIMIT ? OFFSET ?

            """, (
                per_page,
                offset
            ))

        jobs = cursor.fetchall()

        conn.close()

        total_pages = math.ceil(total_jobs / per_page) if total_jobs else 1

        return render_template(

            "jobs.html",

            jobs=jobs,

            page=page,

            total_pages=total_pages,

            search=search

        )
        # ==========================
    # Public Job Details
    # ==========================

    @app.route("/jobs/<int:job_id>")
    def job_details_public(job_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                jobs.*,
                companies.company_name,
                companies.email,
                companies.location AS company_location

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            WHERE jobs.id=?

        """, (job_id,))

        job = cursor.fetchone()

        conn.close()

        if job is None:
            return render_template("404.html"), 404

        return render_template(
            "job_details.html",
            job=job
        )
        # ==========================
    # Jobs By Category
    # ==========================

    @app.route("/jobs/category/<category>")
    def jobs_by_category(category):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                jobs.*,
                companies.company_name

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            WHERE jobs.category=?

            ORDER BY jobs.id DESC

        """, (category,))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "jobs.html",
            jobs=jobs,
            category=category
        )
        # ==========================
    # Jobs By Location
    # ==========================

    @app.route("/jobs/location/<location>")
    def jobs_by_location(location):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                jobs.*,
                companies.company_name

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            WHERE jobs.location=?

            ORDER BY jobs.id DESC

        """, (location,))

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "jobs.html",
            jobs=jobs,
            location=location
        )
        # ==========================
    # Latest Jobs
    # ==========================

    @app.route("/latest-jobs")
    def latest_jobs():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                jobs.*,
                companies.company_name

            FROM jobs

            JOIN companies
            ON jobs.company_id = companies.id

            ORDER BY jobs.id DESC

            LIMIT 10

        """)

        jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "latest_jobs.html",
            jobs=jobs
        )