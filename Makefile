.PHONY: install clean venv help run_example_svm UI docker vite api stop_UI stop_docker stop_vite stop_api

## Variables
VENV_DIR := .venv
VENV_BIN := $(VENV_DIR)/bin
LOGS_DIR := artifacts/logs

## Create the python virtual environment
venv:
	python3 -m venv $(VENV_DIR)

## Install the package and dependencies
install: venv
	$(VENV_BIN)/pip install -e .
	$(VENV_BIN)/pip install -r requirements.txt

## Execute the train_svm.py file
run_example_svm: install
	$(VENV_BIN)/snapper-ml --config_file=examples/experiments/svm.yaml

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(VENV_DIR)


## Start the UI (starts docker, vite, api in the background)
UI: expect
	@$(MAKE) BACKGROUND=1 docker
	@$(MAKE) BACKGROUND=1 vite
	@$(MAKE) BACKGROUND=1 api
	@echo -e '\n\033[1;32mUI started on http://localhost:4000/\033[0m'

## Stop the UI services
stop_UI: stop_docker stop_vite stop_api
	@echo "UI stopped."

## Start Docker containers
docker:
	@if ! docker info > /dev/null 2>&1; then \
		echo "Docker is not active. Attempting to start it..."; \
		sudo systemctl start docker || (echo "Failed to start Docker. Please start it manually." && exit 1); \
	fi
	@if [ "$(BACKGROUND)" = "1" ]; then \
		(cd docker && docker compose up -d); \
	else \
		(cd docker && docker compose up); \
	fi

## Stop Docker containers
stop_docker:
	@(cd docker && docker compose down)

## Start Vite development server
vite:
	@(cd snapper_ml/UI && npm install)
	@if [ "$(BACKGROUND)" = "1" ]; then \
		mkdir -p $(LOGS_DIR); \
		cd snapper_ml/UI && \
		bash -c 'set +H; nohup npx vite --port=4000 > ../../$(LOGS_DIR)/vite.log 2>&1 & echo $$! > ../../vite.pid' & \
	else \
		cd snapper_ml/UI && npx vite --port=4000; \
	fi

## Stop Vite development server
stop_vite:
	@if [ -f vite.pid ]; then \
		kill $$(cat vite.pid) && rm vite.pid; \
		echo "Vite server stopped."; \
	else \
		echo "vite.pid not found. Vite may not be running or was not started via Makefile."; \
	fi

## Start the API
api: install
	@if [ "$(BACKGROUND)" = "1" ]; then \
		mkdir -p $(LOGS_DIR); \
		bash -c 'set +H; nohup $(VENV_BIN)/python api.py > $(LOGS_DIR)/api.log 2>&1 & echo $$! > api.pid' & \
	else \
		$(VENV_BIN)/python api.py; \
	fi

## Stop the API
stop_api:
	@if [ -f api.pid ]; then \
		kill $$(cat api.pid) && rm api.pid; \
		echo "API stopped."; \
	else \
		echo "api.pid not found. API may not be running or was not started via Makefile."; \
	fi

## Check if "expect" is installed and try to install it
expect:
	@if ! command -v expect > /dev/null 2>&1; then \
		echo "'expect' is not installed. Attempting to install it..."; \
		if command -v apt-get > /dev/null 2>&1; then \
			sudo apt-get update && sudo apt-get install -y expect; \
		elif command -v yum > /dev/null 2>&1; then \
			sudo yum install -y expect; \
		elif command -v brew > /dev/null 2>&1; then \
			brew install expect; \
		elif command -v pacman > /dev/null 2>&1; then \
			sudo pacman -S expect; \
		else \
			echo "Package manager not found. Please install 'expect' manually."; \
			exit 1; \
		fi; \
	else \
		echo "'expect' is already installed."; \
	fi

## Show available make commands
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
