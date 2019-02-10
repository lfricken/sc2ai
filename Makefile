isort:
    isort --recursive .

lint:
    flake8
    pydocstyle