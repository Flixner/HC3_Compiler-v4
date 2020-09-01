/**
 * Dieses Testprogramm testet stichprobenartig die Funktionen des Datentyps char
 * Erwartungen: Es Leuchten die roten LEDs immer nur einzeln auf. 
 * Ende des Tests: Es wird 0xF00 über die roten LEDs ausgegeben
 * Fehler eines Tests: Es wird 0xF über die roten LEDs ausgegeben
 **/

short main()
{    
    short z0;
    short erg;
    short i = 1;
    char c0;
    char c1;

while(i){

    /**
     * Test: Zu große Zuweisung
     * Erwartungen: erg != 0; && c0 == 0;
     */
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
    
    /**
     * Test: Numeischer überlauf && ++ Operator && Zuweisung einer Zahl
     * Erwartungen: 1. c0 != 0 -> nach Var++ -> c0 == 0
     */
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

    /**
     * Test: Var-- Operator
     * Erwartungen: 1. c0 != 0x0 -> 2. c0 == 0;
     */
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

    /**
     * Test: Richtiges Bitmuster
     * Erwartungen: 'A' == 0x41
     */
    c0 = 'A';
    erg = c0 - 0x41;
    if(erg == 0){
        SetLEDR(0x80);
    }else {
        SetLEDR(15);
    }
 
    /**
     * Test: Addition mit Buchstaben
     * Erwartungen: 'A' + 2 == 'C'
     */
    c0 += 2;
    c1 = 'C';
    erg = c0 - c1;
    if(erg == 0){
        SetLEDR(0x100);
    }else {
        SetLEDR(15);
    }
 
    /**
     * Test: Subtraktion mit Buchstaben
     * Erwartungen: 'C' - ('A' + 2) == 0
     */
    c0 -= ('A' + 2);
    if(c0 == 0){
        SetLEDR(0x200);
    }else {
        SetLEDR(15);
    }

    /**
     * Test: Division mit Zahl
     * Erwartungen: 'F' / 2 == 35
     */
    c0 = 'F'; // == 70 dezimal
    c0 /= 2;
    erg = c0 - 35;
    if(erg == 0){
        SetLEDR(0x400);
    }else {
        SetLEDR(15);
    }

    /**
     * Test: Multiplikation mit Zahl
     * Erwartungen: 'F' / 2 == 35
     */

    c0 *= 2;
    erg = 'F' - c0;
    if(erg == 0){
        SetLEDR(0x800);
    }else {
        SetLEDR(15);
    }
    
    SetLEDR(0xF00);// Ende der Tests
} 


    return 0;
} 