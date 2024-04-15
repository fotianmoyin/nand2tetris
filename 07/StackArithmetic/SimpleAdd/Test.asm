//RAM[0]=5
//RAM[5]=1
@5
D=A
@SP
M=D
A=M
M=1

//RAM[2]=2
@2
D=A
@ARG
M=D

//RAM[10]=4
@ARG
D=M
@2
D=D+A
@R10
M=D

@SP
A=M
D=M

@R10
A=M
M=D