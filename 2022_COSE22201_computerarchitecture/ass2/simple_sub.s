#
#  Author: Prof. Taeweon Suh
#          Computer Science & Engineering
#          Korea University
#  Date:   June 13, 2020
#  Description: Simple addition of 4 words (result = op1 + op2)
#

.globl __start

.text
.align 4

__start:

        la   t0, op1          # load address; load op1 label to t0 register (t0 is address)
	la   t1, op2          # load address; load op2 label to t1 register (t1 is address)
	la   t2, result       # load address; load result label to t2 register (t2 is address)
	sub t3, t1, t0        # subtract;     t3 = t1 - t0 (distance between addresses)
	srai  t3, t3, 2       # how many words? shift right by 2; t3 /= 4 since 1w = 4B

myloop:
	lw   s0, 0(t0)        # load word;    load t0 address(=op1) to s0
	lw   s1, 0(t1)        # load word;    load t1 address(=op2) to s1
	sub  s2, s1, s0       # add;          s2 = s1 + s0
	sw   s2, 0(t2)        # store word;   store s2 to t2 address(=result)
	addi t3, t3, -1       # decrement by 1; t3 -= 1
	beq  t3, zero, myself # branch equal; if t3==0 goto myself     
	addi t0, t0, 4        # add imm;      t0 += 4
	addi t1, t1, 4        # add imm;      t1 += 4
	addi t2, t2, 4        # add imm;      t2 += 4
	j    myloop           # jump;         goto myloop

myself:
        li   t0, 0x12345678   # just an example pseudo code
        nop	              # just an example pseudo code
        mv   t1, t0           # just an example pseudo code
        j myself
        

.data
.align 4
op1:    .word  1, 2, 3, 4 
op2:    .word  5, 6, 7, 8
result: .word  0, 0, 0, 0 
