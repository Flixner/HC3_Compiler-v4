short main()
{
    short a = GetSW();
    SetLEDR(a);
    
    float b = 12.5;
    short c = b; // automatic typecast, so now c = 12
    return 0;
}
