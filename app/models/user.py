from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

def now(): return datetime.now(timezone.utc)
class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.String(36), primary_key=True)
    full_name=db.Column(db.String(140), nullable=False)
    email=db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone=db.Column(db.String(40))
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(20), nullable=False)
    account_status=db.Column(db.String(20), default='pending', nullable=False)
    email_verified=db.Column(db.Boolean, default=False, nullable=False)
    profile_photo=db.Column(db.String(500))
    last_login_at=db.Column(db.DateTime(timezone=True))
    created_at=db.Column(db.DateTime(timezone=True), default=now, nullable=False)
    updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now)
    def set_password(self, password): self.password_hash=generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    @property
    def is_active(self): return self.account_status == 'active'
@login_manager.user_loader
def load_user(user_id): return db.session.get(User, user_id)
class EmailVerificationToken(db.Model):
    __tablename__ = "email_verification_tokens"
    id=db.Column(db.String(36), primary_key=True); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); token_hash=db.Column(db.String(255), nullable=False); expires_at=db.Column(db.DateTime(timezone=True), nullable=False); used_at=db.Column(db.DateTime(timezone=True)); created_at=db.Column(db.DateTime(timezone=True), default=now)
class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"
    id=db.Column(db.String(36), primary_key=True); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); token_hash=db.Column(db.String(255), nullable=False); expires_at=db.Column(db.DateTime(timezone=True), nullable=False); used_at=db.Column(db.DateTime(timezone=True)); created_at=db.Column(db.DateTime(timezone=True), default=now)
class UserSettings(db.Model):
    __tablename__ = "user_settings"
    id=db.Column(db.String(36), primary_key=True); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False); theme=db.Column(db.String(10), default='light'); email_notifications=db.Column(db.Boolean, default=True); in_app_notifications=db.Column(db.Boolean, default=True); message_notifications=db.Column(db.Boolean, default=True); scholarship_notifications=db.Column(db.Boolean, default=True); privacy_settings=db.Column(db.JSON, default=dict)
class AdminInvitation(db.Model):
    __tablename__ = "admin_invitations"
    id=db.Column(db.String(36), primary_key=True); email=db.Column(db.String(255), nullable=False, index=True); token_hash=db.Column(db.String(255), nullable=False); invited_by=db.Column(db.String(36), db.ForeignKey('users.id')); expires_at=db.Column(db.DateTime(timezone=True), nullable=False); accepted_at=db.Column(db.DateTime(timezone=True)); created_at=db.Column(db.DateTime(timezone=True), default=now)
