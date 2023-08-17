VENV_NAME = venv

ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE = "$(VENV_NAME)/Scripts/activate"
else
	VENV_ACTIVATE = "$(VENV_NAME)/bin/activate"
endif

help:
	@echo "install - install all dependencies;"
	@echo "run - run server;"
	@echo "test - run all tests;"
	@echo "create_migration - create new database migration;"
	@echo "upgrade_db - apply all migrations to the latest version;"
	@echo "downgrade_db - roll back all migrations to the original version;"

install:
	$(VENV_ACTIVATE) && pip install -r requirements/base.txt

run:
	$(VENV_ACTIVATE) && python main.py

# Run all unit tests
test:
	$(VENV_ACTIVATE) && python -m unittest discover

freeze:
	$(VENV_ACTIVATE) && pip freeze > requirements/base.txt

.PHONY: alembic
# make create_migration name="your_migration_name"
create_migration:
	$(VENV_ACTIVATE) && alembic revision -m "$(name)"

upgrade_db:
	$(VENV_ACTIVATE) && alembic upgrade head

downgrade_db:
	$(VENV_ACTIVATE) && alembic downgrade base
