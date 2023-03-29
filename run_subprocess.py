from __future__ import annotations

import os
import subprocess


VENV_PATH = '.venv' if os.name == 'nt' else 'source .venv'
VENV_FOLDER = 'Scripts' if os.name == 'nt' else 'bin'

VENV_ACTIVATE = os.path.join(VENV_PATH, VENV_FOLDER, 'activate')
VENV_PYTHON = os.path.join(VENV_PATH, VENV_FOLDER, 'python')


def run_subprocess(*args):
    path = f'"{args[0]}"'
    arguments = ' '.join(args[1:])
    path_and_arguments = f'{path} {arguments}'
    command = f'{VENV_ACTIVATE} && {VENV_PYTHON} {path_and_arguments}'
    subprocess.Popen(command, shell=True)


def convert_ui_files():
    ui_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
    for file in os.listdir(ui_folder):
        if file.endswith('.ui'):
            input_file = os.path.join(ui_folder, file)
            output_file = os.path.join(ui_folder, f'ui_{file[:-3]}.py')
            subprocess.run(['pyuic5', '-o', output_file, input_file])


convert_ui_files()
