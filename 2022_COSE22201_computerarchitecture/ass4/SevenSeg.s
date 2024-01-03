	.file	"SevenSeg.c"
	.option nopic
	.attribute arch, "rv32i2p0_m2p0_a2p0_c2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	1
	.globl	SevenSeg
	.type	SevenSeg, @function
SevenSeg:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	li	a5,-57344
	addi	a5,a5,12
	sw	a5,-36(s0)
	li	a5,-57344
	addi	a5,a5,16
	sw	a5,-40(s0)
	li	a5,128
	sw	a5,-20(s0)
	li	a5,-16
	sw	a5,-28(s0)
	li	a5,1
	sb	a5,-29(s0)
	sw	zero,-24(s0)
	j	.L2
.L4:
	lw	a5,-20(s0)
	lw	a4,0(a5)
	lw	a5,-28(s0)
	beq	a4,a5,.L3
	sb	zero,-29(s0)
.L3:
	lw	a5,-20(s0)
	addi	a5,a5,-4
	sw	a5,-20(s0)
	lw	a5,-28(s0)
	addi	a5,a5,1
	sw	a5,-28(s0)
	lw	a5,-24(s0)
	addi	a5,a5,1
	sw	a5,-24(s0)
.L2:
	lw	a4,-24(s0)
	li	a5,31
	ble	a4,a5,.L4
	lbu	a5,-29(s0)
	beq	a5,zero,.L5
	lw	a5,-36(s0)
	li	a4,121
	sw	a4,0(a5)
	j	.L6
.L5:
	lw	a5,-40(s0)
	li	a4,36
	sw	a4,0(a5)
.L6:
	j	.L6
	.size	SevenSeg, .-SevenSeg
	.ident	"GCC: (GNU) 10.1.0"
