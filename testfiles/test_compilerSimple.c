short main()
{    
    short z0;
    short erg;
    short i = 1;
    char c0;
    char c1;

while(i){

    //Überlauf Checken Erwartung: 0x100 = 0x00 
    z0 = 0x100;
    c0 = 0x100;
    erg = z0 - c0;
    if(erg){
        SetLEDR(1);
    }else {
        SetLEDR(15);// Fehlercode
    }
    if(c0 == 0){
        SetLEDR(2);
    }else {
        SetLEDR(15);
    }
    
    //Überlauf Checken Erwartung: 0xFF + 1 = 0x00
    c0 = 0xFF;
    if(c0){
        SetLEDR(4);
    }else {
        SetLEDR(15);
    }
    c0++;
    if(c0 == 0){
        SetLEDR(8);
    }else {
        SetLEDR(15);
    }

    //Richtiges Bitmuster Checken Erwartung 'A' == 0x41
    c0 = 'A';
    erg = c0 - 0x41;
    if(erg == 0){
        SetLEDR(16);
    }else {
        SetLEDR(15);
    }

    //Addition mit Buchstaben Checken Erwartung 'A' + 2 == 'C'
    c0 += 2;
    c1 = 'C';
    erg = c0 - c1;
    if(erg == 0){
        SetLEDR(32);
    }else {
        SetLEDR(15);
    }

    //Subtraktion mit Buchstaben Checken Erwartung: 'C' - ('A' + 2) == 0
    c0 -= ('A' + 2);
    if(c0 == 0){
        SetLEDR(32);
    }else {
        SetLEDR(15);
    }
    
    SetLEDR(0xF00);// Ende der Tests
} 


    return 0;
} 