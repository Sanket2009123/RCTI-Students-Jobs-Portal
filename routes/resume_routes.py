from flask import (
    render_template,
    request,
    session,
    redirect,
    flash,
    url_for
)

from database.db import get_connection
from utils.decorators import student_required


def register_resume_routes(app):

    # ==========================================================
    # RESUME BUILDER
    # ==========================================================

    @app.route("/student/resume-builder")
    @student_required
    def resume_builder():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE id = ?
            """,
            (session["student_id"],)
        )

        student = cursor.fetchone()

        conn.close()

        return render_template(
            "resume_builder.html",
            student=student,
            resume=None,
            edit_mode=False
        )


    # ==========================================================
    # SAVE RESUME
    # ==========================================================

    @app.route(
        "/student/save-resume",
        methods=["POST"]
    )
    @student_required
    def save_resume():

        # ------------------------------------------------------
        # BASIC RESUME INFORMATION
        # ------------------------------------------------------

        resume_name = request.form.get(
            "resume_name",
            ""
        ).strip()

        fullname = request.form.get(
            "fullname",
            ""
        ).strip()

        template = request.form.get(
            "template",
            "ats"
        ).strip()

        objective = request.form.get(
            "objective",
            ""
        ).strip()

        linkedin = request.form.get(
            "linkedin",
            ""
        ).strip()

        github = request.form.get(
            "github",
            ""
        ).strip()

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        job_title = request.form.get(
            "job_title",
            ""
        ).strip()


        # ------------------------------------------------------
        # VALIDATE RESUME NAME
        # ------------------------------------------------------

        if not resume_name:

            flash(
                "Resume name is required.",
                "danger"
            )

            return redirect(
                url_for("resume_builder")
            )


        # ------------------------------------------------------
        # GET STUDENT NAME IF FULLNAME IS EMPTY
        # ------------------------------------------------------

        if not fullname:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT firstname, lastname
                FROM students
                WHERE id = ?
                """,
                (session["student_id"],)
            )

            student = cursor.fetchone()

            conn.close()

            if student:

                fullname = (
                    f"{student['firstname']} "
                    f"{student['lastname']}"
                ).strip()


        # ------------------------------------------------------
        # DATABASE CONNECTION
        # ------------------------------------------------------

        conn = get_connection()
        cursor = conn.cursor()


        try:

            # ==================================================
            # RESUME MASTER
            # ==================================================

            cursor.execute(
                """
                INSERT INTO resumes
                (
                    student_id,
                    resume_name,
                    fullname,
                    job_title,
                    template,
                    objective,
                    linkedin,
                    github,
                    portfolio
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session["student_id"],
                    resume_name,
                    fullname,
                    job_title,
                    template,
                    objective,
                    linkedin,
                    github,
                    portfolio
                )
            )

            resume_id = cursor.lastrowid


            # ==================================================
            # EDUCATION
            # ==================================================

            degrees = request.form.getlist(
                "education_degree[]"
            )

            colleges = request.form.getlist(
                "education_college[]"
            )

            years = request.form.getlist(
                "education_year[]"
            )

            cgpas = request.form.getlist(
                "education_cgpa[]"
            )


            for degree, college, year, cgpa in zip(
                degrees,
                colleges,
                years,
                cgpas
            ):

                if degree.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_education
                        (
                            resume_id,
                            degree,
                            college,
                            passing_year,
                            cgpa
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            degree.strip(),
                            college.strip(),
                            year.strip(),
                            cgpa.strip()
                        )
                    )


            # ==================================================
            # PROJECTS
            # ==================================================

            project_titles = request.form.getlist(
                "project_title[]"
            )

            project_descriptions = request.form.getlist(
                "project_description[]"
            )

            project_technologies = request.form.getlist(
                "project_technology[]"
            )


            for title, description, technology in zip(
                project_titles,
                project_descriptions,
                project_technologies
            ):

                if title.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_projects
                        (
                            resume_id,
                            title,
                            description,
                            technology
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            title.strip(),
                            description.strip(),
                            technology.strip()
                        )
                    )


            # ==================================================
            # EXPERIENCE
            # ==================================================

            companies = request.form.getlist(
                "company[]"
            )

            roles = request.form.getlist(
                "role[]"
            )

            durations = request.form.getlist(
                "duration[]"
            )

            experience_descriptions = request.form.getlist(
                "experience_description[]"
            )


            for company, role, duration, description in zip(
                companies,
                roles,
                durations,
                experience_descriptions
            ):

                if company.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_experience
                        (
                            resume_id,
                            company,
                            role,
                            duration,
                            description
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            company.strip(),
                            role.strip(),
                            duration.strip(),
                            description.strip()
                        )
                    )


            # ==================================================
            # SKILLS
            # ==================================================

            skills = request.form.get(
                "skills",
                ""
            ).strip()


            if skills:

                skill_list = skills.split(",")

                for skill in skill_list:

                    skill = skill.strip()

                    if skill:

                        cursor.execute(
                            """
                            INSERT INTO resume_skills
                            (
                                resume_id,
                                skill
                            )
                            VALUES (?, ?)
                            """,
                            (
                                resume_id,
                                skill
                            )
                        )


            # ==================================================
            # CERTIFICATES
            # ==================================================

            certificates = request.form.getlist(
                "certificate_name[]"
            )

            organizations = request.form.getlist(
                "certificate_org[]"
            )

            certificate_years = request.form.getlist(
                "certificate_year[]"
            )


            for certificate, organization, year in zip(
                certificates,
                organizations,
                certificate_years
            ):

                if certificate.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_certificates
                        (
                            resume_id,
                            certificate,
                            organization,
                            year
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            certificate.strip(),
                            organization.strip(),
                            year.strip()
                        )
                    )


            # ==================================================
            # LANGUAGES
            # ==================================================

            languages = request.form.getlist(
                "language[]"
            )


            for language in languages:

                language = language.strip()

                if language:

                    cursor.execute(
                        """
                        INSERT INTO resume_languages
                        (
                            resume_id,
                            language
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            language
                        )
                    )


            # ==================================================
            # ACHIEVEMENTS
            # ==================================================

            achievements = request.form.getlist(
                "achievement[]"
            )


            for achievement in achievements:

                achievement = achievement.strip()

                if achievement:

                    cursor.execute(
                        """
                        INSERT INTO resume_achievements
                        (
                            resume_id,
                            achievement
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            achievement
                        )
                    )


            # ==================================================
            # HOBBIES
            # ==================================================

            hobbies = request.form.getlist(
                "hobby[]"
            )


            for hobby in hobbies:

                hobby = hobby.strip()

                if hobby:

                    cursor.execute(
                        """
                        INSERT INTO resume_hobbies
                        (
                            resume_id,
                            hobby
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            hobby
                        )
                    )


            # ==================================================
            # COMMIT
            # ==================================================

            conn.commit()

            flash(
                "Resume Saved Successfully.",
                "success"
            )

            return redirect(
                url_for("my_resumes")
            )


        except Exception as e:

            conn.rollback()

            print(
                "Resume Save Error:",
                e
            )

            flash(
                "Something went wrong while saving resume.",
                "danger"
            )

            return redirect(
                url_for("resume_builder")
            )


        finally:

            conn.close()


    # ==========================================================
    # MY RESUMES
    # ==========================================================

    @app.route("/student/my-resumes")
    @student_required
    def my_resumes():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM resumes
            WHERE student_id = ?
            ORDER BY id DESC
            """,
            (
                session["student_id"],
            )
        )

        resumes = cursor.fetchall()

        conn.close()

        return render_template(
            "my_resumes.html",
            resumes=resumes
        )


    # ==========================================================
    # RESUME PREVIEW
    # ==========================================================

    @app.route("/resume/preview/<int:resume_id>")
    @student_required
    def resume_preview(resume_id):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM students WHERE id = ?",
                           (session["student_id"],))
            student = cursor.fetchone()

            if student is None:
                flash("Student record not found.", "danger")
                return redirect(url_for("my_resumes"))

            cursor.execute("""
                SELECT * FROM resumes
                WHERE id = ? AND student_id = ?
            """, (resume_id, session["student_id"]))
            resume = cursor.fetchone()

            if resume is None:
                flash("Resume not found.", "danger")
                return redirect(url_for("my_resumes"))

            def fetch(table):
                cursor.execute(
                    f"SELECT * FROM {table} WHERE resume_id = ? ORDER BY id ASC",
                    (resume_id,)
                )
                return cursor.fetchall()

            education = fetch("resume_education")
            projects = fetch("resume_projects")
            experience = fetch("resume_experience")
            skills = fetch("resume_skills")
            certificates = fetch("resume_certificates")
            languages = fetch("resume_languages")
            achievements = fetch("resume_achievements")
            hobbies = fetch("resume_hobbies")

            VALID_TEMPLATES = {
                "ats",
                "modern",
                "executive",
                "creative",
                "developer",
                "data",
                "minimal",
                "fresher"
            }

            selected_template = (
                resume["template"] or "ats"
            ).strip().lower()

            if selected_template not in VALID_TEMPLATES:
                selected_template = "ats"

            template_file = f"resumes/{selected_template}.html"

            return render_template(
                template_file,
                student=student,
                resume=resume,
                education=education,
                projects=projects,
                experience=experience,
                skills=skills,
                certificates=certificates,
                languages=languages,
                achievements=achievements,
                hobbies=hobbies,
                resume_id=resume_id,
                selected_template=selected_template
            )

        except Exception as e:
            print("Resume Preview Error:", e)
            flash("Unable to load resume preview.", "danger")
            return redirect(url_for("my_resumes"))

        finally:
            conn.close()


    # ==========================================================
    # RESUME DETAILS
    # ==========================================================
    # ==========================================================
# ATS RESUME ANALYZER
# ==========================================================

    @app.route(
        "/student/resume-ats/<int:resume_id>"
    )
    @student_required
    def resume_ats(resume_id):

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # --------------------------------------------------
            # GET RESUME
            # --------------------------------------------------

            cursor.execute(
                """
                SELECT *
                FROM resumes
                WHERE id = ?
                AND student_id = ?
                """,
                (
                    resume_id,
                    session["student_id"]
                )
            )

            resume = cursor.fetchone()

            if resume is None:

                flash(
                    "Resume not found.",
                    "danger"
                )

                return redirect(
                    url_for("my_resumes")
                )


            # --------------------------------------------------
            # GET STUDENT
            # --------------------------------------------------

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE id = ?
                """,
                (
                    session["student_id"],
                )
            )

            student = cursor.fetchone()


            # --------------------------------------------------
            # GET RESUME DATA
            # --------------------------------------------------

            def fetch(table):

                cursor.execute(
                    f"""
                    SELECT *
                    FROM {table}
                    WHERE resume_id = ?
                    ORDER BY id ASC
                    """,
                    (resume_id,)
                )

                return cursor.fetchall()


            education = fetch("resume_education")

            projects = fetch("resume_projects")

            experience = fetch("resume_experience")

            skills = fetch("resume_skills")

            certificates = fetch("resume_certificates")

            languages = fetch("resume_languages")

            achievements = fetch("resume_achievements")

            hobbies = fetch("resume_hobbies")


            # ==================================================
            # ATS SCORE
            # ==================================================

            score = 0

            suggestions = []

            strengths = []


            # --------------------------------------------------
            # PERSONAL / BASIC INFORMATION
            # --------------------------------------------------

            if student:

                fullname = student["fullname"] or ""
                email = student["email"] or ""
                mobile = student["mobile"] or ""

            else:

                fullname = ""
                email = ""
                mobile = ""


            if fullname and email and mobile:

                score += 15

                strengths.append(
                    "Complete contact information is available."
                )

            else:

                suggestions.append(
                    "Add complete name, email and mobile number."
                )


            # --------------------------------------------------
            # CAREER OBJECTIVE
            # --------------------------------------------------

            objective = resume["objective"] or ""

            if len(objective.strip()) >= 50:

                score += 10

                strengths.append(
                    "Career objective is clearly defined."
                )

            else:

                suggestions.append(
                    "Add a stronger career objective."
                )


            # --------------------------------------------------
            # SKILLS
            # --------------------------------------------------

            skill_count = len(skills)

            if skill_count >= 8:

                score += 20

                strengths.append(
                    "Good number of technical skills."
                )

            elif skill_count >= 4:

                score += 12

                suggestions.append(
                    "Consider adding more relevant technical skills."
                )

            else:

                score += 5

                suggestions.append(
                    "Add more job-relevant technical skills."
                )


            # --------------------------------------------------
            # EDUCATION
            # --------------------------------------------------

            if len(education) > 0:

                score += 10

                strengths.append(
                    "Education section is present."
                )

            else:

                suggestions.append(
                    "Add your educational qualifications."
                )


            # --------------------------------------------------
            # PROJECTS
            # --------------------------------------------------

            if len(projects) >= 2:

                score += 15

                strengths.append(
                    "Multiple projects demonstrate practical experience."
                )

            elif len(projects) == 1:

                score += 8

                suggestions.append(
                    "Add more projects to strengthen your resume."
                )

            else:

                suggestions.append(
                    "Add academic or personal projects."
                )


            # --------------------------------------------------
            # EXPERIENCE
            # --------------------------------------------------

            if len(experience) > 0:

                score += 10

                strengths.append(
                    "Work experience section is available."
                )

            else:

                suggestions.append(
                    "Add internship or work experience if available."
                )


            # --------------------------------------------------
            # CERTIFICATES
            # --------------------------------------------------

            if len(certificates) > 0:

                score += 5

                strengths.append(
                    "Certifications improve your profile."
                )

            else:

                suggestions.append(
                    "Add relevant certifications if available."
                )


            # --------------------------------------------------
            # PROFESSIONAL PROFILES
            # --------------------------------------------------

            profile_count = 0

            if resume["linkedin"]:
                profile_count += 1

            if resume["github"]:
                profile_count += 1

            if resume["portfolio"]:
                profile_count += 1


            if profile_count >= 2:

                score += 10

                strengths.append(
                    "Professional online profiles are included."
                )

            elif profile_count == 1:

                score += 5

                suggestions.append(
                    "Consider adding GitHub or portfolio profile."
                )

            else:

                suggestions.append(
                    "Add LinkedIn, GitHub or portfolio links."
                )


            # --------------------------------------------------
            # LIMIT SCORE
            # --------------------------------------------------

            score = min(score, 100)


            # --------------------------------------------------
            # SCORE STATUS
            # --------------------------------------------------

            if score >= 80:

                score_status = "Excellent"

            elif score >= 65:

                score_status = "Good"

            elif score >= 50:

                score_status = "Needs Improvement"

            else:

                score_status = "Needs Major Improvement"


            return render_template(
                "resume_ats.html",

                resume=resume,

                student=student,

                education=education,

                projects=projects,

                experience=experience,

                skills=skills,

                certificates=certificates,

                languages=languages,

                achievements=achievements,

                hobbies=hobbies,

                score=score,

                score_status=score_status,

                strengths=strengths,

                suggestions=suggestions
            )


        except Exception as e:

            print(
                "ATS Analysis Error:",
                e
            )

            flash(
                "Unable to analyze resume.",
                "danger"
            )

            return redirect(
                url_for(
                    "resume_details",
                    resume_id=resume_id
                )
            )


        finally:

            conn.close()
    @app.route(
        "/student/resume/<int:resume_id>"
    )
    @student_required
    def resume_details(resume_id):

        conn = get_connection()
        cursor = conn.cursor()


        # ------------------------------------------------------
        # RESUME
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resumes
            WHERE id = ?
            AND student_id = ?
            """,
            (
                resume_id,
                session["student_id"]
            )
        )

        resume = cursor.fetchone()


        if resume is None:

            conn.close()

            flash(
                "Resume not found.",
                "danger"
            )

            return redirect(
                url_for("my_resumes")
            )


        # ------------------------------------------------------
        # STUDENT
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE id = ?
            """,
            (
                session["student_id"],
            )
        )

        student = cursor.fetchone()


        # ------------------------------------------------------
        # EDUCATION
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_education
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        education = cursor.fetchall()


        # ------------------------------------------------------
        # PROJECTS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_projects
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        projects = cursor.fetchall()


        # ------------------------------------------------------
        # EXPERIENCE
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_experience
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        experience = cursor.fetchall()


        # ------------------------------------------------------
        # SKILLS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_skills
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        skills = cursor.fetchall()


        # ------------------------------------------------------
        # CERTIFICATES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_certificates
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        certificates = cursor.fetchall()


        # ------------------------------------------------------
        # LANGUAGES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_languages
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        languages = cursor.fetchall()


        # ------------------------------------------------------
        # ACHIEVEMENTS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_achievements
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        achievements = cursor.fetchall()


        # ------------------------------------------------------
        # HOBBIES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_hobbies
            WHERE resume_id = ?
            ORDER BY id ASC
            """,
            (resume_id,)
        )

        hobbies = cursor.fetchall()


        conn.close()


        return render_template(
            "resume_details.html",
            resume=resume,
            student=student,
            education=education,
            projects=projects,
            experience=experience,
            skills=skills,
            certificates=certificates,
            languages=languages,
            achievements=achievements,
            hobbies=hobbies
        )


    # ==========================================================
    # EDIT RESUME
    # ==========================================================

    @app.route(
        "/student/edit-resume/<int:resume_id>"
    )
    @student_required
    def edit_resume(resume_id):

        conn = get_connection()
        cursor = conn.cursor()


        # ------------------------------------------------------
        # RESUME
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resumes
            WHERE id = ?
            AND student_id = ?
            """,
            (
                resume_id,
                session["student_id"]
            )
        )

        resume = cursor.fetchone()


        if resume is None:

            conn.close()

            flash(
                "Resume not found.",
                "danger"
            )

            return redirect(
                url_for("my_resumes")
            )


        # ------------------------------------------------------
        # STUDENT
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE id = ?
            """,
            (
                session["student_id"],
            )
        )

        student = cursor.fetchone()


        # ------------------------------------------------------
        # EDUCATION
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_education
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        education = cursor.fetchall()


        # ------------------------------------------------------
        # PROJECTS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_projects
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        projects = cursor.fetchall()


        # ------------------------------------------------------
        # EXPERIENCE
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_experience
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        experience = cursor.fetchall()


        # ------------------------------------------------------
        # SKILLS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_skills
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        skills = cursor.fetchall()


        # ------------------------------------------------------
        # CERTIFICATES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_certificates
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        certificates = cursor.fetchall()


        # ------------------------------------------------------
        # LANGUAGES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_languages
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        languages = cursor.fetchall()


        # ------------------------------------------------------
        # ACHIEVEMENTS
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_achievements
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        achievements = cursor.fetchall()


        # ------------------------------------------------------
        # HOBBIES
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM resume_hobbies
            WHERE resume_id = ?
            ORDER BY id
            """,
            (resume_id,)
        )

        hobbies = cursor.fetchall()


        conn.close()


        return render_template(
            "resume_builder.html",
            student=student,
            resume=resume,
            education=education,
            projects=projects,
            experience=experience,
            skills=skills,
            certificates=certificates,
            languages=languages,
            achievements=achievements,
            hobbies=hobbies,
            edit_mode=True
        )


    # ==========================================================
    # UPDATE RESUME
    # ==========================================================

    @app.route(
        "/resume/update/<int:resume_id>",
        methods=["POST"]
    )
    @student_required
    def update_resume(resume_id):

        conn = get_connection()
        cursor = conn.cursor()


        try:

            # --------------------------------------------------
            # GET FORM DATA
            # --------------------------------------------------

            resume_name = request.form.get(
                "resume_name",
                ""
            ).strip()

            fullname = request.form.get(
                "fullname",
                ""
            ).strip()

            template = request.form.get(
                "template",
                "ats"
            ).strip()

            objective = request.form.get(
                "objective",
                ""
            ).strip()

            linkedin = request.form.get(
                "linkedin",
                ""
            ).strip()

            github = request.form.get(
                "github",
                ""
            ).strip()

            portfolio = request.form.get(
                "portfolio",
                ""
            ).strip()

            job_title = request.form.get(
                "job_title",
                ""
            ).strip()


            # --------------------------------------------------
            # UPDATE RESUME MASTER
            # --------------------------------------------------

            cursor.execute(
                """
                UPDATE resumes
                SET
                    resume_name = ?,
                    fullname = ?,
                    job_title = ?,
                    template = ?,
                    objective = ?,
                    linkedin = ?,
                    github = ?,
                    portfolio = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                AND student_id = ?
                """,
                (
                    resume_name,
                    fullname,
                    job_title,
                    template,
                    objective,
                    linkedin,
                    github,
                    portfolio,
                    resume_id,
                    session["student_id"]
                )
            )


            # --------------------------------------------------
            # DELETE OLD CHILD RECORDS
            # --------------------------------------------------

            tables = [
                "resume_education",
                "resume_projects",
                "resume_experience",
                "resume_skills",
                "resume_certificates",
                "resume_languages",
                "resume_achievements",
                "resume_hobbies"
            ]


            for table in tables:

                cursor.execute(
                    f"""
                    DELETE FROM {table}
                    WHERE resume_id = ?
                    """,
                    (resume_id,)
                )


            # ==================================================
            # EDUCATION
            # ==================================================

            degrees = request.form.getlist(
                "education_degree[]"
            )

            colleges = request.form.getlist(
                "education_college[]"
            )

            years = request.form.getlist(
                "education_year[]"
            )

            cgpas = request.form.getlist(
                "education_cgpa[]"
            )


            for degree, college, year, cgpa in zip(
                degrees,
                colleges,
                years,
                cgpas
            ):

                if degree.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_education
                        (
                            resume_id,
                            degree,
                            college,
                            passing_year,
                            cgpa
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            degree.strip(),
                            college.strip(),
                            year.strip(),
                            cgpa.strip()
                        )
                    )


            # ==================================================
            # PROJECTS
            # ==================================================

            titles = request.form.getlist(
                "project_title[]"
            )

            technologies = request.form.getlist(
                "project_technology[]"
            )

            descriptions = request.form.getlist(
                "project_description[]"
            )


            for title, technology, description in zip(
                titles,
                technologies,
                descriptions
            ):

                if title.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_projects
                        (
                            resume_id,
                            title,
                            technology,
                            description
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            title.strip(),
                            technology.strip(),
                            description.strip()
                        )
                    )


            # ==================================================
            # EXPERIENCE
            # ==================================================

            companies = request.form.getlist(
                "company[]"
            )

            roles = request.form.getlist(
                "role[]"
            )

            durations = request.form.getlist(
                "duration[]"
            )

            descriptions = request.form.getlist(
                "experience_description[]"
            )


            for company, role, duration, description in zip(
                companies,
                roles,
                durations,
                descriptions
            ):

                if company.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_experience
                        (
                            resume_id,
                            company,
                            role,
                            duration,
                            description
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            company.strip(),
                            role.strip(),
                            duration.strip(),
                            description.strip()
                        )
                    )


            # ==================================================
            # SKILLS
            # ==================================================

            skills = request.form.get(
                "skills",
                ""
            ).strip()


            for skill in skills.split(","):

                skill = skill.strip()

                if skill:

                    cursor.execute(
                        """
                        INSERT INTO resume_skills
                        (
                            resume_id,
                            skill
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            skill
                        )
                    )


            # ==================================================
            # CERTIFICATES
            # ==================================================

            names = request.form.getlist(
                "certificate_name[]"
            )

            organizations = request.form.getlist(
                "certificate_org[]"
            )

            years = request.form.getlist(
                "certificate_year[]"
            )


            for name, organization, year in zip(
                names,
                organizations,
                years
            ):

                if name.strip():

                    cursor.execute(
                        """
                        INSERT INTO resume_certificates
                        (
                            resume_id,
                            certificate,
                            organization,
                            year
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            resume_id,
                            name.strip(),
                            organization.strip(),
                            year.strip()
                        )
                    )


            # ==================================================
            # LANGUAGES
            # ==================================================

            languages = request.form.getlist(
                "language[]"
            )


            for language in languages:

                language = language.strip()

                if language:

                    cursor.execute(
                        """
                        INSERT INTO resume_languages
                        (
                            resume_id,
                            language
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            language
                        )
                    )


            # ==================================================
            # ACHIEVEMENTS
            # ==================================================

            achievements = request.form.getlist(
                "achievement[]"
            )


            for achievement in achievements:

                achievement = achievement.strip()

                if achievement:

                    cursor.execute(
                        """
                        INSERT INTO resume_achievements
                        (
                            resume_id,
                            achievement
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            achievement
                        )
                    )


            # ==================================================
            # HOBBIES
            # ==================================================

            hobbies = request.form.getlist(
                "hobby[]"
            )


            for hobby in hobbies:

                hobby = hobby.strip()

                if hobby:

                    cursor.execute(
                        """
                        INSERT INTO resume_hobbies
                        (
                            resume_id,
                            hobby
                        )
                        VALUES (?, ?)
                        """,
                        (
                            resume_id,
                            hobby
                        )
                    )


            # ==================================================
            # COMMIT
            # ==================================================

            conn.commit()

            flash(
                "Resume updated successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "resume_details",
                    resume_id=resume_id
                )
            )


        except Exception as e:

            conn.rollback()

            print(
                "Resume Update Error:",
                e
            )

            flash(
                f"Error updating resume: {str(e)}",
                "danger"
            )

            return redirect(
                url_for(
                    "edit_resume",
                    resume_id=resume_id
                )
            )


        finally:

            conn.close()


    # ==========================================================
    # DUPLICATE RESUME
    # ==========================================================

    @app.route(
        "/student/duplicate-resume/<int:resume_id>"
    )
    @student_required
    def duplicate_resume(resume_id):

        flash(
            "Duplicate Resume feature coming soon.",
            "info"
        )

        return redirect(
            url_for("my_resumes")
        )


    # ==========================================================
    # DELETE RESUME
    # ==========================================================

    @app.route(
        "/student/delete-resume/<int:resume_id>"
    )
    @student_required
    def delete_resume(resume_id):

        conn = get_connection()
        cursor = conn.cursor()


        try:

            tables = [
                "resume_education",
                "resume_projects",
                "resume_experience",
                "resume_skills",
                "resume_certificates",
                "resume_languages",
                "resume_achievements",
                "resume_hobbies"
            ]


            for table in tables:

                cursor.execute(
                    f"""
                    DELETE FROM {table}
                    WHERE resume_id = ?
                    """,
                    (resume_id,)
                )


            cursor.execute(
                """
                DELETE FROM resumes
                WHERE id = ?
                AND student_id = ?
                """,
                (
                    resume_id,
                    session["student_id"]
                )
            )


            conn.commit()

            flash(
                "Resume Deleted Successfully.",
                "success"
            )


        except Exception as e:

            conn.rollback()

            print(
                "Resume Delete Error:",
                e
            )

            flash(
                "Unable to delete resume.",
                "danger"
            )


        finally:

            conn.close()


        return redirect(
            url_for("my_resumes")
        )