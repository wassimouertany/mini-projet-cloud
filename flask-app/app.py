import os
import redis
import json
from flask import Flask, request, jsonify
from models import db, Task
from prometheus_flask_exporter import PrometheusMetrics
import socket


app = Flask(__name__)

# ── Config base de données ──────────────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://admin:admin@db:5432/tasks'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── Init extensions ─────────────────────────────────────────────
db.init_app(app)
metrics = PrometheusMetrics(app)

# ── Redis ───────────────────────────────────────────────────────
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

CACHE_KEY = 'tasks_cache'

# ── Routes ──────────────────────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Essaie le cache Redis d'abord
    cached = redis_client.get(CACHE_KEY)
    if cached:
        return jsonify({'source': 'cache', 'tasks': json.loads(cached)}), 200

    tasks = Task.query.all()
    result = [t.to_dict() for t in tasks]

    # Stocke en cache 30 secondes
    redis_client.setex(CACHE_KEY, 30, json.dumps(result))

    return jsonify({'source': 'db', 'tasks': result}), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Le champ title est requis'}), 400

    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()

    # Invalide le cache
    redis_client.delete(CACHE_KEY)

    return jsonify(task.to_dict()), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'done' in data:
        task.done = data['done']

    db.session.commit()
    redis_client.delete(CACHE_KEY)

    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    # Invalide le cache
    redis_client.delete(CACHE_KEY)

    return jsonify({'message': f'Tâche {task_id} supprimée'}), 200


@app.route('/visits')
def visits():
    count = redis_client.incr('visit_counter')
    return jsonify({'visits': count}), 200

@app.route('/whoami')
def whoami():
    return jsonify({
        'container': socket.gethostname(),
        'instance': os.getenv('HOSTNAME', 'unknown')
    }), 200

# ── Démarrage ───────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)