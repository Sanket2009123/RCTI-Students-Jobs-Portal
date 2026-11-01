from flask import send_file, session, flash, redirect, url_for, render_template, request

import os
import html
from io import BytesIO

# ============================================================
# WEASYPRINT / MSYS2 WINDOWS DLL CONFIGURATION
# ============================================================

WEASYPRINT_DLL_DIR = r"C:\msys64\ucrt64\bin"

if os.path.isdir(WEASYPRINT_DLL_DIR):

    # WeasyPrint uses this variable to locate GTK/Pango/GLib DLLs.
    os.environ["WEASYPRINT_DLL_DIRECTORIES"] = WEASYPRINT_DLL_DIR

    # Python 3.8+ Windows DLL search path.
    # Keep the handle alive for the lifetime of this module.
    try:
        _weasyprint_dll_handle = os.add_dll_directory(
            WEASYPRINT_DLL_DIR
        )
    except (AttributeError, OSError):
        _weasyprint_dll_handle = None
from database.db import get_connection
from utils.decorators import student_required


def _safe(value):
    """Convert database values safely for ReportLab Paragraph."""
    if value is None:
        return ""

    return html.escape(str(value))


def _value(row, *keys):
    """Return the first available non-empty field from a sqlite Row."""
    for key in keys:
        try:
            value = row[key]
        except (KeyError, IndexError):
            continue

        if value is not None and str(value).strip():
            return str(value).strip()

    return ""






def register_resume_pdf_routes(app):

    @app.route("/resume/pdf/<int:resume_id>")
    @student_required
    def download_resume_pdf(resume_id):

        """
        Download the EXACT selected resume template as PDF.

        Preview:
            /resume/preview/<resume_id>

        Download:
            /resume/pdf/<resume_id>

        Both routes load the same resume_id and the same selected
        template from the database. The preview HTML is rendered
        directly to PDF with WeasyPrint, so the PDF keeps the
        template's HTML/CSS design.
        """

        conn = get_connection()

        try:
            cursor = conn.cursor()

            # =====================================================
            # 1. LOAD EXACT RESUME
            # =====================================================

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

            # =====================================================
            # 2. LOAD STUDENT
            # =====================================================

            cursor.execute(
                """
                SELECT *
                FROM students
                WHERE id = ?
                """,
                (session["student_id"],)
            )

            student = cursor.fetchone()

            if student is None:
                flash(
                    "Student information not found.",
                    "danger"
                )
                return redirect(
                    url_for("my_resumes")
                )

            # =====================================================
            # 3. LOAD SAME RELATED DATA AS PREVIEW ROUTE
            # =====================================================

            def fetch(table_name):

                cursor.execute(
                    f"""
                    SELECT *
                    FROM {table_name}
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

            # =====================================================
            # 4. USE EXACT SAME TEMPLATE SELECTION AS PREVIEW
            # =====================================================

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
                _value(
                    resume,
                    "template"
                )
                or "ats"
            )

            selected_template = (
                selected_template
                .strip()
                .lower()
                .replace(".html", "")
            )

            if selected_template not in VALID_TEMPLATES:
                selected_template = "ats"

            template_file = (
                f"resumes/{selected_template}.html"
            )

            # =====================================================
            # 5. RENDER THE SAME HTML TEMPLATE USED BY PREVIEW
            # =====================================================

            rendered_html = render_template(
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

            # =====================================================
            # 6. HTML -> PDF
            # =====================================================
            #
            # WeasyPrint is intentionally used here instead of
            # ReportLab. The HTML template contains the real resume
            # design, CSS, colors, layout, profile photo, etc.
            #
            # request.url_root lets WeasyPrint resolve URLs such as:
            # /static/uploads/profile_photos/photo.jpg
            #

            # WeasyPrint must be installed in the SAME Python environment
            # that runs this Flask application.
            try:
                from weasyprint import HTML
            except Exception as e:
                app.logger.exception(
                    "WeasyPrint import failed for resume %s",
                    resume_id
                )
                raise RuntimeError(
                    "WeasyPrint could not load. "
                    f"DLL directory: {WEASYPRINT_DLL_DIR}. "
                    f"Original error: {e}"
                ) from e

            pdf_bytes = HTML(
                string=rendered_html,
                base_url=request.url_root
            ).write_pdf()

            # =====================================================
            # 7. PROFESSIONAL FILE NAME
            # =====================================================

            student_name = (
                _value(
                    resume,
                    "fullname",
                    "name"
                )
                or _value(
                    student,
                    "fullname",
                    "name"
                )
                or "Student"
            )

            safe_filename = (
                student_name
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
                .replace("*", "_")
                .replace("?", "_")
                .replace('"', "_")
                .replace("<", "_")
                .replace(">", "_")
                .replace("|", "_")
                .replace(" ", "_")
                .strip("._ ")
            )

            if not safe_filename:
                safe_filename = "Student"

            filename = (
                f"{safe_filename}_Resume.pdf"
            )

            # =====================================================
            # 8. SEND PDF TO BROWSER
            # =====================================================

            return send_file(
                BytesIO(pdf_bytes),
                as_attachment=True,
                download_name=filename,
                mimetype="application/pdf"
            )

        except Exception as e:

            import traceback

            print("=" * 70)
            print("EXACT RESUME PDF ERROR")
            print("=" * 70)
            print("Resume ID:", resume_id)
            print(
                "Student ID:",
                session.get("student_id")
            )
            print(
                "Error:",
                repr(e)
            )
            traceback.print_exc()
            print("=" * 70)

            # Do NOT redirect back to preview here. That used to hide the
            # real PDF error and made it look like Download simply reopened
            # the preview page.
            return (
                "Unable to generate the PDF for this resume. "
                f"Error: {html.escape(str(e))}",
                500
            )

        finally:

            try:
                conn.close()
            except Exception:
                pass
