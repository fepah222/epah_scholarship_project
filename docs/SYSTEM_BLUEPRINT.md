# Epah Scholarship System Blueprint

## Product objective
Epah Scholarship connects students with verified educational institutions and scholarship opportunities. The institution experience is inspired by Facebook Pages: cover image, logo, About, Posts, Photos, Scholarships and Followers.

## Roles
- Student: profile, qualifications, feed, follow institutions, react/comment, message institutions, discover/save/apply for scholarships.
- Institution: public profile, verification documents, posts, gallery, followers, inbox, scholarships and application review.
- Administrator: invitation-only access, institution verification, scholarship approval, moderation, reports and audit review.

## Confirmed social features
- Posts and announcements
- Photo/video gallery
- Student follows
- Six post reactions: like, love, haha, wow, sad, angry
- Comments and one-level replies
- Private real-time text messaging through Flask-SocketIO

## Scholarship rules
Institutions can register and build a public profile before verification. Only approved institutions can have scholarships approved and published. Students can apply to published opportunities before the deadline. Application records and supporting documents are private.

## Technology
Python, Flask, Flask-SQLAlchemy, SQLite, Flask-Login, Flask-Migrate, Flask-WTF, Flask-SocketIO, HTML, CSS and JavaScript. No MySQL or XAMPP.

## Visual identity
Navy `#182B49`, warm white `#F8F6F0`, restrained gold `#D5A63C`; light and dark theme support.

## Release approach
Foundation/authentication; institution identity; social features; scholarship management; applications; notifications/admin; testing and deployment.
