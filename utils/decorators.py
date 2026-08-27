from functools import wraps
from flask import session, redirect, flash


# ==========================
# Student Required
# ==========================

def student_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "student_id" not in session:
            flash("Please login as Student first.", "warning")
            return redirect("/student/login")

        return func(*args, **kwargs)

    return wrapper


# ==========================
# Company Required
# ==========================

def company_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "company_id" not in session:
            flash("Please login as Company first.", "warning")
            return redirect("/company/login")

        return func(*args, **kwargs)

    return wrapper


# ==========================
# Admin Required
# ==========================

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "admin_id" not in session:
            flash("Please login as Admin first.", "warning")
            return redirect("/admin/login")

        return func(*args, **kwargs)

    return wrapper