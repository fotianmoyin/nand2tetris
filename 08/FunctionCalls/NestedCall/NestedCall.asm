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
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// call Sys.main 0
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
// goto function Sys.main
@Sys.main
0;JMP
// return-address
(Sys.RETURN_ADDRESS_0)
// pop R5 1
@R5
D=A
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(Sys.init$LOOP)
// goto Sys.init$LOOP
@Sys.init$LOOP
0;JMP
// function Sys.main 5
(Sys.main)
// repeat 5 times: PUSH 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop LCL 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop LCL 2
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop LCL 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
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
// goto function Sys.add12
@Sys.add12
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
// push LCL 0
@LCL
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
// push LCL 1
@LCL
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
// push LCL 2
@LCL
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
// push LCL 3
@LCL
D=M
@3
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push LCL 4
@LCL
D=M
@4
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
// function Sys.add12 0
(Sys.add12)
// repeat 0 times: PUSH 0
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
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
// push constant 12
@12
D=A
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
