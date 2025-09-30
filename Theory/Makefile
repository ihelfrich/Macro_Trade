SHELL=/bin/bash

.PHONY: all env test sims empirics paper

env:
	@echo "Setting up environment..."
	pip install -q -r requirements.txt


test:
	@echo "Running tests..."
	python3 -m pytest

sims:
	@echo "Running simulations..."
	PYTHONPATH=. python3 sims/run_tri_node.py
	PYTHONPATH=. python3 sims/run_io.py
	PYTHONPATH=. python3 sims/run_granular.py
	PYTHONPATH=. python3 sims/run_nonhomothetic.py
	PYTHONPATH=. python3 sims/make_empirics.py --output-dir .
	PYTHONPATH=. python3 sims/run_sensitivity.py --output-dir .
	PYTHONPATH=. python3 sims/make_distributional.py --output-dir tables --fig-dir figs

empirics:
	@echo "Running empirical analysis..."
	# Add empirical analysis commands here

paper:
	@echo "Compiling paper..."
	cd paper && pdflatex main.tex && bibtex main.aux && pdflatex main.tex && pdflatex main.tex

all: test sims empirics
	-make paper
