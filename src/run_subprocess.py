from __future__ import annotations

import os
import subprocess


VENV_PATH = '.venv' if os.name == 'nt' else 'source .venv'
VENV_FOLDER = 'Scripts' if os.name == 'nt' else 'bin'

VENV_ACTIVATE = os.path.join(VENV_PATH, VENV_FOLDER, 'activate')
VENV_PYTHON = os.path.join(VENV_PATH, VENV_FOLDER, 'python')


def run_subprocess(*args):
    path_and_arguments = ' '.join(args)
    command = f'{VENV_ACTIVATE} && {VENV_PYTHON} "{path_and_arguments}"'
    subprocess.Popen(command, shell=True)
