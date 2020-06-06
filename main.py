#!/bin/env python

import sys
from io import StringIO
# C to AST parser import
from pycparser import c_parser

from AssemblyGenerator import *

# Präprozessor import 
import PreProcessor

def main():
    
    #Nur für testzwecke auskommentiert 
    """ if len(sys.argv) == 3:
        optimisation_level = sys.argv[1]
        input_file_path = sys.argv[2]
    else:
        print('ERROR: invalid number of arguments - use main.py <optimization level> <input file>\n')
        return
 """
    #Nur für Testzwecke
    #--------------------------------------------------
    optimisation_level = 0
    input_file_path = "testfiles/test_compilerSimple.c"
    #--------------------------------------------------

    
    if not input_file_path.endswith('.c'):
        print('ERROR: invalid Filetype - only .c allowed\n')
        return

    #Hier wird der Präprozessor aufgerufen
    #Es wird eine neue Datei erstellt die für den Compiler kompatibel ist
    #Der Inhalt dieser neuen Datei ist der Rückgabetyp von der Funktion preProcess
    text = PreProcessor.preProcess(input_file_path)

    # Filter Comments
    while text.find("//") > 0 or text.find("/*") > 0 or text.find("*/") > 0:
        if text.find("//") > 0:
            comment_start = text.find('//')
            comment_end = text.find('\n', comment_start)
            text = text[:comment_start] + text[comment_end:]
        elif text.find("/*") > 0:
            comment_start = text.find('/*')
            comment_end = text.find('*/', comment_start)
            if comment_end > comment_start:
                text = text[:comment_start] + text[comment_end + 2:]
            else:
                print('Not Closed Comment with /* \n')
                return
        elif text.find("*/") > 0:
            print('Cannot close Comment with */ before opening it \n')
            return
            
    print('creating Syntax Tree/Parsing')
    parser = c_parser.CParser()
    try:
        ast = parser.parse(text, filename=input_file_path)
    except Exception as ex:
        print("ERROR during Parsing: " + str(ex))
        return

    print('Generating Assembly')
    try:
        asm_gen = AssemblyGenerator()
        asm_gen.WorkFromAST(ast)
    except Exception as ex:
        tex = str(ex)
        try:
            # Show Location in Commandline + Error
            # BSP.
            # main.c:8:2: ERROR: Massage
            line = int(tex[tex.find(':', 3) + 1:tex.find(':', tex.find(':', 3) + 1)])
            pos = int(
                tex[tex.find(':', tex.find(':', 3) + 1) + 1:tex.find(':', tex.find(':', tex.find(':', 3) + 1) + 1)])
            print(tex)
            print(text.splitlines()[line - 1])
            print(' ' * pos + '  ' + '^')
        except Exception as err:
            # Only Error Massage
            print(tex)
            print(err)
        return

    print('Converting Assembly to text')
    assembly_text = asm_gen.GetInTextform()

    print('Outputting Assembly text to file')
    output_file_name = input_file_path[:-2] + '.asm'
    try:
        output_file = open(output_file_name, 'w')
        output_file.write(assembly_text)
        output_file.close()
    except Exception as err:
        print('ERROR: can not save file ' + output_file_name)
        print(err)
        return

    print('done - exiting')


if __name__ == "__main__":
    main()
