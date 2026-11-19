import uuid, os
from werkzeug.utils import secure_filename
from flask import current_app
ALLOWED_IMAGES={'png','jpg','jpeg','webp','gif'}
ALLOWED_VIDEOS={'mp4','webm','mov'}
def save_upload(file, category='public', allowed=None):
    if not file or not file.filename: return None
    ext=file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else ''
    allowed=allowed or ALLOWED_IMAGES
    if ext not in allowed: raise ValueError('Unsupported file extension.')
    folder=current_app.config['PRIVATE_UPLOAD'] if category=='private' else current_app.config['PUBLIC_UPLOAD']
    name=f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    os.makedirs(folder,exist_ok=True); file.save(os.path.join(folder,name))
    return name
