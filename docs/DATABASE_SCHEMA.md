# Database Schema Reference

The SQLAlchemy models define these 29 principal tables:

1. `users` — central accounts, roles and authentication.
2. `email_verification_tokens` — expiring email verification tokens.
3. `password_reset_tokens` — expiring password reset tokens.
4. `user_settings` — theme, privacy and notification preferences.
5. `admin_invitations` — invitation-only administrator onboarding.
6. `student_profiles` — student-specific profile data.
7. `student_qualifications` — academic qualifications.
8. `institution_profiles` — institutional identity and verification state.
9. `institution_documents` — private verification documents.
10. `media_albums` — institution gallery albums.
11. `institution_media` — institution gallery files.
12. `posts` — institution timeline posts.
13. `post_media` — post attachments.
14. `post_reactions` — one reaction per user per post.
15. `post_comments` — comments and one-level replies.
16. `institution_follows` — unique student/institution follow relationships.
17. `conversations` — private conversations.
18. `conversation_participants` — authorized conversation membership.
19. `messages` — persistent messages.
20. `message_receipts` — delivery/read receipts.
21. `scholarships` — institution scholarship listings and approval state.
22. `scholarship_documents` — scholarship attachments.
23. `applications` — student submissions.
24. `application_documents` — private application files.
25. `saved_scholarships` — unique student saved opportunities.
26. `notifications` — user notifications.
27. `reminder_logs` — duplicate-safe deadline reminder tracking.
28. `reports` — reported content and accounts.
29. `admin_actions` — administrative audit trail.

All IDs are UUID-style strings. Foreign keys and uniqueness constraints enforce core relationships. Review the model source files for exact SQLAlchemy column definitions.
