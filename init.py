import sys
import os
from pathlib import Path
import logging


if len(sys.argv) != 2:
    logging.error("Использование: uv run init.py {директория для сохранения ранобэ}")
    exit(1)

dir_path = Path(sys.argv[1])

if not os.path.isdir(str(dir_path)):
    logging.error("Убедитесь, что директория существует")
    exit(2)

with open("config.txt", "w") as f:
    f.write(str(dir_path))
    