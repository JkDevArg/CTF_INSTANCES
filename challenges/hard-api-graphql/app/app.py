import os
import graphene
from flask import Flask, request, jsonify, render_template_string

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# Data store
USERS = {
    1: {"id": 1, "username": "admin", "email": "admin@corp.internal", "private_note": FLAG},
    2: {"id": 2, "username": "alice", "email": "alice@corp.com", "private_note": "Meeting at 3pm"},
    3: {"id": 3, "username": "bob", "email": "bob@corp.com", "private_note": "Buy milk"},
}


class UserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    private_note = graphene.String()  # This is what players must discover


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)

    def resolve_user(root, info, id):
        u = USERS.get(id)
        if not u:
            return None
        return UserType(**u)

    def resolve_users(root, info):
        return [UserType(**u) for u in USERS.values()]


schema = graphene.Schema(query=Query)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GraphCore API</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
    min-height: 100vh;
    padding: 40px 20px;
  }
  .container { max-width: 860px; margin: 0 auto; }
  h1 {
    font-size: 2.2rem;
    color: #ff6b6b;
    margin-bottom: 8px;
    letter-spacing: 2px;
  }
  .tag {
    display: inline-block;
    background: #6e040f;
    color: #ff9999;
    padding: 3px 12px;
    border-radius: 4px;
    font-size: 0.78rem;
    letter-spacing: 1px;
    margin-bottom: 28px;
    text-transform: uppercase;
  }
  .story {
    border-left: 3px solid #ff6b6b;
    padding: 14px 20px;
    font-style: italic;
    color: #8b949e;
    background: #161b22;
    border-radius: 0 6px 6px 0;
    margin-bottom: 32px;
  }
  h2 {
    color: #e6edf3;
    font-size: 1.1rem;
    margin-bottom: 14px;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px;
  }
  .endpoint {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 16px;
  }
  .method {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 10px;
  }
  .get { background: #1f6feb; color: #fff; }
  .post { background: #238636; color: #fff; }
  .ep-path { color: #79c0ff; font-size: 1rem; }
  .ep-desc { color: #8b949e; font-size: 0.88rem; margin-top: 8px; }
  pre {
    background: #010409;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    font-size: 0.85rem;
    color: #e6edf3;
    margin-top: 10px;
    line-height: 1.5;
  }
  .hint {
    margin-top: 36px;
    padding: 14px 20px;
    border: 1px dashed #6e040f;
    border-radius: 6px;
    color: #ff9999;
    font-size: 0.88rem;
    background: #0d0608;
  }
  .hint-label {
    color: #ff6b6b;
    font-weight: bold;
    display: block;
    margin-bottom: 4px;
  }
</style>
</head>
<body>
<div class="container">
  <h1>GraphCore API</h1>
  <span class="tag">hard &bull; api</span>

  <div class="story">
    Una plataforma interna usa GraphQL para exponer su API de usuarios.
    La documentación es mínima — solo saben que existe un endpoint <code>/graphql</code>.
    Pero GraphQL habla por sí mismo. Cada campo, cada tipo, cada secreto.
  </div>

  <h2>Endpoints</h2>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/graphql?query={...}</span>
    <div class="ep-desc">Ejecuta una query GraphQL via query param.</div>
  </div>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/graphql</span>
    <div class="ep-desc">Ejecuta una query GraphQL. Body: <code>{"query": "..."}</code></div>
    <pre>curl -s -X POST http://&lt;host&gt;/graphql \\
  -H "Content-Type: application/json" \\
  -d '{"query": "{ users { id username email } }"}'</pre>
  </div>

  <h2>Ejemplo — Listar usuarios</h2>
  <pre>curl -s -X POST http://&lt;host&gt;/graphql \\
  -H "Content-Type: application/json" \\
  -d '{"query": "{ users { id username email } }"}'

# Respuesta:
{
  "data": {
    "users": [
      {"id": 1, "username": "admin", "email": "admin@corp.internal"},
      {"id": 2, "username": "alice", "email": "alice@corp.com"},
      {"id": 3, "username": "bob",   "email": "bob@corp.com"}
    ]
  }
}</pre>

  <h2>Consulta por ID</h2>
  <pre>curl -s -X POST http://&lt;host&gt;/graphql \\
  -H "Content-Type: application/json" \\
  -d '{"query": "{ user(id: 2) { username email } }"}'</pre>

  <div class="hint">
    <span class="hint-label">// HINT</span>
    GraphQL puede contarte su propio esquema si le preguntas de la manera correcta.
    Algunos campos no aparecen en los ejemplos, pero eso no significa que no existan.
  </div>
</div>
</body>
</html>"""

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/graphql', methods=['GET', 'POST'])
def graphql():
    if request.method == 'GET':
        query = request.args.get('query', '')
    else:
        data = request.get_json(silent=True) or {}
        query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    result = schema.execute(query)
    response = {}
    if result.data:
        response['data'] = result.data
    if result.errors:
        response['errors'] = [str(e) for e in result.errors]
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
