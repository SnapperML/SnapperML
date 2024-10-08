.PHONY: install clean

install: activate
	(source .venv/bin/activate && pip install -e .)

activate:
	make clean
	(python3 -m venv .venv && source .venv/bin/activate)

run: clean install
	(source .venv/bin/activate && cd examples && snapper-ml --config_file=experiments/svm.yaml)

clean:
	rm -rf .venv
