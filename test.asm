.org 1000
.byte 12H, 30, 22H, 10011101B
Loop: add $s1, $s2, $s3
addi $s1, $s2, 100
sub $s1, $s2, $s3
lw $s1, 100($s2)
lui $s1, 100
sw $s1, 100($s2)
slt $s1, $s2, $s3
beq $s1, $s2, Loop
Test: move $t1, $t2
clear $t0
ble $t3, $t5, LT
bgt $t4, $t5, GT
bge $t5, $t3, EQ
bne $s1, $s2, Exit
beq $t1, 16, Test
beq $t2, 100000, Loop
GT: li $t1, 16
j Exit
LT: li $t2, 100000
jr $ra
EQ: addi $t0, $t2, 100000
lw $t5, 100000($t2)
jal 10000
Exit: .end
