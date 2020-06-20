#line 1 "testfiles/test_compilerSimple.c"
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
