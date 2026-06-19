/*
 * Lab02 Node.js API — JWT + SSRF vulnerable (educativo)
 */
const express   = require('express');
const jwt       = require('jsonwebtoken');
const axios     = require('axios');
const bodyParser= require('body-parser');

const app    = express();
const SECRET = process.env.JWT_SECRET || 'default_weak_secret';
app.use(bodyParser.json());

const USERS = {
  guest: { password: 'guest123', role: 'guest' },
  admin: { password: 'adm1nP4ss', role: 'admin' },
};

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'lab02-api' }));

// LOGIN — emite JWT con secret débil
app.post('/api/login', (req, res) => {
  const { user, pass } = req.body || {};
  const u = USERS[user];
  if (u && u.password === pass) {
    const token = jwt.sign({ user, role: u.role }, SECRET, { expiresIn: '1h' });
    return res.json({ token });
  }
  res.status(401).json({ error: 'Invalid credentials' });
});

// MIDDLEWARE — verifica JWT (vulnerable a alg:none y weak secret)
function authMiddleware(req, res, next) {
  const auth = req.headers.authorization || '';
  const token = auth.replace('Bearer ', '');
  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch (e) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// ADMIN endpoint — requiere role=admin
app.get('/api/admin/flag', authMiddleware, (req, res) => {
  if (req.user.role !== 'admin')
    return res.status(403).json({ error: 'Forbidden' });
  res.json({ flag: 'FLAG{jwt_w34k_s3cr3t_byp4ss3d}', hint: 'Flag #2 — JWT Admin' });
});

// SSRF endpoint — vulnerable: acepta URLs arbitrarias
app.post('/api/fetch', authMiddleware, async (req, res) => {
  const { url } = req.body || {};
  if (!url) return res.status(400).json({ error: 'url required' });
  try {
    const resp = await axios.get(url, { timeout: 3000 });
    res.json({ status: resp.status, data: resp.data });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.listen(3000, () => console.log('Lab02 API on :3000'));
