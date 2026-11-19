from datetime import datetime, timezone
from ..extensions import db
now=lambda: datetime.now(timezone.utc)
class MediaAlbum(db.Model):
    __tablename__ = "media_albums"
    id=db.Column(db.String(36), primary_key=True); institution_id=db.Column(db.String(36), db.ForeignKey('institution_profiles.id'), nullable=False); album_name=db.Column(db.String(150), nullable=False); description=db.Column(db.Text); cover_media_id=db.Column(db.String(36)); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now)
class InstitutionMedia(db.Model):
    __tablename__ = "institution_media"
    id=db.Column(db.String(36), primary_key=True); institution_id=db.Column(db.String(36), db.ForeignKey('institution_profiles.id'), nullable=False); album_id=db.Column(db.String(36), db.ForeignKey('media_albums.id')); media_type=db.Column(db.String(20), nullable=False); title=db.Column(db.String(180)); description=db.Column(db.Text); file_path=db.Column(db.String(500), nullable=False); thumbnail_path=db.Column(db.String(500)); uploaded_at=db.Column(db.DateTime(timezone=True), default=now); visibility=db.Column(db.String(20), default='public'); uploaded_by=db.Column(db.String(36), db.ForeignKey('users.id'))
class Post(db.Model):
    __tablename__ = "posts"
    id=db.Column(db.String(36), primary_key=True); institution_id=db.Column(db.String(36), db.ForeignKey('institution_profiles.id'), nullable=False); content=db.Column(db.Text); post_type=db.Column(db.String(30), default='text'); visibility=db.Column(db.String(20), default='public'); is_pinned=db.Column(db.Boolean, default=False); publication_status=db.Column(db.String(20), default='published'); published_at=db.Column(db.DateTime(timezone=True), default=now); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now)
    institution=db.relationship('InstitutionProfile', backref='posts')
    media=db.relationship('PostMedia', cascade='all, delete-orphan', backref='post')
    reactions=db.relationship('PostReaction', cascade='all, delete-orphan', backref='post')
    comments=db.relationship('PostComment', cascade='all, delete-orphan', backref='post')
class PostMedia(db.Model):
    __tablename__ = "post_media"
    id=db.Column(db.String(36), primary_key=True); post_id=db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False); media_type=db.Column(db.String(20)); file_path=db.Column(db.String(500), nullable=False); thumbnail_path=db.Column(db.String(500)); caption=db.Column(db.String(255)); display_order=db.Column(db.Integer, default=0); created_at=db.Column(db.DateTime(timezone=True), default=now)
class PostReaction(db.Model):
    __tablename__ = "post_reactions"
    __table_args__=(db.UniqueConstraint('post_id','user_id',name='uq_post_user_reaction'),)
    id=db.Column(db.String(36), primary_key=True); post_id=db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); reaction_type=db.Column(db.String(20), nullable=False); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now)
class PostComment(db.Model):
    __tablename__ = "post_comments"
    id=db.Column(db.String(36), primary_key=True); post_id=db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False); user_id=db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False); parent_comment_id=db.Column(db.String(36), db.ForeignKey('post_comments.id')); comment_text=db.Column(db.Text, nullable=False); created_at=db.Column(db.DateTime(timezone=True), default=now); updated_at=db.Column(db.DateTime(timezone=True), default=now, onupdate=now); deleted_at=db.Column(db.DateTime(timezone=True)); author=db.relationship('User', foreign_keys=[user_id]); replies=db.relationship('PostComment', backref=db.backref('parent', remote_side=[id]))
class InstitutionFollow(db.Model):
    __tablename__ = "institution_follows"
    __table_args__=(db.UniqueConstraint('student_id','institution_id',name='uq_student_institution_follow'),)
    id=db.Column(db.String(36), primary_key=True); student_id=db.Column(db.String(36), db.ForeignKey('student_profiles.id'), nullable=False); institution_id=db.Column(db.String(36), db.ForeignKey('institution_profiles.id'), nullable=False); created_at=db.Column(db.DateTime(timezone=True), default=now); notification_enabled=db.Column(db.Boolean, default=True)
