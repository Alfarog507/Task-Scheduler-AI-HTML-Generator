This project consists of two main modules:

Task Scheduler: A task scheduler that allows managing and ordering tasks based on dependencies using a topological sorting algorithm.
HTMLGenerator: An HTML generator and validator that verifies the correctness of the HTML documents generated based on user instructions using Tailwind CSS.

1. Task Scheduler:
Description:

The TaskScheduler class allows managing tasks, adding dependencies, removing tasks, and determining the execution order respecting dependencies.
It uses data structures like defaultdict to manage dependencies and deque for execution queues.
It includes validation to detect circular dependencies in the task graph.
Key Functions:

- add_task(task_id, dependencies=[]): Adds a task to the scheduler with its dependencies.
- remove_task(task_id): Removes a task from the scheduler.
- list_tasks(): Returns the list of all registered tasks.
- find_execution_order(): Determines the order in which tasks should be executed respecting their dependencies.

HTMLGenerator Class in Python
Description:
The HTMLGenerator class provides functionality to generate HTML content based on user descriptions. It uses the dspy library to interact with the model and generate HTML using Tailwind CSS.

- Generate HTML: Generates valid HTML code based on a given user description.
- HTML Validation: Uses HTMLParser to parse and validate the HTML output for any errors.
