FIND=find
PACKAGE=prospector-holds
PIP=pip
PYTHON=python3
XARGS=xargs

.PHONY: help
help:  ## This.
	@perl -ne 'print if /^[a-zA-Z_.-]+:.*## .*$$/' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test:  ## Run the test driver
	$(PACKAGE)

.PHONY: tests
tests:  ## Run the test suite
	$(PYTHON) -m unittest

.PHONY: clean
clean:  ## Clean up temporary build files
	$(FIND) . -type d -name '__pycache__' -print0 \
	| $(XARGS) -0 --no-run-if-empty \
		rm -rf \
	;

.PHONY: requirements.txt
requirements.txt:  ## Install the python requirements
	$(PIP) install -r '$(@)'

requirements.txt.lock: requirements.txt  ## Pin the current requirements
	$(PIP) freeze >'$(@)'
