targs = --cov-report term-missing --cov logx --cov logxutil

pip:
	pip install -r requirements.txt

test:
	pytest $(targs)

fmt:
	black .

lint:
	flake8 .

clean:
	git clean -fXd
	find . -name \*.pyc -delete
	rm -rf .cache

publish:
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
