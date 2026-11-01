from .main_routes import register_main_routes
from .auth_routes import register_auth_routes
from .student_routes import register_student_routes
from .company_routes import register_company_routes
from .admin_routes import register_admin_routes
from .job_routes import register_job_routes
from .error_routes import register_error_routes
from .resume_routes import register_resume_routes
from .resume_pdf import register_resume_pdf_routes

def register_routes(app):

    register_main_routes(app)
    register_auth_routes(app)
    register_student_routes(app)
    register_company_routes(app)
    register_admin_routes(app)
    register_job_routes(app)
    register_error_routes(app)
    register_resume_routes(app)
    register_resume_pdf_routes(app)