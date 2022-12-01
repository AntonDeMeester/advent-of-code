PYTHON_FOLDERS := aoc_2022

check:
	isort --check-only  ${PYTHON_FOLDERS}
	black --check  ${PYTHON_FOLDERS}
	mypy ${PYTHON_FOLDERS}
	flake8  ${PYTHON_FOLDERS}
	radon cc  ${PYTHON_FOLDERS} -a -nc

reformat:
	isort  ${PYTHON_FOLDERS}
	black  ${PYTHON_FOLDERS}

test:
	pytest ${PYTHON_FOLDERS}