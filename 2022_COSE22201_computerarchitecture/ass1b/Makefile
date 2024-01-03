HOME=/home/jgh/rv32imac
MIPSBIN=$(HOME)/bin
AS=$(MIPSBIN)/riscv32-unknown-elf-as
LD=$(MIPSBIN)/riscv32-unknown-elf-ld
CC=$(MIPSBIN)/riscv32-unknown-elf-gcc
CPP=$(MIPSBIN)/riscv32-unknown-elf-cpp
OBJDUMP=$(MIPSBIN)/riscv32-unknown-elf-objdump
OBJCOPY=$(MIPSBIN)/riscv32-unknown-elf-objcopy
ASFLAGS= -g -march=rv32i
LDFLAGS= -N -X -Tlabcode.lds
CCFLAGS= -c -g -march=rv32i

all: labcode

labcode: lab0.o compare.o
	$(LD) $(LDFLAGS)  lab0.o compare.o -o labcode
	$(OBJDUMP) -xS  labcode > labcode.dump
	$(OBJDUMP) -xS lab0.o > lab0.odump
	$(OBJDUMP) -xS compare.o > compare.odump
	$(OBJCOPY) -O  binary labcode labcode.bin
	./bin2hex.perl > labcode.hex
	./hex2mif.perl

lab0.o: lab0.s
	$(AS) $(ASFLAGS) lab0.s -o lab0.o
	
compare.o:	compare.c
	$(CPP) compare.c > compare.i
	$(CC) -Wall -S compare.i
	$(AS) $(ASFLAGS) compare.s -o compare.o
	$(CC) $(CCFLAGS) compare.c
	
clean:
	rm -rf *.i compare.s *.o *.mif *.dump *.odump *.hex *.bin *.mif labcode
