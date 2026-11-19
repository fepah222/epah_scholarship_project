# Implementation Specification

## Authentication
Shared `users` table with `student`, `institution`, and `admin` roles. Passwords use Werkzeug password hashing. Public registration permits student and institution roles only. Admin onboarding is invitation-only.

## Institution profile
One institution profile per institution account. Public profile shows cover, logo, description, About, Posts, Photos, Scholarships and follower count. Verification status must be visible. Private verification documents are not public.

## Social
Institution-owned posts; reactions are unique per `(post_id,user_id)`; comments support one-level replies; follows are unique per `(student_id,institution_id)`. Backend ownership checks are mandatory.

## Messaging
Flask-SocketIO events: `join_conversation`, `send_message`, `new_message`, `socket_error`, `mark_read`, and `read_receipt`. Authenticate sockets and verify participant membership for every operation. Persist a message before broadcasting it. Only conversation participants can join its room.

## Scholarships
Institutions submit scholarships for review. Admin approval is required. The institution must be verified before scholarship approval. Only approved and published scholarships appear in the public directory.

## Applications
Students submit applications against published scholarships. Prevent duplicate applications by the same student unless resubmission is explicitly supported. Store documents privately and enforce ownership on every read/download.

## Production work still required
Email delivery and token verification; secure admin bootstrap; upload UI and robust content inspection; private file delivery; full message creation UX and receipts; notification delivery and scheduled reminder worker; comprehensive moderation; stronger tests; production deployment and backups.
