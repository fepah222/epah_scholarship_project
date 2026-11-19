import uuid
from flask import request
from flask_login import current_user
from flask_socketio import join_room, emit
from ..extensions import db
from ..models import ConversationParticipant, Message, Conversation, MessageReceipt
from datetime import datetime, timezone

def register_socket_events(socketio):
    @socketio.on('connect')
    def connected(auth=None):
        if not current_user.is_authenticated: return False
    @socketio.on('join_conversation')
    def join_conversation(data):
        if not current_user.is_authenticated: return
        cid=(data or {}).get('conversation_id')
        part=ConversationParticipant.query.filter_by(conversation_id=cid,user_id=current_user.id,is_active=True).first()
        if part: join_room(cid); emit('joined_conversation',{'conversation_id':cid})
        else: emit('socket_error',{'message':'Not authorized for this conversation.'})
    @socketio.on('send_message')
    def send_message(data):
        if not current_user.is_authenticated: return
        data=data or {}; cid=data.get('conversation_id'); body=(data.get('message') or '').strip()
        part=ConversationParticipant.query.filter_by(conversation_id=cid,user_id=current_user.id,is_active=True).first()
        if not part or not body or len(body)>5000:
            emit('socket_error',{'message':'Message invalid or conversation access denied.'}); return
        msg=Message(id=str(uuid.uuid4()),conversation_id=cid,sender_id=current_user.id,message_type='text',message_text=body)
        conv=db.session.get(Conversation,cid); conv.last_message_at=datetime.now(timezone.utc)
        db.session.add(msg); db.session.commit()
        payload={'id':msg.id,'conversation_id':cid,'sender_id':current_user.id,'sender_name':current_user.full_name,'message':body,'sent_at':msg.sent_at.isoformat()}
        emit('new_message',payload,to=cid)
    @socketio.on('mark_read')
    def mark_read(data):
        if not current_user.is_authenticated: return
        cid=(data or {}).get('conversation_id')
        part=ConversationParticipant.query.filter_by(conversation_id=cid,user_id=current_user.id,is_active=True).first()
        if not part: return
        part.last_read_at=datetime.now(timezone.utc); db.session.commit(); emit('read_receipt',{'conversation_id':cid,'user_id':current_user.id},to=cid,include_self=False)
