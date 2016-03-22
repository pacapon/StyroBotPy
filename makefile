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

copy:
	cp -R "./deps/" "./dist/" 
	cp "./credentials.txt" "./dist/credentials.txt" # This is just how i keep my credentials outside of the repo

$(TARGET): $(FILES) 
	$(CC) $(C_FLAGS) $(FILES) -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

clean:
	rm -rf ./build/ ./dist/ ./StyroBotPy.spec
