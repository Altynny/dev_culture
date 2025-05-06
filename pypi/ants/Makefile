help:
	@echo "Make project with following instructions"
	@cat Makefile

dev:
	pipenv install --dev

test: dev
	pipenv run pytest --doctest-modules --junitxml=junit/test-results.xml

build: clean
	pipenv install wheel
	pipenv run python setup.py sdist bdist_wheel

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/ 
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete