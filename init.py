import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    raise ValueError("Использование: uv run init.py {директория для сохранения ранобэ}")

dir_path = Path(sys.argv[1])

if not os.path.isdir(str(dir_path)):
    raise ValueError("Убедитесь, что директория существует")

with open("config.txt", "w") as f:
    f.write(str(dir_path))
    