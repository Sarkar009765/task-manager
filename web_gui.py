from flask import Flask, render_template_string, request, jsonify
from models import TaskModel

app = Flask(__name__)
model = TaskModel()

@app.route('/')
def index():
    tasks = model.get_all_tasks()
    stats = model.get_stats()
    tasks_list = [dict(t) for t in tasks]
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 25px;
            font-size: 2em;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 25px;
            gap: 15px;
        }
        .stat-card {
            flex: 1;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }
        .stat-card h3 {
            font-size: 2.5em;
            margin: 0;
        }
        .stat-card p {
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        .add-btn {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .add-btn:hover {
            transform: scale(1.02);
        }
        .task-list {
            display: grid;
            gap: 15px;
        }
        .task-card {
            background: #fff;
            border-left: 5px solid #ccc;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .task-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.12);
        }
        .priority-Critical { border-left-color: #e74c3c; }
        .priority-High { border-left-color: #e67e22; }
        .priority-Medium { border-left-color: #f1c40f; }
        .priority-Low { border-left-color: #2ecc71; }
        .task-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        .task-desc {
            color: #666;
            margin-bottom: 10px;
        }
        .tags {
            margin: 10px 0;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            background: #f0f0f0;
            margin-right: 5px;
            color: #555;
        }
        .task-meta {
            font-size: 0.85em;
            color: #888;
            margin-top: 10px;
        }
        .task-actions {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.8; }
        .btn-complete { background: #2ecc71; color: white; }
        .btn-delete { background: #e74c3c; color: white; }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 1000;
        }
        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            width: 90%;
            max-width: 500px;
            border-radius: 15px;
            position: relative;
        }
        .close {
            position: absolute;
            right: 20px;
            top: 15px;
            font-size: 28px;
            cursor: pointer;
            color: #999;
        }
        .close:hover { color: #333; }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            font-weight: bold;
            color: #555;
            margin-bottom: 5px;
        }
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 1em;
        }
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }
        .save-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        @media (max-width: 600px) {
            .stats { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Task Manager</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{{ stats.total }}</h3>
                <p>Total Tasks</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);">
                <h3>{{ stats.pending }}</h3>
                <p>Pending</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);">
                <h3>{{ stats.completed }}</h3>
                <p>Completed</p>
            </div>
        </div>
        
        <button class="add-btn" onclick="showModal()">➕ Add New Task</button>
        
        <div class="task-list">
            {% for task in tasks %}
            <div class="task-card priority-{{ task['priority'] }}">
                <div class="task-title">{{ task['title'] }}</div>
                <div class="task-desc">{{ task['description'] or 'No description' }}</div>
                <div class="tags">
                    <span class="badge">{{ task['priority'] }}</span>
                    <span class="badge">{{ task['status'] }}</span>
                    {% if task['tags'] %}
                    <span class="badge">🏷 {{ task['tags'] }}</span>
                    {% endif %}
                </div>
                <div class="task-meta">
                    📅 Due: {{ task['due_date'] or 'No date' }}
                </div>
                <div class="task-actions">
                    {% if task['status'] == 'Pending' %}
                    <button class="btn btn-complete" onclick="completeTask({{ task['id'] }})">✓ Complete</button>
                    {% endif %}
                    <button class="btn btn-delete" onclick="deleteTask({{ task['id'] }})">🗑 Delete</button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <!-- Modal -->
    <div id="taskModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>Add New Task</h2>
            
            <div class="form-group">
                <label>Title *</label>
                <input type="text" id="title" placeholder="What needs to be done?">
            </div>
            
            <div class="form-group">
                <label>Description</label>
                <textarea id="desc" placeholder="Task details..."></textarea>
            </div>
            
            <div class="form-group">
                <label>Priority</label>
                <select id="priority">
                    <option value="Low">Low</option>
                    <option value="Medium" selected>Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Due Date</label>
                <input type="date" id="dueDate">
            </div>
            
            <div class="form-group">
                <label>Tags (comma separated)</label>
                <input type="text" id="tags" placeholder="work, urgent, personal">
            </div>
            
            <button class="save-btn" onclick="saveTask()">Save Task</button>
        </div>
    </div>
    
    <script>
        function showModal() {
            document.getElementById('taskModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('taskModal').style.display = 'none';
        }
        
        function saveTask() {
            const data = {
                title: document.getElementById('title').value,
                description: document.getElementById('desc').value,
                priority: document.getElementById('priority').value,
                due_date: document.getElementById('dueDate').value,
                tags: document.getElementById('tags').value
            };
            
            if (!data.title) {
                alert('Please enter a title!');
                return;
            }
            
            fetch('/add_task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(() => location.reload());
        }
        
        function completeTask(id) {
            fetch('/complete/' + id, {method: 'POST'}).then(() => location.reload());
        }
        
        function deleteTask(id) {
            if (confirm('Delete this task?')) {
                fetch('/delete/' + id, {method: 'DELETE'}).then(() => location.reload());
            }
        }
        
        window.onclick = function(event) {
            if (event.target == document.getElementById('taskModal')) {
                closeModal();
            }
        }
    </script>
</body>
</html>'''
    return render_template_string(html, tasks=tasks_list, stats=stats)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    data = request.json
    model.add_task(
        data['title'], 
        data.get('description'), 
        data.get('priority', 'Medium'), 
        data.get('due_date'), 
        data.get('tags')
    )
    return jsonify({'success': True})

@app.route('/complete/<int:id>', methods=['POST'])
def complete_route(id):
    model.complete_task(id)
    return jsonify({'success': True})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_route(id):
    model.delete_task(id)
    return jsonify({'success': True})

if __name__ == '__main__':
    print("🚀 Task Manager Starting...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, port=5000)