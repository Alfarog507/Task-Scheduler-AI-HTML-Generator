from collections import defaultdict, deque  # Importamos defaultdict y deque para manejar estructuras de datos

class TaskScheduler:
    def __init__(self):
        # Inicializamos un diccionario para almacenar las tareas y sus dependencias
        self.tasks = {}

    def add_task(self, task_id, dependencies=[]):
        """
        Agrega una tarea al programador con sus dependencias.
        - task_id: Identificador único de la tarea.
        - dependencies: Lista de tareas que deben completarse antes de esta tarea.
        """
        if task_id in self.tasks:
            raise ValueError(f'Task {task_id} already exists.')  # Evita duplicar tareas
        self.tasks[task_id] = dependencies  # Guarda la tarea junto con sus dependencias

    def remove_task(self, task_id):
        """
        Elimina una tarea del programador.
        - task_id: Identificador de la tarea que se desea eliminar.
        """
        if task_id not in self.tasks:
            raise ValueError(f'Task {task_id} does not exist.')  # Valida si la tarea existe
        del self.tasks[task_id]  # Elimina la tarea del diccionario

    def list_tasks(self):
        """
        Retorna la lista de todas las tareas registradas.
        """
        return list(self.tasks.keys())

    def find_execution_order(self):
        """
        Determina el orden en el que se deben ejecutar las tareas respetando las dependencias.
        Utiliza el algoritmo de ordenación topológica.
        """
        # 1. Inicializar grados de entrada (in-degree) para todas las tareas
        in_degree = {task: 0 for task in self.tasks}  # Todas las tareas comienzan con grado de entrada 0
        dependency_graph = defaultdict(list)  # Grafo para mapear relaciones entre tareas

        # 2. Construir el grafo de dependencias y calcular el grado de entrada
        for task, deps in self.tasks.items():
            for dep in deps:
                dependency_graph[dep].append(task)  # 'dep' es una dependencia de 'task'
                in_degree[task] += 1  # Incrementar el grado de entrada de la tarea dependiente

        # 3. Crear una cola para tareas con grado de entrada 0
        zero_in_degree = deque([task for task, degree in in_degree.items() if degree == 0])
        execution_order = []  # Lista para almacenar el orden de ejecución

        # 4. Procesar tareas con grado de entrada 0
        while zero_in_degree:
            task = zero_in_degree.popleft()  # Tomar una tarea sin dependencias pendientes
            execution_order.append(task)  # Agregarla al orden de ejecución

            # Reducir el grado de entrada de las tareas dependientes
            for dependent in dependency_graph[task]:
                in_degree[dependent] -= 1  # Reducir el grado de entrada
                if in_degree[dependent] == 0:  # Si ya no tiene dependencias pendientes
                    zero_in_degree.append(dependent)  # Agregar a la cola

        # 5. Verificar si se procesaron todas las tareas
        if len(execution_order) != len(self.tasks):
            raise ValueError("Circular dependency detected!")  # Si no, hay un ciclo

        return execution_order  # Devolver el orden de ejecución

# Ejemplo de uso con el input basados en la prueba unitaria
tasks = [
    {"id": "task1", "dependencies": []},
    {"id": "task2", "dependencies": ["task1"]},
    {"id": "task3", "dependencies": ["task1"]},
    {"id": "task4", "dependencies": ["task2", "task3"]},
]

scheduler = TaskScheduler()
for task in tasks:
    scheduler.add_task(task["id"], task["dependencies"])

execution_order = scheduler.find_execution_order()
print(execution_order)  # Salida esperada: ['task1', 'task2', 'task3', 'task4']
