/**
 * forschleife mit überlauf
 * alle Ergebnisse auf das Display ausgeben
 * Operatoren: ++ -- + - * / 
 **/
char test(char a){
    char offset = 3;
    char erg;
    erg = a + offset;
    return erg;
}
short main()
{
    char a, b;
    char d;
    a = test('a');
    b = 'A';

    d = a++ * --b;
    
    return 0;
}