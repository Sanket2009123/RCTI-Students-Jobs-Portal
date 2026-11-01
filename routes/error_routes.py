from flask import render_template


def register_error_routes(app):

    # ==========================
    # 404 Page Not Found
    # ==========================
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404


    # ==========================
    # 500 Internal Server Error
    # ==========================
    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500


    # ==========================
    # 403 Forbidden
    # ==========================
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("403.html"), 403