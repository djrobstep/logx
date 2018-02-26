targs = --cov-report term-missing --cov logx

pip:
	pip install -r requirements.txt

test:
	pytest $(targs)

lint:
	flake8 logx
	flake8 tests

clean:
	git clean -fXd
	find . -name \*.pyc -delete
	rm -rf .cache

publish:
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
