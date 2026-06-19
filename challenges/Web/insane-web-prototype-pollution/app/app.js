const express = require('express');
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const FLAG = process.env.FLAG || 'CTF{placeholder_flag_here}';

// Vulnerable deep merge function — no protección contra __proto__
function deepMerge(target, source) {
    for (const key in source) {
        if (source[key] && typeof source[key] === 'object') {
            if (!target[key]) target[key] = {};
            deepMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

// User database
const users = {
    guest: { password: 'guest123', settings: {} }
};

app.get('/', (req, res) => {
    res.send(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>SettingsCorp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}pre{background:#001100;padding:12px;font-size:.85rem}.hint{color:#009920;font-style:italic}</style></head><body>
<h1>SettingsCorp &mdash; User Preferences API</h1>
<div class="box"><p>API para gestionar preferencias de usuario. Aut&eacute;nticate y actualiza tu configuraci&oacute;n.</p></div>
<div class="box">
<h2 style="color:#00cc33;margin-bottom:10px">Endpoints</h2>
<pre>POST /login
  Body: {"username":"guest","password":"guest123"}

POST /settings/update  (requiere token)
  Header: Authorization: Bearer &lt;token&gt;
  Body: {"settings": {...}}

GET /admin/flag        (requiere isAdmin)
  Header: Authorization: Bearer &lt;token&gt;</pre></div>
<div class="box"><p class="hint">Las propiedades heredadas no siempre son tuyas &mdash; pero puedes contaminarlas.</p></div>
</body></html>`);
});

const tokens = {};

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (users[username] && users[username].password === password) {
        const token = Math.random().toString(36).substr(2);
        tokens[token] = username;
        return res.json({ token, message: 'Login successful' });
    }
    res.status(401).json({ error: 'Invalid credentials' });
});

app.post('/settings/update', (req, res) => {
    const token = (req.headers.authorization || '').replace('Bearer ', '');
    const username = tokens[token];
    if (!username) return res.status(401).json({ error: 'Unauthorized' });

    const newSettings = req.body.settings || {};
    // VULNERABLE: deepMerge con datos del usuario contamina Object.prototype
    deepMerge(users[username].settings, newSettings);

    res.json({ message: 'Settings updated', settings: users[username].settings });
});

app.get('/admin/flag', (req, res) => {
    const token = (req.headers.authorization || '').replace('Bearer ', '');
    const username = tokens[token];
    if (!username) return res.status(401).json({ error: 'Unauthorized' });

    const user = users[username];
    // isAdmin verificado directamente — prototype contaminado lo hace truthy
    if (!user.isAdmin) {
        return res.status(403).json({ error: 'Admin only', hint: 'Solo los administradores pueden ver esto' });
    }

    res.json({ flag: FLAG });
});

app.listen(80, () => console.log('SettingsCorp corriendo en :80'));
