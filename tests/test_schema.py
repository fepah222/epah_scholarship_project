from app.extensions import db


def test_all_documented_tables_are_registered(app):
    expected = {
        "users", "email_verification_tokens", "password_reset_tokens", "user_settings",
        "admin_invitations", "student_profiles", "student_qualifications",
        "institution_profiles", "institution_documents", "media_albums",
        "institution_media", "posts", "post_media", "post_reactions", "post_comments",
        "institution_follows", "conversations", "conversation_participants", "messages",
        "message_receipts", "scholarships", "scholarship_documents", "applications",
        "application_documents", "saved_scholarships", "notifications", "reminder_logs",
        "reports", "admin_actions",
    }
    assert expected.issubset(set(db.metadata.tables))


def test_every_foreign_key_target_resolves(app):
    for table in db.metadata.tables.values():
        for column in table.columns:
            for foreign_key in column.foreign_keys:
                assert foreign_key.column.table.name in db.metadata.tables
