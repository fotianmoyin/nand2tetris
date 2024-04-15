// SP=256
@256
D=A
@SP
M=D
// call Sys.init 0
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
// goto function Sys.init
@Sys.init
0;JMP
// return-address
(Sys.RETURN_ADDRESS_2)
// function Sys.init 0
(Sys.init)
// repeat 0 times: PUSH 0
// push constant 1
@1
D=A
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
// push constant 3
@3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 5
@5
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 7
@7
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
// push constant 9
@9
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add 3
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
@3
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
// goto function Sys.add
@Sys.add
0;JMP
// return-address
(Sys.RETURN_ADDRESS_0)
// call Sys.add 3
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
@3
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
// goto function Sys.add
@Sys.add
0;JMP
// return-address
(Sys.RETURN_ADDRESS_1)
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
(Sys.init$WHILE)
// goto Sys.init$WHILE
@Sys.init$WHILE
0;JMP
// function Sys.add 0
(Sys.add)
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
// push ARG 2
@ARG
D=M
@2
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
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
