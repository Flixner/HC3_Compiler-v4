#line 8 "testfiles/test_compilerSimple.c"
short main()
{
    short z0;
    short erg;
    short i = 1;
    char c0;
    char c1;

while(i){





    z0 = 0x100;
    c0 = 0x100;
    erg = z0 - c0;
    if(erg){
        SetLEDR(1);
    }else {
        SetLEDR(15);
    }
    if(c0 == 0){
        SetLEDR(2);
    }else {
        SetLEDR(15);
    }





    c0 = 0xFF;
    if(c0++){
        SetLEDR(4);
    }else {
        SetLEDR(15);
    }
    if(c0 == 0){
        SetLEDR(8);
    }else {
        SetLEDR(15);
    }





    c0 = 0x1;
    if(c0--){
        SetLEDR(16);
    }else {
        SetLEDR(15);
    }
    if(c0 == 0){
        SetLEDR(32);
    }else {
        SetLEDR(15);
    }
#line 142 "testfiles/test_compilerSimple.c"
    SetLEDR(0xF00);
}


    return 0;
}
