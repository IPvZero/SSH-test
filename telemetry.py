from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from datetime import date
import pathlib
import os
import colorama
from colorama import Fore, Style

clear_command = "clear"
os.system(clear_command)
print(Fore.YELLOW + "Nornir is retrieving network telemetry...")
def backup_configurations(task):
    commands = "show run", "show cdp neighbor detail", "show version", "show clock", "show logging"
    for cmd in commands:
        name = str(cmd)
        folder = name.replace(" ", "-")
        config_dir = "config-archive"
        date_dir = config_dir + "/" + str(date.today())
        command_dir = date_dir + "/" + folder
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)
        r = task.run(task=send_command, command=cmd)
        task.run(
            task=write_file,
            content=r.result,
            filename=f"" + str(command_dir) + "/" + task.host.name + ".txt",
     )

nr = InitNornir(config_file="config.yaml")


result = nr.run(
    name="Creating Backup Archive", task=backup_configurations
)


os.system(clear_command)
print(Fore.GREEN + "Archive Created")
