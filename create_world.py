import sys
from repository import repo, Resource, Worker, Task


def main():
    repo.create_tables()
    input = open(sys.argv[1])
    for line in input:
        line = line.rstrip()
        args = line.split(',')
        # Resource
        if len(args) == 2:
            resource = Resource(*args)
            repo.resources.insert(resource)
        # Worker
        if len(args) == 3:
            args = args[1:]
            args.append("idle")
            worker = Worker(*args)
            repo.workers.insert(worker)
        # Task
        if len(args) == 5:
            task = Task(*args)
            repo.tasks.insert(task)


if __name__ == '__main__':
    main()