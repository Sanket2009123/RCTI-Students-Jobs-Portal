from flask import render_template, request, redirect, session, flash, url_for
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

import random
import time
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from authlib.integrations.flask_client import OAuth

from config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD
)


# =========================================================
# SEND OTP
# =========================================================

def send_otp(email, otp):

    message = MIMEMultipart()

    message["From"] = EMAIL_ADDRESS
    message["To"] = email
    message["Subject"] = "RCTI Students Jobs Portal - Password Reset OTP"

    body = f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Regards,
RCTI Students Jobs Portal
"""

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(
        EMAIL_HOST,
        EMAIL_PORT
    )

    server.starttls()

    server.login(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
    )

    server.send_message(message)

    server.quit()


# =========================================================
# REGISTER AUTH ROUTES
# =========================================================

def register_auth_routes(app):

    # =====================================================
    # STUDENT REGISTER
    # =====================================================

    @app.route("/student/register", methods=["GET", "POST"])
    def student_register():

        if request.method == "POST":

            firstname = request.form["firstname"]
            lastname = request.form["lastname"]

            email = request.form["email"]
            mobile = request.form["mobile"]
            college = request.form["college"]
            branch = request.form["branch"]
            semester = request.form["semester"]
            skills = request.form["skills"]

            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            # ---------------------------------------------
            # Password Confirmation
            # ---------------------------------------------

            if password != confirm_password:

                flash(
                    "Invalid Confirm Password!",
                    "danger"
                )

                return render_template(
                    "student_register.html"
                )

            # ---------------------------------------------
            # Password Hash
            # ---------------------------------------------

            password = generate_password_hash(password)

            conn = get_connection()
            cursor = conn.cursor()

            # ---------------------------------------------
            # Check Email
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE email=?
                """,
                (email,)
            )

            student = cursor.fetchone()

            if student:

                conn.close()

                flash(
                    "Email already exists.",
                    "danger"
                )

                return render_template(
                    "student_register.html"
                )

            # ---------------------------------------------
            # Insert Student
            # ---------------------------------------------

            cursor.execute(
                """
                INSERT INTO students
                (
                    firstname,
                    lastname,
                    email,
                    mobile,
                    college,
                    branch,
                    semester,
                    skills,
                    password
                )

                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    firstname,
                    lastname,
                    email,
                    mobile,
                    college,
                    branch,
                    semester,
                    skills,
                    password
                )
            )

            conn.commit()
            conn.close()

            flash(
                "Registration Successful! Please Login.",
                "success"
            )

            return redirect(
                "/student/login"
            )

        return render_template(
            "student_register.html"
        )


    # =====================================================
    # STUDENT LOGIN
    # =====================================================

    @app.route("/student/login", methods=["GET", "POST"])
    def student_login():

        if request.method == "POST":

            email = request.form["email"]
            password = request.form["password"]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE email=?
                """,
                (email,)
            )

            student = cursor.fetchone()

            conn.close()

            if student and check_password_hash(
                student["password"],
                password
            ):

                session.clear()

                session["student_id"] = student["id"]

                session["student_name"] = (
                    student["firstname"]
                    + " "
                    + student["lastname"]
                )

                session["student_email"] = student["email"]

                session["student_photo"] = student["profile_photo"]

                # -----------------------------------------
                # Redirect after Job Apply
                # -----------------------------------------

                next_job = (
                    request.args.get("next")
                    or request.form.get("next")
                )

                if next_job:

                    return redirect(
                        f"/student/apply/{next_job}"
                    )

                return redirect(
                    "/student/dashboard"
                )

            flash(
                "Incorrect Email or Password!",
                "danger"
            )

            return render_template(
                "student_login.html"
            )

        return render_template(
            "student_login.html"
        )


    # =====================================================
    # STUDENT FORGOT PASSWORD
    # =====================================================

    @app.route(
        "/student/forgot-password",
        methods=["GET", "POST"]
    )
    def student_forgot_password():

        if request.method == "POST":

            email = request.form["email"]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE email=?
                """,
                (email,)
            )

            student = cursor.fetchone()

            conn.close()

            if student:

                otp = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                session["reset_email"] = email
                session["reset_otp"] = otp
                session["otp_time"] = time.time()
                session["user_type"] = "student"

                send_otp(
                    student["email"],
                    otp
                )

                flash(
                    "OTP sent successfully to your registered email.",
                    "success"
                )

                return redirect(
                    url_for("verify_otp")
                )

            flash(
                "Email not registered.",
                "danger"
            )

        return render_template(
            "forgot_password.html"
        )


    # =====================================================
    # VERIFY OTP
    # =====================================================

    @app.route(
        "/student/verify-otp",
        methods=["GET", "POST"]
    )
    def verify_otp():

        if request.method == "POST":

            user_otp = request.form["otp"]

            # ---------------------------------------------
            # OTP Exists
            # ---------------------------------------------

            if "reset_otp" not in session:

                flash(
                    "OTP expired. Please try again.",
                    "danger"
                )

                return redirect(
                    url_for("student_forgot_password")
                )

            # ---------------------------------------------
            # OTP Time
            # ---------------------------------------------

            if (
                time.time()
                - session["otp_time"]
                > 300
            ):

                session.clear()

                flash(
                    "OTP expired.",
                    "danger"
                )

                return redirect(
                    url_for("student_forgot_password")
                )

            # ---------------------------------------------
            # Verify OTP
            # ---------------------------------------------

            if user_otp == session["reset_otp"]:

                flash(
                    "OTP verified successfully.",
                    "success"
                )

                if session.get("user_type") == "company":

                    return redirect(
                        url_for("company_reset_password")
                    )

                return redirect(
                    url_for("student_reset_password")
                )

            flash(
                "Invalid OTP.",
                "danger"
            )

        return render_template(
            "verify_otp.html"
        )


    # =====================================================
    # STUDENT RESET PASSWORD
    # =====================================================

    @app.route(
        "/student/reset-password",
        methods=["GET", "POST"]
    )
    def student_reset_password():

        if "reset_email" not in session:

            flash(
                "Session expired.",
                "danger"
            )

            return redirect(
                url_for("student_forgot_password")
            )

        if request.method == "POST":

            password = request.form["password"]
            confirm = request.form["confirm_password"]

            if password != confirm:

                flash(
                    "Passwords do not match.",
                    "danger"
                )

                return render_template(
                    "reset_password.html"
                )

            password = generate_password_hash(
                password
            )

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE students
                SET password=?
                WHERE email=?
                """,
                (
                    password,
                    session["reset_email"]
                )
            )

            conn.commit()
            conn.close()

            session.pop(
                "reset_email",
                None
            )

            session.pop(
                "reset_otp",
                None
            )

            session.pop(
                "otp_time",
                None
            )

            flash(
                "Password Updated Successfully.",
                "success"
            )

            return redirect(
                url_for("student_login")
            )

        return render_template(
            "reset_password.html"
        )


    # =====================================================
    # COMPANY REGISTER
    # =====================================================

    @app.route(
        "/company/register",
        methods=["GET", "POST"]
    )
    def company_register():

        if request.method == "POST":

            company_name = request.form["company_name"]
            hr_name = request.form["hr_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            website = request.form["website"]
            address = request.form["address"]

            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password:

                flash(
                    "Invalid Confirm Password!",
                    "danger"
                )

                return render_template(
                    "company_register.html"
                )

            password = generate_password_hash(
                password
            )

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM companies
                WHERE email=?
                """,
                (email,)
            )

            company = cursor.fetchone()

            if company:

                conn.close()

                flash(
                    "Company Email Already Registered",
                    "danger"
                )

                return render_template(
                    "company_register.html"
                )

            cursor.execute(
                """
                INSERT INTO companies
                (
                    company_name,
                    hr_name,
                    email,
                    phone,
                    website,
                    address,
                    password
                )

                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    company_name,
                    hr_name,
                    email,
                    phone,
                    website,
                    address,
                    password
                )
            )

            conn.commit()
            conn.close()

            flash(
                "Company Registered Successfully! Please Login.",
                "success"
            )

            return redirect(
                url_for("company_login")
            )

        return render_template(
            "company_register.html"
        )


    # =====================================================
    # COMPANY LOGIN
    # =====================================================

    @app.route(
        "/company/login",
        methods=["GET", "POST"]
    )
    def company_login():

        if request.method == "POST":

            email = request.form["email"]
            password = request.form["password"]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM companies
                WHERE email=?
                """,
                (email,)
            )

            company = cursor.fetchone()

            conn.close()

            if company and check_password_hash(
                company["password"],
                password
            ):

                session.clear()

                session["company_id"] = company["id"]

                session["company_name"] = company["company_name"]

                session["company_email"] = company["email"]

                session["company_logo"] = company["logo"]

                return redirect(
                    "/company/dashboard"
                )

            flash(
                "Incorrect Email or Password!",
                "danger"
            )

            return render_template(
                "company_login.html"
            )

        return render_template(
            "company_login.html"
        )


    # =====================================================
    # COMPANY FORGOT PASSWORD
    # =====================================================

    @app.route(
        "/company/forgot-password",
        methods=["GET", "POST"]
    )
    def company_forgot_password():

        if request.method == "POST":

            email = request.form["email"]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM companies
                WHERE email=?
                """,
                (email,)
            )

            company = cursor.fetchone()

            conn.close()

            if company:

                otp = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                session["reset_email"] = email
                session["reset_otp"] = otp
                session["otp_time"] = time.time()
                session["user_type"] = "company"

                send_otp(
                    email,
                    otp
                )

                flash(
                    "OTP sent successfully to your registered email.",
                    "success"
                )

                return redirect(
                    url_for("verify_otp")
                )

            flash(
                "Email not registered.",
                "danger"
            )

        return render_template(
            "forgot_password.html"
        )


    # =====================================================
    # COMPANY RESET PASSWORD
    # =====================================================

    @app.route(
        "/company/reset-password",
        methods=["GET", "POST"]
    )
    def company_reset_password():

        if "reset_email" not in session:

            flash(
                "Session expired.",
                "danger"
            )

            return redirect(
                url_for("company_forgot_password")
            )

        if request.method == "POST":

            password = request.form["password"]
            confirm = request.form["confirm_password"]

            if password != confirm:

                flash(
                    "Passwords do not match.",
                    "danger"
                )

                return render_template(
                    "reset_password.html"
                )

            password = generate_password_hash(
                password
            )

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE companies
                SET password=?
                WHERE email=?
                """,
                (
                    password,
                    session["reset_email"]
                )
            )

            conn.commit()
            conn.close()

            session.pop(
                "reset_email",
                None
            )

            session.pop(
                "reset_otp",
                None
            )

            session.pop(
                "otp_time",
                None
            )

            flash(
                "Password Updated Successfully.",
                "success"
            )

            return redirect(
                url_for("company_login")
            )

        return render_template(
            "reset_password.html"
        )


    # =====================================================
    # STUDENT LOGOUT
    # =====================================================

    @app.route("/student/logout")
    def student_logout():

        session.clear()

        flash(
            "Logged out successfully.",
            "success"
        )

        response = redirect("/")

        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

        response.headers["Pragma"] = "no-cache"

        response.headers["Expires"] = "0"

        return response


    # =====================================================
    # COMPANY LOGOUT
    # =====================================================

    @app.route("/company/logout")
    def company_logout():

        session.clear()

        flash(
            "Logged out successfully.",
            "success"
        )

        response = redirect("/")

        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )

        response.headers["Pragma"] = "no-cache"

        response.headers["Expires"] = "0"

        return response


    # =====================================================
    # ADMIN LOGIN
    # =====================================================

    @app.route(
        "/admin/login",
        methods=["GET", "POST"]
    )
    def admin_login():

        if request.method == "POST":

            email = request.form["email"]

            password = request.form["password"]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM admins
                WHERE email=?
                """,
                (email,)
            )

            admin = cursor.fetchone()

            conn.close()

            if admin and check_password_hash(
                admin["password"],
                password
            ):

                session["admin_id"] = admin["id"]

                session["admin_name"] = admin["name"]

                return redirect(
                    "/admin/dashboard"
                )

            return "<h3>Invalid Email or Password</h3>"

        return render_template("admin_login.html")