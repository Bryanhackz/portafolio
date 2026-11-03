-- Añade índice para la limpieza periódica de oauth_states expirados (M-002).
CREATE INDEX IF NOT EXISTS ix_oauth_states_created
    ON oauth_states(created_at);