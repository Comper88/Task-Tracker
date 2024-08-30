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


class StatusTask(object):
    '''
    Enum representing all possible task statuses
    '''

    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'
    ALL = 'all'


class Main(object):
    def __init__(self, args: list[str]):
        ...


    def run(self):
        '''
        Function to run the main class
        '''


    def commandMatch(self):
        '''
        Makes connections between CLI commands and their logic
        '''


    def writeInJSON(self):
        '''
        Writes the resulting JSON object to a ".json" file
        '''


    def setMaxTaskID(self):
        '''
        Finds out the maximum ID among all tasks
        '''


    def printTabel(self, title: str, status: StatusTask):
        '''
        Creates a table with tasks according
        to their specified status
        '''


    def checkCLITaskID(self, ID: int) -> bool:
        '''
        Checks that the passed ID exists among tasks
        '''
    

    def findElementByTaskID(self, ID: int) -> int:
        ...


    def checkExistsFileJSON(self) -> bool:
        ...
