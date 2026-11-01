from flask import render_template, session
from database.db import get_connection
from utils.decorators import student_required


def register_resume_ats_routes(app):

    @app.route("/resume/ats/<int:resume_id>")
    @student_required
    def resume_ats(resume_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM resumes
            WHERE id=? AND student_id=?
        """, (
            resume_id,
            session["student_id"]
        ))

        resume = cursor.fetchone()

        if not resume:

            conn.close()

            return "Resume Not Found"

        cursor.execute(
            "SELECT * FROM resume_skills WHERE resume_id=?",
            (resume_id,)
        )

        skills = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM resume_projects WHERE resume_id=?",
            (resume_id,)
        )

        projects = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM resume_education WHERE resume_id=?",
            (resume_id,)
        )

        education = cursor.fetchall()
        score = 0

        suggestions = []

        # Objective

        if resume["objective"]:

            score += 20

        else:

            suggestions.append(
                "Add Career Objective."
            )

        # Skills

        if len(skills) >= 5:

            score += 25

        else:

            suggestions.append(
                "Add at least 5 skills."
            )

        # Projects

        if len(projects) >= 2:

            score += 25

        else:

            suggestions.append(
                "Add minimum 2 projects."
            )

        # Education

        if len(education) > 0:

            score += 20

        else:

            suggestions.append(
                "Add education details."
            )

        # LinkedIn

        if resume["linkedin"]:

            score += 10

        else:

            suggestions.append(
                "Add LinkedIn profile."
            )
                    # -----------------------------------
        # Score Category
        # -----------------------------------

        if score >= 90:

            level = "Excellent"
            color = "success"

        elif score >= 70:

            level = "Good"
            color = "primary"

        elif score >= 50:

            level = "Average"
            color = "warning"

        else:

            level = "Poor"
            color = "danger"

        conn.close()

        return render_template(

            "resume_ats.html",

            resume=resume,

            score=score,

            level=level,

            color=color,

            suggestions=suggestions,

            skills=skills,

            projects=projects,

            education=education

        )