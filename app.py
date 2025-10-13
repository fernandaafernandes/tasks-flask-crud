from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# CRUD
tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json() or {}
    new_task = Task(
        id=task_id_control, title=data["title"], description=data.get("description", "")
    )
    task_id_control += 1
    tasks.append(new_task)
    return (
        jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id}),
        200,
    )


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return (
        jsonify({"tasks": [t.to_dict() for t in tasks], "total_tasks": len(tasks)}),
        200,
    )


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id: int):
    task = next((t for t in tasks if t.id == id), None)
    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    return jsonify(task.to_dict()), 200


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json() or {}
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if hasattr(task, "completed") and "completed" in data:
        task.completed = data["completed"]

    return (
        jsonify({"message": "Tarefa atualizada com sucesso", "task": task.to_dict()}),
        200,
    )


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
