from flask import render_template, request
from database.db import get_connection

def register_main_routes(app):

    @app.route("/")
    def home():

        search = request.args.get("search", "").strip()

        conn = get_connection()
        cursor = conn.cursor()

        jobs = []

        if search:

            cursor.execute("""

                SELECT
                    jobs.*,
                    companies.company_name

                FROM jobs

                JOIN companies
                ON jobs.company_id = companies.id

                WHERE jobs.status='Active'

                AND
                (
                    jobs.title LIKE ?
                    OR jobs.location LIKE ?
                    OR companies.company_name LIKE ?
                )

            """, (

                f"%{search}%",
                f"%{search}%",
                f"%{search}%"

            ))

            jobs = cursor.fetchall()

        conn.close()

        return render_template(
            "index.html",
            jobs=jobs,
            search=search
        )


    @app.route("/about")
    def about():
        return render_template("about.html")


    @app.route("/contact")
    def contact():
        return render_template("contact.html")


    @app.route("/companies")
    def companies():
        return render_template("companies.html")