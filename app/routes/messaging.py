import uuid
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..models import Conversation, ConversationParticipant, Message
bp=Blueprint('messaging',__name__,url_prefix='/messages')
@bp.get('/')
@login_required
def inbox():
    parts=ConversationParticipant.query.filter_by(user_id=current_user.id,is_active=True).all(); ids=[p.conversation_id for p in parts]
    conversations=Conversation.query.filter(Conversation.id.in_(ids)).order_by(Conversation.last_message_at.desc()).all() if ids else []
    return render_template('messaging/inbox.html',conversations=conversations)
@bp.get('/<conversation_id>')
@login_required
def conversation(conversation_id):
    part=ConversationParticipant.query.filter_by(conversation_id=conversation_id,user_id=current_user.id,is_active=True).first()
    if not part: abort(403)
    messages=Message.query.filter_by(conversation_id=conversation_id).order_by(Message.sent_at.asc()).limit(200).all()
    return render_template('messaging/conversation.html',conversation_id=conversation_id,messages=messages)
