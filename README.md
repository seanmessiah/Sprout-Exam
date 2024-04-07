# Sprout-Exam

### Prerequisites
- [Python 3.9](https://python.org)
- [PostgreSQL](https://www.postgresql.org/)

### Backend Setup
1. Create virtual environment using `Python 3.9`. 

```shell
pip install virtualenv
python3.9 -m venv env
source env/bin/activate
```

2. Install dependencies.

```shell
pip install -r requirements.txt
```

3. Copy sample .env file and fill in settings.

```shell
cd backend 
cp .env.example .env
```

4. Create database if missing.

```shell
sudo -u postgres -i
createdb SproutEMS
```

5. Run the local server.

```shell
cd backend
uvicorn main:app --reload
```