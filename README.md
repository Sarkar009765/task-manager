# Task Manager

[](#task-manager)

> A simple and elegant Task Management application with web GUI, built with Python and Flask.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](LICENSE)

---

## Features

- ✅ Add, complete, and delete tasks
- ✅ Priority levels (Critical, High, Medium, Low)
- ✅ Due dates
- ✅ Task tags
- ✅ Beautiful web interface
- ✅ Real-time statistics dashboard
- ✅ SQLite database (no setup required)
- ✅ Responsive design

---

## Installation

```bash
# Clone the project
git clone https://github.com/Sarkar009765/task-manager.git
cd task-manager

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Run the App

```bash
python web_gui.py
```

Then open: http://localhost:5000

### Use as Python Module

```python
from models import TaskModel

# Initialize
task_manager = TaskModel()

# Add a task
task_id = task_manager.add_task(
    title="Buy groceries",
    description="Milk, eggs, bread",
    priority="High",
    due_date="2026-05-15",
    tags="shopping,home"
)

# Get all tasks
tasks = task_manager.get_all_tasks()
for task in tasks:
    print(task['title'], task['status'])

# Complete a task
task_manager.complete_task(task_id)

# Delete a task
task_manager.delete_task(task_id)

# Get statistics
stats = task_manager.get_stats()
print(f"Total: {stats['total']}, Pending: {stats['pending']}, Completed: {stats['completed']}")
```

---

## Project Structure

```
task-manager/
├── models.py           # Task database operations
├── web_gui.py          # Flask web application
├── requirements.txt    # Python dependencies
├── tasks.db           # SQLite database (auto-created)
├── LICENSE            # MIT License
└── README.md          # This file
```

---

## How It Works

1. **models.py** - Contains `TaskModel` class for database operations
   - `add_task()` - Create new task
   - `get_all_tasks()` - Fetch all tasks
   - `complete_task()` - Mark task as complete
   - `delete_task()` - Delete a task
   - `get_stats()` - Get task statistics

2. **web_gui.py** - Flask web application
   - Beautiful UI with gradient design
   - Real-time statistics
   - Add/Complete/Delete tasks
   - Priority color coding

---

## Screenshots

The web interface includes:
- 📊 Dashboard with task statistics
- ➕ Add new task form
- 📋 Task list with priority badges
- ✅ Complete and delete actions

---

## Requirements

- Python 3.11+
- Flask 2.0+

---

## License

[MIT License](LICENSE) - Feel free to use this!

---

## Author

**Sarkar009765**

---

## Contributing

Contributions welcome! Fork the repo and submit a PR.