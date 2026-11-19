def register_blueprints(app):
    from .auth import bp as auth_bp
    from .student import bp as student_bp
    from .institution import bp as institution_bp
    from .social import bp as social_bp
    from .scholarship import bp as scholarship_bp
    from .messaging import bp as messaging_bp
    from .admin import bp as admin_bp
    for bp in (auth_bp, student_bp, institution_bp, social_bp, scholarship_bp, messaging_bp, admin_bp): app.register_blueprint(bp)
