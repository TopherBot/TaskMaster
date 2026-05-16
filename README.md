# TaskMaster

TaskMaster is a simple, zero‑dependency command‑line to‑do list manager written in Python 3.

## Features
- Add a new task
- List all pending/completed tasks
- Mark a task as completed
- Remove a task
- Persistent storage in a local `tasks.json`

## Installation
```bash
# Clone the repository (or copy the files)
git clone https://github.com/yourusername/TaskMaster.git
cd TaskMaster

# Ensure you have Python 3.8+ installed
python3 --version
```

## Usage
```bash
# Add a task
taskmaster.py add "Buy groceries"

# List tasks
taskmaster.py list

# Mark a task as done
taskmaster.py complete 1

# Remove a task
taskmaster.py delete 2
```

Run `taskmaster.py --help` for a full list of commands and options.

## Contributing
Feel free to open issues or submit pull requests. Please keep code style consistent (PEP 8) and add tests for new features.

## License
This project is licensed under the MIT License – see the `LICENSE` file for details.
