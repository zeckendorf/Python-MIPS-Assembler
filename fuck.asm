.org 1001
VYTE_LOC: .byte 4AH , 5CH ,    DFH, 10, 1010B
JESSE_SUX: add $s1,$s2,$s1
           addi $s1, $s2, -100 #hey!!!!
           j EXIT
     EXIT: j JESSE_SUX
