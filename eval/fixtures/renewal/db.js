// query(sql, params) -> { rows }
const { Pool } = require('pg');
const pool = new Pool();
module.exports = { query: (sql, params) => pool.query(sql, params) };
// Tables: subscriptions(id, customer_id, price_cents, period_end), charges(id, subscription_id, period_end, payment_intent_id, created_at)
