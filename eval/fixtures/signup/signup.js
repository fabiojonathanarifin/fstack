const db = require('./db');

async function signUp(email, name) {
  const { rows } = await db.query('insert into users(email, name) values ($1, $2) returning id', [email, name]);
  return rows[0].id;
}

module.exports = { signUp };
