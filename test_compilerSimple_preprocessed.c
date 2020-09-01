#line 8 "test_compilerSimple.c"
short main()
{
    short z0;
    short erg;
    short i = 1;
    char c0;
    char c1;

while(i){
#line 72 "test_compilerSimple.c"
    c0 = 'A';
    erg = c0 - 0x41;
    if(erg == 0){
        SetLEDR(0x80);
    }else {
        SetLEDR(15);
    }





    c0 += 2;
    c1 = 'C';
    erg = c0 - c1;
    if(erg == 0){
        SetLEDR(0x100);
    }else {
        SetLEDR(15);
    }





    c0 -= ('A' + 2);
    if(c0 == 0){
        SetLEDR(0x200);
    }else {
        SetLEDR(15);
    }





    c0 = 'F';
    c0 /= 2;
    erg = c0 - 35;
    if(erg == 0){
        SetLEDR(0x400);
    }else {
        SetLEDR(15);
    }






    c0 *= 2;
    erg = 'F' - c0;
    if(erg == 0){
        SetLEDR(0x800);
    }else {
        SetLEDR(15);
    }

    SetLEDR(0xF00);
}


    return 0;
}
