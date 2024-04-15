// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
//将最小清屏地址放到变量min中，将最大清屏地址放到变量max中，然后定义清屏地址的起始值是最小清屏地址。
//填充的过程就是逐渐增大清屏地址，直到清屏地址等于最大清屏地址。
//清屏的过程就是逐渐减小清屏地址，直到清屏地址等于最小清屏地址。
//在循环中，检测是否有按键动作。若有，跳转到填充代码块，进行填充操作；否则，进行清屏操作。
//这里最小清屏地址是：16384；最大清屏地址是：24575；按键地址是：24576。
//增大清屏地址意味着要填充，减小清屏地址就要清屏，为了消除边界问题，我们先对当前清屏地址进行清屏或填充动作，然后再判断是否到达边界。
//当前Hack计算机字长是16位，所以填充一个字长的十进制数为：-1
@SCREEN
D=A
//最小清屏地址
@min
M=D
//当前清屏地址
@i
M=D
//最大清屏地址
@24575
D=A
@max
M=D
(LOOP)
    //按键判断
    @KBD
    D=M
    @FILL
    D;JGT

    //***************清屏代码开始*************//
    //将当前清屏地址填充为白色
    @i
    A=M
    M=0
    //判断是否到达最小清屏地址边界
    @min
    D=M
    @i
    D=M-D
    @LOOP
    D;JEQ
    //减小当前清屏地址
    @i
    M=M-1
    @LOOP
    0;JMP
    //***************清屏代码结束*************//

    //***************填充代码开始*************//
    //将当前清屏地址填充为黑色
    (FILL)
        @i
        A=M
        M=-1
        //判断是否到达最大清屏地址边界
        @max
        D=M
        @i
        D=M-D
        @LOOP
        D;JEQ
        //增大当前清屏地址
        @i
        M=M+1
        @LOOP
        0;JMP
    //***************填充代码结束*************//
(END)
@END
0;JMP