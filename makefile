##################################
# Variables                      #
##################################
SHELL = /bin/sh

CC = pyinstaller
C_FLAGS = --onefile -p 

TARGET = styrobotpy 
#################################

all: build copy-dependencies copy-plugins

build: $(TARGET)

re-all: clean-all all

run:
	cd ./dist/ && ./styrobotpy 

runpy:
	cd ./dist/ && python styrobot.py

recopy: clean copy

copy: copy-dependencies copy-source
	
copy-dependencies:
	cp -r "./deps/." "./dist/" 

	@# This is just how i keep my credentials outside of the repo
	cp "./credentials.txt" "./dist/credentials.txt" 

copy-source:
	cp -r "./styrobot/." "./dist/"

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
