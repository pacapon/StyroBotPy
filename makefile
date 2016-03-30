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

re-all: clean-all all

run:
	cd ./dist/ && ./styrobotpy 

recopy: clean copy

copy:
	cp -r "./deps/." "./dist/" 
	cp -r "./styrobot/plugins/" "./dist/plugins/"

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

test:
	cp -r "./styrobot/" "./dist/"
	cp -r "./deps/." "./dist/" 
	cp "./credentials.txt" "./dist/credentials.txt" 

copy-plugins:
	cp -r "./styrobot/plugins/" "./dist/plugins/"

$(TARGET): 
	$(CC) $(C_FLAGS) ./styrobot/ ./styrobot/styrobot.py -n $(TARGET) 

install:
	sudo ./InstallDependencies.sh

reload: clean-plugins copy-plugins

clean-plugins:
	rm -rf ./dist/plugins/

clean:
	rm -rf ./dist/

clean-all: clean
	rm -rf ./build/ ./styrobotpy.spec 
