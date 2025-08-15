# Ranoparse
Парсер для [ranobehub.org](ranobehub.org), создающий на выходе EPUB

## 📦 Установка
1. Установите [Python](https://www.python.org/downloads/)
1. Установите [uv](https://github.com/astral-sh/uv):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Склонируйте репозиторий
```bash
git clone https://github.com/username/project-name.git
cd project-name
```
3. Установите зависимости
```bash
uv sync
```

## 🚀 Запуск
1. Установите директорию для скачивания ранобэ
```bash
uv run init.py {директория}
```
2. Запустите парсер
```bash
uv run app.py {ссылка на главную страницу ранобэ}
```
3. Спустя какое-то время в указанной папке появится папка со всеми томами ранобэ✨

## 🗑 Удаление
1. Удалите папку репозитория
- Linux:
```bash
rm -r Ranoparse
```
- Windows:
```powershell
rmdir Ranoparse
```
2. Удалите uv
```bash
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
# Linux
rm ~/.local/bin/uv ~/.local/bin/uvx
# Windows
rm $HOME\.local\bin\uv.exe
rm $HOME\.local\bin\uvx.exe
```
3. (Windows) Удалите Python через Настройки > Приложения
