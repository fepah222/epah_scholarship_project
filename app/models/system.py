from datetime import datetime, timezone
from ..extensions import db
now=lambda: datetime.now(timezone.utc)
class Notification(db.Model):
    __tablename__ = "notifications"
    id=db.Column(db.String(36), primary_key=True); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True); notification_type=db.Column(db.String(50)); title=db.Column(db.String(180), nullable=False); message=db.Column(db.Text); related_entity_type=db.Column(db.String(50)); related_entity_id=db.Column(db.String(36)); is_read=db.Column(db.Boolean, default=False); created_at=db.Column(db.DateTime(timezone=True), default=now); read_at=db.Column(db.DateTime(timezone=True))
class ReminderLog(db.Model):
    __tablename__ = "reminder_logs"
    __table_args__=(db.UniqueConstraint('scholarship_id','student_id','reminder_type',name='uq_reminder_once'),)
    id=db.Column(db.String(36), primary_key=True); scholarship_id=db.Column(db.String(36), db.ForeignKey('scholarships.id'), nullable=False); student_id=db.Column(db.String(36), db.ForeignKey('student_profiles.id'), nullable=False); reminder_type=db.Column(db.String(20), nullable=False); scheduled_for=db.Column(db.DateTime(timezone=True)); sent_at=db.Column(db.DateTime(timezone=True)); delivery_status=db.Column(db.String(30), default='pending')
class Report(db.Model):
    __tablename__ = "reports"
    id=db.Column(db.String(36), primary_key=True); reporter_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); reported_entity_type=db.Column(db.String(50), nullable=False); reported_entity_id=db.Column(db.String(36), nullable=False); reason=db.Column(db.String(100), nullable=False); description=db.Column(db.Text); report_status=db.Column(db.String(20), default='pending'); admin_notes=db.Column(db.Text); reviewed_by=db.Column(db.String(36), db.ForeignKey('users.id')); reviewed_at=db.Column(db.DateTime(timezone=True)); created_at=db.Column(db.DateTime(timezone=True), default=now)
class AdminAction(db.Model):
    __tablename__ = "admin_actions"
    id=db.Column(db.String(36), primary_key=True); admin_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); action_type=db.Column(db.String(80), nullable=False); target_entity_type=db.Column(db.String(50)); target_entity_id=db.Column(db.String(36)); reason=db.Column(db.Text); action_data=db.Column(db.JSON); created_at=db.Column(db.DateTime(timezone=True), default=now)
