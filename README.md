# HC3 -- C-Compiler
## Basic Data Types + Operations
- `short`
    - arithmetic operations
        - `+` addition 
        - `-` subtraction 
        - `*` multiplication 
        - `/` division 
        - `%` modulo 
    - assignments
        - `=` assignment 
        - `++` increment 
        - `--` decrement 
        - combined `+=, -=, ...` 
    - comparisons
        - `==` equals
        - `!=` not equals
        - `>` greater than
        - `<` less than
        - `>=` greater or equal than
        - `<=` less or equal than
    - propositional logic
        - `!` not
        - `&&` and
        - `||` or
    - bit manipulation
        - `&` bitwise AND
        - `|` bitwise OR
        - `^` bitwise XOR
        - `~` bitwise NOT
        - `<<` shift bitwise left
        - `>>` shift bitwise right
    - other
        - `?` conditional operator
- `float`
    - arithmetic operations
        - `+` addition 
        - `-` subtraction 
        - `*` multiplication 
        - `/` division 

## Keywords
- data types
    - `void`
    - `short`
    - `float`
- conditional execution
    - `if, else if, else` 
    - `switch case`
- loops
    - `for`
    - `while` 
    - `do while`  
- jumps
    - `return`
    - `break`   

## Supported C-Elements
- function calls
- function definitions
- global variables
- constants
- code blocks `{ ... }`     

## Build-In Functions
There is no need for an include directive to use the following functions.
- `short GetSW();` returns value of switches SW15 ... SW0
- `short GetKEY0();` returns value of button KEY0
- `short GetKEY1();` returns value of button KEY1
- `void SetLEDR(short value);` sets LEDR(15 ... 0) to value 
- `void SetHEX0(short value);` sets HEX0 to value (without conversion)
- `void SetHEX1(short value);` sets HEX1 to value (without conversion)
- `void SetHEX2(short value);` sets HEX2 to value (without conversion)
- `void SetHEX3(short value);` sets HEX3 to value (without conversion)
- `void SetHEX4(short value);` sets HEX4 to value (without conversion)
- `void SetHEX5(short value);` sets HEX5 to value (without conversion)
- `void SetHEX6(short value);` sets HEX6 to value (without conversion)
- `void SetHEX7(short value);` sets HEX7 to value (without conversion)

## Basic main function
    short main()
    {
        short a = GetLEDR();
        SetLEDR(a);
        
        float b = 12.5;
        short c = b; // automatic typecast -> c = 12
        return 0;
    }

## using the compiler
python3 main.py optimization_level input_file
input_file: must have .c ending
optimization_level: fake, not used
The output file is determined by changing the input_file ending to .asm
Example:
    python3 main.py 0 main.c

## Dependencies
   - [Python C-Parser](https://github.com/eliben/pycparser)
   - [Numpy](https://numpy.org/)

## Changelog
- 09.01.2020 [Sebastian Bräske, Manuel Bloedow, Matthias Rosenthal]
    - fixed bug with new pycparser which cased compilation fail 
    - fixed bug when requesting value of key0 or key1
    - added support of new HC 3 float <-> short conversion
    - added possibility for loading float numbers via `LUI + LLI`
    - refactored code


(c) Technische Hochschule Mittelhessen   
