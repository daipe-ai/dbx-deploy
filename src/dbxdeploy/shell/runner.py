import io
import os
import subprocess


def run_and_read_output(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, shell=shell)
    output = io.TextIOWrapper(proc.stdout, encoding="utf-8").read().rstrip()

    if not output:
        raise Exception(f"No output returned to stdout for: {command}")

    return output


def run_shell_command(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, shell=shell)
    proc.communicate()

    if proc.returncode > 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}")
