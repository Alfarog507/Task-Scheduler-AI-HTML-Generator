# Python Utilities — Task Scheduler & AI HTML Generator

Two standalone Python modules exploring different problem spaces: graph-based task scheduling with cycle detection, and LLM-driven HTML generation with structural validation.

---

## Module 1 — Task Scheduler

A dependency-aware task scheduler that determines execution order using **Kahn's algorithm** (topological sort via BFS). Includes circular dependency detection that fails fast before any task runs.

### How it works

Tasks are stored in a directed graph using `defaultdict`. When `find_execution_order()` is called, it computes in-degree for each node and processes nodes with zero dependencies first via a `deque` queue — standard Kahn's algorithm. If any nodes remain unprocessed after the BFS, a cycle exists and the method raises an error.

```python
scheduler = TaskScheduler()
scheduler.add_task("deploy", dependencies=["build", "test"])
scheduler.add_task("build", dependencies=["lint"])
scheduler.add_task("lint")
scheduler.add_task("test", dependencies=["build"])

order = scheduler.find_execution_order()
# → ["lint", "build", "test", "deploy"]
```

### API

| Method | Description |
|---|---|
| `add_task(task_id, dependencies=[])` | Register a task with optional dependencies |
| `remove_task(task_id)` | Remove a task and its edges from the graph |
| `list_tasks()` | Return all registered task IDs |
| `find_execution_order()` | Return topologically sorted execution order, raises if cycle detected |

---

## Module 2 — AI HTML Generator

An LLM-powered HTML generator that takes a plain-language description and returns Tailwind CSS-styled HTML. Uses **DSPy** to structure the prompt-response contract, and Python's built-in `HTMLParser` to validate the output before returning it.

### How it works

DSPy defines a typed signature for the generation task — input: user description, output: valid HTML string. The module calls OpenAI under the hood via DSPy's LM abstraction. The response is then passed through `HTMLParser` to catch structural errors (unclosed tags, malformed attributes) before the result reaches the caller.

```python
generator = HTMLGenerator()
html = generator.generate("A centered card with a title, subtitle, and a blue CTA button")
# Returns validated Tailwind HTML or raises HTMLValidationError
```

### Why DSPy over a raw prompt

DSPy treats LLM calls as typed functions with declared inputs and outputs, rather than raw string templates. This makes the generation step composable and testable — the signature can be optimized or swapped without touching the calling code.

---

## Setup

```bash
pip install -r requirements.txt
```

**Environment variables**
```
OPENAI_API_KEY=your_key_here
```

---

## Files

| File | Description |
|---|---|
| `task_scheduler.py` | TaskScheduler class with topological sort and cycle detection |
| `html_generator.py` | HTMLGenerator class with DSPy + OpenAI + HTMLParser validation |
| `requirements.txt` | Python dependencies |
