##################################
# Variables                      #
##################################
SHELL = /bin/sh

CC = pyinstaller
C_FLAGS = --onefile

TARGET = StyroBotPy
FILES = StyroBotPy.py
#################################

all: copy

build: $(TARGET)

run: copy
	python ./dist/StyroBotPy.py

copy:
	cp -r "./deps/" "./dist/" 
	cp "./src/$(FILES)" "./dist/$(FILES)"

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

$(TARGET): ./src/$(FILES) 
	$(CC) $(C_FLAGS) ./src/$(FILES) -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

clean:
	rm -rf ./build/ ./dist/ ./StyroBotPy.spec
