#!/usr/bin/env python3
"""TaskMaster – a tiny CLI to‑do list manager.

Provides sub‑commands:
  add <task>        Add a new task
  list [--all]      List pending tasks (default) or all tasks with --all
  complete <id>      Mark task with given ID as completed
  delete <id>        Remove task with given ID

Data is persisted in a local JSON file named 'tasks.json' in the same
directory as this script.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# ----- Constants -----
DATA_FILE = Path(__file__).with_name("tasks.json")

# ----- Helper Functions -----
def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from the JSON file.
    Returns an empty list if the file does not exist or is malformed.
    """
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[error] Failed to read tasks: {e}", file=sys.stderr)
        return []

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Write the tasks list back to the JSON file atomically."""
    try:
        tmp_file = DATA_FILE.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, sort_keys=True)
        tmp_file.replace(DATA_FILE)
    except OSError as e:
        print(f"[error] Could not save tasks: {e}", file=sys.stderr)
        sys.exit(1)

def get_next_id(tasks: List[Dict[str, Any]]) -> int:
    """Return the next integer ID for a new task."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def find_task(tasks: List[Dict[str, Any]], task_id: int) -> Dict[str, Any]:
    """Return the task dict matching *task_id* or raise ValueError."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task with id {task_id} not found")

# ----- Command Implementations -----
def cmd_add(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": args.title,
        "completed": False,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task [{new_task['id']}]: {new_task['title']}")

def cmd_list(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    filtered = tasks if args.all else [t for t in tasks if not t["completed"]]
    if not filtered:
        print("No pending tasks.")
        return
    for task in filtered:
        status = "✔" if task["completed"] else "✗"
        print(f"[{task['id']}] {status} {task['title']}")

def cmd_complete(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    try:
        task = find_task(tasks, args.id)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    if task["completed"]:
        print(f"Task [{task['id']}] is already completed.")
        return
    task["completed"] = True
    save_tasks(tasks)
    print(f"Marked task [{task['id']}] as completed.")

def cmd_delete(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    try:
        task = find_task(tasks, args.id)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Deleted task [{task['id']}].")

# ----- Argument Parser Setup -----
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskmaster.py", description="Simple CLI to‑do list manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", help="Title of the task")
    parser_add.set_defaults(func=cmd_add)

    # list
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("--all", action="store_true", help="Show all tasks, including completed")
    parser_list.set_defaults(func=cmd_list)

    # complete
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("id", type=int, help="ID of the task to complete")
    parser_complete.set_defaults(func=cmd_complete)

    # delete
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="ID of the task to delete")
    parser_delete.set_defaults(func=cmd_delete)

    return parser

# ----- Main Entrypoint -----
def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    # Dispatch to the appropriate command function
    args.func(args)

if __name__ == "__main__":
    main()
