.data
	VAR_global:	.space	0
	VAR_ackermann_p:	.word	0
	VAR_ackermann_t:	.word	0
	VAR_main_x:	.word	0
	VAR_main_y:	.word	0
	newLine:	.asciiz	"\n"
.text
ackermann:
	add	$t0,	$zero,	$a1
	add	$t1,	$zero,	$a2
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	li	$t2,	-1
	mul	$t3,	$t2,	1
	lw	$t2,	VAR_ackermann_t
	move	$t2,	$t3
	beq	$a1,	0,	L_1
	li	$t3,	0
	b	L_2
L_1:
	li	$t3,	1
L_2:
	beq	$t3,	0,	L_7
	add	$t3,	$a2,	1
	move	$t2,	$t3
	b	L_8
L_7:
	beq	$a2,	0,	L_3
	li	$t3,	0
	b	L_4
L_3:
	li	$t3,	1
L_4:
	beq	$t3,	0,	L_5
	sub	$t3,	$a1,	1
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$t3
	addi	$a2,	$zero,	1
	jal	ackermann
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	add	$t4,	$zero,	$v1
	move	$t2,	$t4
	b	L_6
L_5:
	sub	$t4,	$a1,	1
	sub	$t5,	$a2,	1
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$a1
	add	$a2,	$zero,	$t5
	jal	ackermann
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	add	$t6,	$zero,	$v1
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t6,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$t4
	add	$a2,	$zero,	$t6
	jal	ackermann
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t6,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	add	$t7,	$zero,	$v1
	move	$t2,	$t7
L_6:
L_8:
	add	$v1,	$zero,	$t2
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
main:
	li	$v0,	5
	syscall
	lw	$t0,	VAR_main_x
	move	$t0,	$v0
	li	$v0,	5
	syscall
	lw	$t1,	VAR_main_y
	move	$t1,	$v0
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	add	$a1,	$zero,	$t0
	add	$a2,	$zero,	$t1
	jal	ackermann
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	add	$t2,	$zero,	$v1
	li	$v0,	1
	move	$a0,	$t2
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	li	$v0,	10
	syscall
