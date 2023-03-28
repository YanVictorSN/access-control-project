from __future__ import annotations

import os
import pathlib
import subprocess


VENV_PATH = '.venv' if os.name == 'nt' else 'source .venv'
VENV_FOLDER = 'Scripts' if os.name == 'nt' else 'bin'

VENV_ACTIVATE = pathlib.Path(VENV_PATH, VENV_FOLDER, 'activate')
VENV_PYTHON = pathlib.Path(VENV_PATH, VENV_FOLDER, 'python')


def run_subprocess(*args):
    path = f'"{args[0]}"'
    arguments = ' '.join(args[1:])
    path_and_arguments = f'{path} {arguments}'
    command = f'{VENV_ACTIVATE} && {VENV_PYTHON} {path_and_arguments}'
    subprocess.Popen(command, shell=True)
