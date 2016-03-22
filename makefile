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

$(TARGET): $(FILES) 
	$(CC) $(C_FLAGS) $(FILES) -n $(TARGET) 
