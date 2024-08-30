from pathlib import Path
from sys import argv
from datetime import date
import json

from rich import print
from rich.table import Table


HELP_TEXT = '''
[red]Commands[/]:
* [green bold]task-cli list [/][yellow] <todo || in-process || done>[/]           —  change task status
* [green bold]task-cli list[/]                                         —  show all tasks
* [green bold]task-cli update [/][yellow]<task ID: [/][blue]integer[/][yellow]> <new description> [/] —  set a new task description by its ID
* [green bold]task-cli delete [/][yellow]<task ID: [/][blue]integer[/][yellow]>[/]                    —  delete task by its ID
* [green bold]task-cli mark-in-progress [/][yellow]<task ID: [/][blue]integer[/][yellow]>[/]          —  set task status by its ID
* [green bold]task-cli mark-in-done [/][yellow]<task ID: [/][blue]integer[/][yellow]>[/]              —  set task status by its ID
* [green bold]task-cli mark-in-todo [/][yellow]<task ID: [/][blue]integer[/][yellow]>[/]              —  set task status by its ID
'''[1:-1]


class StatusTask:
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'
    ALL = 'all'


class Main:
    def __init__(self, args: list[str]):
        self.homeDir = Path('.')
        self.args = args
        self.JSONdata = []
        self.maxTaskID = 1


    def run(self):
        if not self.checkExistsFileJSON():
            with (self.homeDir / '.json').open('w', encoding='utf-8') as file:
                file.write('[]')
        
        else:
            with (self.homeDir / '.json').open('r', encoding='utf-8') as file:
                self.JSONdata = json.load(file)
                self.setMaxTaskID()
        
        self.commandMatch()
        self.writeInJSON()


    def commandMatch(self):
        match self.args:
            case ['add', description]:
                self.maxTaskID += 1
                todayDate = str( date.today() )
                
                self.JSONdata.append(
                    {
                        "id": self.maxTaskID,
                        "description": description,
                        "status": StatusTask.TODO,
                        "createdAt": todayDate,
                        "updatedAt": todayDate,
                    }
                )


            case ['list']:
                self.printTabel(
                    'Table of all tasks',
                    StatusTask.ALL
                )


            case ['list', StatusTask.DONE]:
                self.printTabel(
                    'Table of all completed tasks',
                    StatusTask.DONE
                )


            case ['list', StatusTask.IN_PROGRESS]:
                self.printTabel(
                    'Table of all tasks in progress',
                    StatusTask.IN_PROGRESS
                )


            case ['list', StatusTask.TODO]:
                self.printTabel(
                    'Todo table',
                    StatusTask.TODO
                )


            case ['list', errText]:
                print(
                    f'[red bold]Error! "{errText}" cannot be a parameter value![/]\n',
                    'Allowed values:\n',
                    '* [green]todo[/]\n',
                    '* [green]in-progress[/]\n',
                    '* [green]done[/]',
                )


            case ['delete', taskID]:
                ID = self.parseTaskID(taskID)

                i = self.findElementByTaskID(ID)
                self.JSONdata.pop(i)
            
            
            case ['update', taskID, description]:
                ID = self.parseTaskID(taskID)

                ID = self.findElementByTaskID(ID)
                self.JSONdata[i]['description'] = description


            case ['mark-in-progress', taskID]:
                ID = self.parseTaskID(taskID)

                i = self.findElementByTaskID(ID)
                self.JSONdata[i]['status'] = StatusTask.IN_PROGRESS


            case ['mark-done', taskID]:
                ID = self.parseTaskID(taskID)

                i = self.findElementByTaskID(ID)
                self.JSONdata[i]['status'] = StatusTask.DONE


            case ['mark-todo', taskID]:
                ID = self.parseTaskID(taskID)

                i = self.findElementByTaskID(ID)
                self.JSONdata[i]['status'] = StatusTask.TODO

            case ['help' | '/?'] | []:
                print(HELP_TEXT)

            case _:
                print(
                    '[red bold]Error! Task-cli does not accept such parameters![/]\n'
                    '[green](i) Type "task-cli help" for available commands[/]'
                )
                exit(1) 

    def writeInJSON(self):
        with (self.homeDir / '.json').open('w', encoding='utf-8') as file:
            json.dump(self.JSONdata, file, ensure_ascii=False)


    def setMaxTaskID(self):
        for task in self.JSONdata:
            if task['id'] > self.maxTaskID:
                self.maxTaskID = task['id']
    

    def findElementByTaskID(self, ID: int) -> int:
        for i in range( len(self.JSONdata) ):
            if self.JSONdata[i]['id'] == ID:
                return i
            

    def printTabel(self, title: str, status: StatusTask):
        result = Table(title=title)
        tasks: list = self.JSONdata

        if status != StatusTask.ALL:
            tasks = filter(
                lambda elem: True if elem['status'] == status else False,
                self.JSONdata
            )
            tasks = list(tasks)

        result.add_column('ID')
        result.add_column('Discription')
        result.add_column('Status')
        result.add_column('Created at')
        result.add_column('Updated at')

        for task in tasks:
            result.add_row(
                str(task['id']),
                str(task['description']),
                str(task['status']),
                str(task['createdAt']),
                str(task['updatedAt']),
            )

        print(result)
    

    def parseTaskID(self, taskID):
        try:
            ID = int(taskID)
            self.checkCLITaskID(ID)
            return ID
        except:
            print('[red bold]Error! The second parameter must be an integer![/]')
            exit(1)


    def checkExistsFileJSON(self) -> bool:
        return (self.homeDir / '.json').exists()
    

    def checkCLITaskID(self, ID: int) -> bool:
        for task in self.JSONdata:
            if task['id'] == ID:
                return True
        
        print('[red bold]Error! There is no task with the specified ID![/]')
        exit(1)


if __name__ == '__main__':
    app = Main(argv[1:])
    app.run()
