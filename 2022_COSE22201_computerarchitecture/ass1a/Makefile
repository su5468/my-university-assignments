CC=gcc
    
all: compare

compare: compare.o
	objdump -SD -Mintel compare.o > compare.odump
#	make .dump file since object file is binary
#	can't link since .c file doesn't have main() func
#	in this case x86 compiler cannot make executable file

compare.o: compare.s
	as compare.s -o compare.o

compare.s: compare.i
	$(CC) -S compare.i

compare.i: compare.c
	cpp compare.c > compare.i

clean:
	rm -rf *.i *.s *.o *.mif *.dump *.odump *.hex *.bin *.mif labcode
