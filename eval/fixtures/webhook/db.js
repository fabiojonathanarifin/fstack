// Thin wrapper over Postgres. query(sql, params) returns { rows }.
const { Pool } = require('pg');
const pool = new Pool();
module.exports = { query: (sql, params) => pool.query(sql, params) };
// Tables: wallets(user_id, balance_cents), ledger(id, user_id, amount_cents, source, source_id, created_at)
