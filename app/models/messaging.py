from datetime import datetime, timezone
from ..extensions import db
now=lambda: datetime.now(timezone.utc)
class Conversation(db.Model):
    __tablename__ = "conversations"
    id=db.Column(db.String(36), primary_key=True); conversation_type=db.Column(db.String(30), default='student_institution'); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now); last_message_at=db.Column(db.DateTime(timezone=True)); participants=db.relationship('ConversationParticipant', cascade='all, delete-orphan', backref='conversation')
class ConversationParticipant(db.Model):
    __tablename__ = "conversation_participants"
    __table_args__=(db.UniqueConstraint('conversation_id','user_id',name='uq_conversation_user'),)
    id=db.Column(db.String(36), primary_key=True); conversation_id=db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); joined_at=db.Column(db.DateTime(timezone=True), default=now); last_read_at=db.Column(db.DateTime(timezone=True)); is_active=db.Column(db.Boolean, default=True); muted_until=db.Column(db.DateTime(timezone=True)); user=db.relationship('User')
class Message(db.Model):
    __tablename__ = "messages"
    id=db.Column(db.String(36), primary_key=True); conversation_id=db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False, index=True); sender_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); message_type=db.Column(db.String(20), default='text'); message_text=db.Column(db.Text); attachment_path=db.Column(db.String(500)); sent_at=db.Column(db.DateTime(timezone=True), default=now); edited_at=db.Column(db.DateTime(timezone=True)); deleted_at=db.Column(db.DateTime(timezone=True)); sender=db.relationship('User')
class MessageReceipt(db.Model):
    __tablename__ = "message_receipts"
    __table_args__=(db.UniqueConstraint('message_id','user_id',name='uq_message_receipt_user'),)
    id=db.Column(db.String(36), primary_key=True); message_id=db.Column(db.String(36), db.ForeignKey('messages.id'), nullable=False); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); delivered_at=db.Column(db.DateTime(timezone=True)); read_at=db.Column(db.DateTime(timezone=True))
