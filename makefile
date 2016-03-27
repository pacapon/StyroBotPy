##################################
# Variables                      #
##################################
SHELL = /bin/sh

CC = pyinstaller
C_FLAGS = --onefile -p 

TARGET = styrobotpy 
#################################

all:build copy

build: $(TARGET)

run: copy
	cd ./dist/ && make run

copy:
	cp -r "./deps/." "./dist/" 
	cp -r "./styrobot/plugins/" "./dist/plugins/"

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

$(TARGET): 
	$(CC) $(C_FLAGS) ./styrobot/ ./styrobot/styrobot.py -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

clean:
	rm -rf ./build/ ./dist/ ./styrobotpy.spec 
