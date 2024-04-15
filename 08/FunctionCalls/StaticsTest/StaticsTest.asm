// SP=256
@256
D=A
@SP
M=D
// call Sys.init 0
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
(Sys.RETURN_ADDRESS_4)
// function Class1.set 0
(Class1.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class1.0
M=D
// push ARG 1
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
AM=M-1
D=M
@Class1.1
M=D
// push constant 0
@0
D=A
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
// function Class1.get 0
(Class1.get)
// repeat 0 times: PUSH 0
// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.1
D=M
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
// function Class2.set 0
(Class2.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class2.0
M=D
// push ARG 1
@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
AM=M-1
D=M
@Class2.1
M=D
// push constant 0
@0
D=A
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
// function Class2.get 0
(Class2.get)
// repeat 0 times: PUSH 0
// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.1
D=M
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
// push return_address
@Sys.RETURN_ADDRESS_0
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
@2
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
// goto function Class1.set
@Class1.set
0;JMP
// return-address
(Sys.RETURN_ADDRESS_0)
// pop R5 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
// push return_address
@Sys.RETURN_ADDRESS_1
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
@2
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
// goto function Class2.set
@Class2.set
0;JMP
// return-address
(Sys.RETURN_ADDRESS_1)
// pop R5 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// call Class1.get 0
// push return_address
@Sys.RETURN_ADDRESS_2
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
// goto function Class1.get
@Class1.get
0;JMP
// return-address
(Sys.RETURN_ADDRESS_2)
// call Class2.get 0
// push return_address
@Sys.RETURN_ADDRESS_3
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
// goto function Class2.get
@Class2.get
0;JMP
// return-address
(Sys.RETURN_ADDRESS_3)
(Sys.init$WHILE)
// goto Sys.init$WHILE
@Sys.init$WHILE
0;JMP
