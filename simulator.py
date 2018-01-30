import os.path
from repository import *


def main():
    # a dict to hold the workers current tasks
    assignments = {}

    while os.path.isfile('world.db') & (len(repo.tasks.find_all()) > 0):
        for task in repo.tasks.find_all():
            worker = repo.workers.find(id=task.worker_id)[0]
            if task.task_name not in assignments:
                if worker.id not in assignments.values():
                    resource = repo.resources.find(name=task.resource_name)[0]
                    new_amount = resource.amount - task.resource_amount
                    repo.resources.update(set_values={"amount": new_amount}, cond={"name": resource.name})

                    # change worker status to busy
                    repo.workers.update(set_values={"status": "busy"}, cond={"id": worker.id})
                    assignments[task.task_name] = worker.id
                    print("%s says: work work" % worker.name)
            else:
                print("%s is busy %s..." % (worker.name, task.task_name))
                # update task with one iteration
                repo.tasks.update(set_values={"time_to_make": task.time_to_make - 1},
                                    cond={"task_name": task.task_name})

        # check if the workers have finished their tasks
        finished = []
        for task_name in assignments:
            task = repo.tasks.find(task_name=task_name)[0]
            if task.time_to_make == 0:
                repo.workers.update(set_values={"status": "idle"}, cond={"id": task.worker_id})
                repo.tasks.delete(task_name=task.task_name)
                finished.append(task_name)
                print("%s says: All Done!" % repo.workers.find(id=task.worker_id)[0].name)

        for task_name in finished:
            assignments.pop(task_name)

if __name__ == '__main__':
    main()