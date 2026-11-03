-- RLS se emula en data/authorizer.py (SQLite no implementa RLS nativa).
-- Este archivo solo garantiza los índices que soportan los predicados de autorización.

CREATE INDEX IF NOT EXISTS ix_projects_owner ON projects(owner_id);
CREATE INDEX IF NOT EXISTS ix_projects_published ON projects(published);
CREATE INDEX IF NOT EXISTS ix_messages_created ON messages(created_at DESC);
CREATE INDEX IF NOT EXISTS ix_messages_read ON messages(read);