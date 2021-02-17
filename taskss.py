# task data base, creates task and stuff

class TaskData:
    def __init__(self, filename):
        self.filename = filename
        self.usertasks = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.usertasks = {}

        for line in self.file:
            taskname, description, time = line.strip().split(";")
            self.usertasks[taskname] = (description, time)

        self.file.close()

    def get_usertasks(self, taskname):
        if taskname in self.usertasks:
            return self.usertasks[taskname]
        else:
            return -1

    def add_usertasks(self, taskname, description, time):
        if taskname.strip() not in self.usertasks:
            self.usertasks[taskname.strip()] = (description.strip(), time.strip())
            self.save()
            return 1
        else:
            print("Data Already Exists")
            return -1

    def validate(self, taskname, description):
        if self.get_usertasks(taskname) != -1:
            return self.usertasks[taskname][0] == description
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for task in self.usertasks:
                f.write(task + ";" + self.usertasks[task][0] + ";" + self.usertasks[task][1] + "\n")