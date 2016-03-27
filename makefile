##################################
# Variables                      #
##################################
SHELL = /bin/sh

CC = pyinstaller
C_FLAGS = --onefile

TARGET = styrobotpy 
FILES = styrobot.py
#################################

all: copy

build: $(TARGET)

run: copy
	python ./dist/styrobot.py

copy:
	cp -r "./deps/" "./dist/" 
	cp "./styrobot/$(FILES)" "./dist/$(FILES)"

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

$(TARGET): ./styrobot/$(FILES) 
	$(CC) $(C_FLAGS) ./styrobot/$(FILES) -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

clean:
	rm -rf ./build/ ./dist/ 
