import uuid

from flask import Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    Post, PostReaction, PostComment, InstitutionProfile,
    StudentProfile, InstitutionFollow, Application, Scholarship,
)

bp = Blueprint("social", __name__, url_prefix="/social")


def uid():
    return str(uuid.uuid4())


def can_view_post(post):
    """Public posts are readable by everyone; restricted posts require an accepted application."""
    if post.visibility == "public":
        return True
    if not current_user.is_authenticated or current_user.role != "student":
        return False

    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not student:
        return False

    return (
        Application.query.join(Scholarship, Application.scholarship_id == Scholarship.id)
        .filter(
            Application.student_id == student.id,
            Application.application_status == "accepted",
            Scholarship.institution_id == post.institution_id,
        )
        .first()
        is not None
    )


def require_post_access(post):
    if not post or post.publication_status != "published":
        abort(404)
    if not can_view_post(post):
        abort(404)


@bp.post("/posts")
@login_required
def create_post():
    if current_user.role != "institution":
        abort(403)
    institution = InstitutionProfile.query.filter_by(user_id=current_user.id).first()
    if not institution:
        abort(403)
    if institution.verification_status != "approved":
        flash("Your institution must be approved by an administrator before publishing posts.", "warning")
        return redirect(url_for("institution.dashboard"))

    content = request.form.get("content", "").strip()
    visibility = request.form.get("visibility", "public").strip()
    if not content:
        flash("Write something before publishing.", "warning")
        return redirect(url_for("institution.dashboard"))
    if visibility not in {"public", "accepted_applicants"}:
        abort(400)

    post = Post(
        id=uid(),
        institution_id=institution.id,
        content=content,
        post_type="text",
        visibility=visibility,
        publication_status="published",
    )
    db.session.add(post)
    db.session.commit()
    flash("Post published successfully.", "success")
    return redirect(url_for("institution.public_profile", profile_id=institution.id))


@bp.post("/posts/<post_id>/react")
@login_required
def react(post_id):
    post = db.session.get(Post, post_id)
    require_post_access(post)
    kind = request.form.get("reaction_type", "like")
    if kind not in ("like", "love", "haha", "wow", "sad", "angry"):
        abort(400)
    reaction = PostReaction.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if reaction and reaction.reaction_type == kind:
        db.session.delete(reaction)
    elif reaction:
        reaction.reaction_type = kind
    else:
        db.session.add(PostReaction(id=uid(), post_id=post.id, user_id=current_user.id, reaction_type=kind))
    db.session.commit()
    return redirect(request.referrer or url_for("home"))


@bp.post("/posts/<post_id>/comments")
@login_required
def comment(post_id):
    post = db.session.get(Post, post_id)
    require_post_access(post)
    comment_text = request.form.get("comment_text", "").strip()
    if not comment_text or len(comment_text) > 3000:
        flash("Comment must contain between 1 and 3000 characters.", "warning")
    else:
        db.session.add(PostComment(
            id=uid(), post_id=post.id, user_id=current_user.id, comment_text=comment_text
        ))
        db.session.commit()
    return redirect(request.referrer or url_for("home"))


@bp.post("/institutions/<institution_id>/follow")
@login_required
def follow(institution_id):
    if current_user.role != "student":
        abort(403)
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    institution = db.session.get(InstitutionProfile, institution_id)
    if not student or not institution or institution.verification_status != "approved":
        abort(404)
    relation = InstitutionFollow.query.filter_by(
        student_id=student.id, institution_id=institution.id
    ).first()
    if relation:
        db.session.delete(relation)
        flash("You unfollowed this institution.", "info")
    else:
        db.session.add(InstitutionFollow(
            id=uid(), student_id=student.id, institution_id=institution.id
        ))
        flash("You are now following this institution.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("institution.public_profile", profile_id=institution.id))
