CC = g++

# Uncomment one of the following to switch between debug and opt mode
#OPT = -O3 -DNDEBUG
OPT = -g -ggdb

CFLAGS += -Wall -c -I. -I./include -I/usr/include/ -I./ $(OPT)

LDFLAGS+= -Wall -lpthread -lssl -lcrypto

LIBOBJECTS = \
	./hashutil.o \

HEADERS = $(wildcard src/*.h)

TEST = test

all: $(TEST)

clean:
	rm -f $(TEST) */*.o

test: test.o $(LIBOBJECTS) 
	$(CC) test.o $(LIBOBJECTS) $(LDFLAGS) -o $@

%.o: %.cc ${HEADERS} Makefile
	$(CC) $(CFLAGS) $< -o $@

