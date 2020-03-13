.DEFAULT_GOAL := help

###### Development

compile-requirements: ## Compile *.txt requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in

upgrade-requirements: ## Upgrade all requirements
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in

format: ## Format source code
	black ./onthego

build: ## Build python source package
	python setup.py sdist

pypi: build ## Send source package to pypi
	twine upload --skip-existing ./dist/spotify-onthego-*.tar.gz

###### Testing

test: test-lint test-format ## Run all tests

test-format: ## Run formatting tests
	black --check --diff ./onthego
	
test-lint: ## Run lint tests
	pylint --rcfile=./.pylintrc ./onthego

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
