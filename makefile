##################################
# Variables                      #
##################################
SHELL = /bin/sh

CC = pyinstaller
C_FLAGS = --onefile

TARGET = StyroBotPy
FILES = StyroBotPy.py
#################################

all: $(TARGET) copy

run: copy
	python ./dist/StyroBotPy.py

copy:
	cp -r "./deps/" "./dist/" 
	cp "./$(FILES)" "./dist/$(FILES)"

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

$(TARGET): $(FILES) 
	$(CC) $(C_FLAGS) $(FILES) -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

clean:
	rm -rf ./build/ ./dist/ ./StyroBotPy.spec
