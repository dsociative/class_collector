ENV=.env
PYTHON=$(ENV)/bin/python

all: clean venv

venv:
	virtualenv .env
	@echo Install PIP inside virtual environment
	./$(ENV)/bin/easy_install pip

	@echo Activate virtual env
	. $(ENV)/bin/activate

	@echo Installing dependencies
	./$(ENV)/bin/pip install --download-cache ~/pip -r ./requirements.txt

clean:
	rm -rf $(ENV)


tests:
	$(PYTHON)
