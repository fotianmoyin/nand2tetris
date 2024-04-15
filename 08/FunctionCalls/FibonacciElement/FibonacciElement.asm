// SP=256
@256
D=A
@SP
M=D
// call Sys.init 0
// push return_address
@Sys.RETURN_ADDRESS_5
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG=SP-n-5
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
// goto function Sys.init
@Sys.init
0;JMP
// return-address
(Sys.RETURN_ADDRESS_5)
// function Main.fibonacci 0
(Main.fibonacci)
// repeat 0 times: PUSH 0
// push ARG 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@SP
M=M-1
A=M
D=M-D
@Main.LT_0
D;JLT
D=0
@Main.NEXT_1
0;JMP
(Main.LT_0)
D=-1
(Main.NEXT_1)
@SP
A=M
M=D
@SP
M=M+1
// if-goto Main.fibonacci$IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// goto Main.fibonacci$IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
(Main.fibonacci$IF_TRUE)
// push ARG 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// return
// FRAME = LCL
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@5
A=D-A
D=M
@R14
M=D
// *ARG=pop()
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// SP = ARG+1
@ARG
D=M+1
@SP
M=D
// THAT
@R13
D=M-1
AM=D
D=M
@THAT
M=D
// THIS
@R13
D=M-1
AM=D
D=M
@THIS
M=D
// ARG
@R13
D=M-1
AM=D
D=M
@ARG
M=D
// LCL
@R13
D=M-1
AM=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
(Main.fibonacci$IF_FALSE)
// push ARG 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// call Main.fibonacci 1
// push return_address
@Main.RETURN_ADDRESS_2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG=SP-n-5
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
// goto function Main.fibonacci
@Main.fibonacci
0;JMP
// return-address
(Main.RETURN_ADDRESS_2)
// push ARG 0
@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// call Main.fibonacci 1
// push return_address
@Main.RETURN_ADDRESS_3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG=SP-n-5
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
// goto function Main.fibonacci
@Main.fibonacci
0;JMP
// return-address
(Main.RETURN_ADDRESS_3)
// add
@SP
AM=M-1
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
// return
// FRAME = LCL
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@5
A=D-A
D=M
@R14
M=D
// *ARG=pop()
@SP
AM=M-1
D=M
@ARG
A=M
M=D
// SP = ARG+1
@ARG
D=M+1
@SP
M=D
// THAT
@R13
D=M-1
AM=D
D=M
@THAT
M=D
// THIS
@R13
D=M-1
AM=D
D=M
@THIS
M=D
// ARG
@R13
D=M-1
AM=D
D=M
@ARG
M=D
// LCL
@R13
D=M-1
AM=D
D=M
@LCL
M=D
// goto RET
@R14
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// repeat 0 times: PUSH 0
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1
// push return_address
@Sys.RETURN_ADDRESS_4
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG=SP-n-5
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
// LCL=SP
@SP
D=M
@LCL
M=D
// goto function Main.fibonacci
@Main.fibonacci
0;JMP
// return-address
(Sys.RETURN_ADDRESS_4)
(Sys.init$WHILE)
// goto Sys.init$WHILE
@Sys.init$WHILE
0;JMP
