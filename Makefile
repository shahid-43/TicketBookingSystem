PYTHON = python3

SOURCE = main.py
EXECUTABLE = ./dist/main
# default target
all:
	@echo "main is ready to run"
	@echo "Use 'make run input=input_file.txt' to execute the program without executable file"
	@echo "Use 'make run_executable input=input_file.txt' to execute the program with executable file"


.PHONY: build
build:
	@echo "building env and downloading required packages"
	python3 -m venv env && source env/bin/activate && pip install -r requirement.txt && pyinstaller --onefile  $(SOURCE)
	

run_executable: build
	@echo "running executable file"
	$(EXECUTABLE) $(input)
	

#  run with the input file with standard command
run:  
	$(PYTHON) $(SOURCE) $(input) 

# to clean files
clean:
	@echo "removing generated files"
	rm -f *_output.txt
	rm -f _pycache_/*
	rm -rf _pycache_
	rm -rf build
	rm -rf dist
	rm -f main.spec
	rm -rf env


help:
	@echo "Available targets:"
	@echo "  make        - Prepare the program for execution"
	@echo "  make run    - Run the program (use: make run input=input_filename.txt)"
	@echo "  make run_executable   - builds the program and creates an executable file and runs that (use: make run_executable input=input_filename.txt)"
	@echo "  make clean  - Remove generated files"
	@echo "  make help   - Show this help message"
	@echo "  make build   - builds the env and required packages for executable file creation"

.PHONY: all run clean help