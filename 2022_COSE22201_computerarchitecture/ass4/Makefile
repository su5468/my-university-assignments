#
#  Makefile to generate RISC-V binary for Computer Architecture class
#
#  Author: Prof. Taeweon Suh
#          Computer Science & Engineering
#	   College of Informatics
#          Korea University
#
#  Date:   2020-06-11
#

    HOME=/home/jgh/rv32imac
    MIPSBIN=$(HOME)/bin
    AS=$(MIPSBIN)/riscv32-unknown-elf-as
    LD=$(MIPSBIN)/riscv32-unknown-elf-ld
	CC=$(MIPSBIN)/riscv32-unknown-elf-gcc
	CPP=$(MIPSBIN)/riscv32-unknown-elf-cpp        
    OBJDUMP=$(MIPSBIN)/riscv32-unknown-elf-objdump
    OBJCOPY=$(MIPSBIN)/riscv32-unknown-elf-objcopy
#   ASFLAGS= -Wall -O2 -g
#    ASFLAGS= -g -mips32
    ASFLAGS= -g -march=rv32i
    LDFLAGS= -N -X -Tlabcode.lds
    CCFLAGS= -c -g -march=rv32i
    
    all: labcode 

    labcode: ass3_2018130508.o lab0.o SevenSeg.o
	$(LD) $(LDFLAGS) ass3_2018130508.o lab0.o SevenSeg.o -o labcode
	$(OBJDUMP) -xS  labcode > labcode.dump
	$(OBJDUMP) -xS ass3_2018130508.o > ass3_2018130508.odump
	$(OBJDUMP) -xS lab0.o > lab0.odump
	$(OBJDUMP) -xS SevenSeg.o > SevenSeg.odump 
	$(OBJCOPY) -O  binary labcode labcode.bin
	./bin2hex.perl > labcode.hex
	./hex2mif.perl 
#	./mipsel-readelf -a labcode > labcode.r
#	./mipsel-nm labcode > labcode.n
	cp -f insts_data.mif ../milestone/RV32I_Class_Project/RV32I_System_Syn
	cd ../milestone/RV32I_Class_Project/RV32I_System_Syn && ./quartus_mem_update_download.bat
	 
    lab0.o: lab0.s
	$(AS) $(ASFLAGS) lab0.s -o lab0.o
	
    SevenSeg.o:	SevenSeg.c
	$(CPP) SevenSeg.c > SevenSeg.i
	$(CC) -Wall -S SevenSeg.i
	$(AS) $(ASFLAGS) SevenSeg.s -o Sevenseg.o
	$(CC) $(CCFLAGS) SevenSeg.c

    ass3_2018130508.o: ass3_2018130508.s
	$(AS) $(ASFLAGS) ass3_2018130508.s -o ass3_2018130508.o
	
    clean:
	rm -rf SevenSeg.i SevenSeg.s *.o *.mif *.dump *.odump *.hex *.bin *.mif labcode
