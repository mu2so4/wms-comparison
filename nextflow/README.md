# Nextflow Workflow Demo

## 🧩 Описание

[**Nextflow**](https://www.nextflow.io) — мощный и гибкий инструмент управления workflow, ориентированный на reproducible science. Позволяет легко масштабировать задачи от локального запуска до облака и HPC-систем.

В этом примере демонстрируется запуск двухэтапного workflow на Nextflow, полученного автоматическим преобразованием из скрипта CWL с помощью библиотеки **Janis**.

---

## ⚙️ Установка и подготовка

### 🔧 Требования
- **Java** версии **от 17 до 23**

---

### 📦 Установка Nextflow
[Документация по установке](https://www.nextflow.io/docs/latest/install.html)

**Required Python version: 3.11**
1. Ensure you are in the fireworks directory, which contains the init.sh script.
2. Run the installation (`sudo` required):
```
./init.sh
```

This will set up a virtual environment `.nextflow-venv`, install Nextflow and its dependencies (including Janise) and convert the CWL into Nextflow format.

---

## 🔁 Конвертация из CWL в Nextflow с помощью Janis

Для автоматического преобразования используется [**Janis**](https://janis.readthedocs.io/en/translate-docs/index.html) — инструмент для трансляции workflow между различными системами, включая CWL и Nextflow.

> ✅ Janis уже включён в `requirements.txt`

### 🔄 Шаги

1. Убедитесь, что CWL-скрипт успешно запускается с помощью `cwltool` (см. [инструкцию](../cwltool/README.md)). Все пути должны быть абсолютными.
2. Запустите трансляцию:
```bash
# Из папки nextflow/
janis translate --from cwl --to nextflow ../cwltool/main.cwl
```

Конвертация тестового Workflow уже включена в `init.sh`.

### 📂 Полученная структура
```
translated/
│── main.nf
│── nextflow.config
└── modules/
    ├── task1.nf
    └── task2.nf
```

- `main.nf` — основной файл pipeline
- `modules/*.nf` — этапы workflow
- `nextflow.config` — конфигурация параметров

---

## 🛠️ Конфигурация

1. В `nextflow.config` укажите значения параметров (`inpFile`, пути к скриптам `task1.py`, `task2.py` и др.)
2. В `modules/task1.nf` и `modules/task2.nf` **удалите строки, начинающиеся с `container`**, если не используете контейнеры (Singularity/Docker). Они идут первыми в блоке `process`.

---

## 🚀 Запуск

```bash
source nextflow-venv/bin/activate  # если ещё не активировано
nextflow run main.nf
```

---

## 🧩 Особенности Nextflow

- 🐌 **Работает примерно в 2 раза медленнее**, чем запуск напрямую без WMS
- 🔁 **Успешно применён парсер CWL** — Janis корректно транслирует pipeline
- ⚙️ **Поддержка контейнеров (Docker/Singularity)** — при необходимости можно использовать контейнеры
