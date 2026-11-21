from pathlib import Path

from flask import Flask, render_template, send_from_directory
from sqlalchemy import text

from config import Config
from .extensions import csrf, db, login_manager, migrate, socketio


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.setdefault("APPLICATION_NAME", "Epah Scholarship")
    app.jinja_env.globals["getattr"] = getattr

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    for folder in (app.config["PUBLIC_UPLOAD"], app.config["PRIVATE_UPLOAD"]):
        Path(folder).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, async_mode="threading")
    csrf.init_app(app)

    from . import models  # noqa: F401
    from .routes import register_blueprints

    register_blueprints(app)

    from .sockets.events import register_socket_events
    register_socket_events(socketio)

    @app.get("/")
    def home():
        from .models import InstitutionProfile, Scholarship

        scholarships = (
            Scholarship.query.filter_by(approval_status="approved", publication_status="published")
            .order_by(Scholarship.created_at.desc()).limit(6).all()
        )
        institutions = (
            InstitutionProfile.query.filter_by(verification_status="approved")
            .order_by(InstitutionProfile.created_at.desc()).limit(6).all()
        )
        return render_template("public/home.html", scholarships=scholarships, institutions=institutions)

    @app.get("/media/<path:filename>")
    def media_file(filename):
        return send_from_directory(app.config["PUBLIC_UPLOAD"], filename)

    @app.get("/health")
    def health():
        db.session.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "application": app.config["APPLICATION_NAME"],
            "database": db.engine.url.get_backend_name(),
        }

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def too_large(error):
        return render_template("errors/413.html"), 413

    @app.cli.command("create-admin")
    def create_admin_command():
        """Create the first administrator from the local terminal."""
        import click
        import uuid
        from werkzeug.security import generate_password_hash
        from .models import User

        if User.query.filter_by(role="admin").first():
            raise click.ClickException(
                "An administrator already exists. Additional administrators must be provisioned through the invitation workflow."
            )

        full_name = click.prompt("Administrator full name").strip()
        email = click.prompt("Administrator email").strip().lower()
        password = click.prompt("Password (minimum 12 characters)", hide_input=True, confirmation_prompt=True)
        if len(password) < 12:
            raise click.ClickException("Password must contain at least 12 characters.")
        if User.query.filter_by(email=email).first():
            raise click.ClickException("That email address is already registered.")

        user = User(
            id=str(uuid.uuid4()), full_name=full_name, email=email,
            password_hash=generate_password_hash(password), role="admin",
            account_status="active", email_verified=True,
        )
        db.session.add(user)
        db.session.commit()
        click.echo("First Epah Scholarship administrator created successfully.")

    with app.app_context():
        db.create_all()

    return app
