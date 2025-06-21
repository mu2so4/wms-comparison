# Apache Airflow + CWL-Airflow Demo

## 📌 Описание

[**Apache Airflow**](https://airflow.apache.org/) — один из самых популярных инструментов для оркестрации рабочих процессов (WMS). В данном проекте используется связка **Apache Airflow** и [**CWL-Airflow**](https://github.com/Barski-lab/cwl-airflow/) (v1.2.11) для запуска рабочих процессов, описанных в формате **CWL**.

Этот пример демонстрирует запуск существующего CWL-пайплайна через Airflow, при этом фактическое выполнение происходит через `cwltool`.

---

## ⚙️ Установка

### 🐍 Требуемые версии Python

- **Python 3.8** — для запуска Airflow и CWL-Airflow
- **Python 3.11** — для выполнения самого воркфлоу

> ❗ CWL-Airflow несовместим с Airflow выше версии 2.1.4, поэтому используется Airflow 2.1.4 + Python 3.8 (с Python 3.11 не запускается)

---

### 🔧 Установка Python 3.8 (если не установлен)

```bash
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev \
    libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev \
    libsqlite3-dev wget curl libbz2-dev liblzma-dev

cd /tmp
wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz
tar -xf Python-3.8.20.tgz
cd Python-3.8.20
./configure --enable-optimizations
sudo make altinstall
```

---

### 🛠️ Установка Airflow и CWL-Airflow

1. Убедитесь, что ваш CWL-воркфлоу корректно работает через `cwltool` (см. [соответствующий README.md](../cwltool/README.md)).
2. Перейдите в директорию `airflow/` проекта.
3. Выполните скрипт инициализации:
```bash
chmod +x init.sh
./init.sh
```

Если установка прошла успешно, вы увидите инструкции для запуска `Airflow`.

---

## 🚀 Запуск Airflow

### Терминал 1 — `scheduler`
```bash
source airflow-venv/bin/activate
airflow scheduler
```

### Терминал 2 — `webserver`
```bash
source airflow-venv/bin/activate
airflow webserver
```

После запуска веб-сервера откройте браузер: [http://localhost:8080](http://localhost:8080)  
Данные для входа:
- **Логин:** `admin`
- **Пароль:** `admin`

---

## ▶️ Запуск воркфлоу

Ваш DAG будет называться `seismic`.

1. Нажмите кнопку ▶️ напротив DAG.
2. Выберите **Trigger DAG w/ config**.
3. Подтвердите запуск.

Результаты будут сохранены в:
```
~/airflow/cwl_outputs
```

Журнал выполнения можно просматривать в интерфейсе или в терминале с `airflow scheduler`.

---

## 💡 Особенности

- 📊 Удобный и мощный **веб-интерфейс**
- 🧱 Использует **реализацию CWL через cwltool**, всё работает «как есть»
- 🐢 **Медленнее в 3 раза** по сравнению с прямым запуском
- ⚠️ **Сложная установка**, требует двух версий Python и строго определённых версий Airflow/CWL-Airflow
