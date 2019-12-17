.DEFAULT_GOAL := help

###### Development

compile-requirements: ## Compile *.txt requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in

format:
	black ./onthego


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
