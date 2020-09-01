#line 1 "main.c"
char test(short s){
    return 'a';
}

short main(){

    char ch = 'A';
    short s = 1;
#line 50 "main.c"
    putChar('1');
    putChar('2');
    putChar('3');
    putChar('4');
    putChar('5');
    putChar('6');
    putChar('7');
    putChar('8');
    putChar('>');


    ch = getChar();
    putChar(ch);
    ch = getChar();
    putChar(ch);
    ch = getChar();
    putChar(ch);
#line 78 "main.c"
    return 0;
}
