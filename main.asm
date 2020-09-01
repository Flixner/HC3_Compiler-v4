#instructionsize 16
test: 
	STORE r2 r1 ;		function entry-point
	SUBI r1 1 ;		together with above: save(push) FUNC on stack
	STORE r3 r1 ;		push LINK on stack (just in case)
	SUBI r1 1 ;		...
	MOV r2 r1 ;		set Function Basepointer = STACK on calltime
	SUBI r1 1 ;		    reserve space for local variables on stack
	LUI r22 0 ;		    load Constant
	LLI r22 97 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	MOV r1 r2 ;		mark local variables as undeclared (just move STACK back)
	ADDI r1 1 ;		pop LINK back from stack
	LOAD r3 r1 ;		...
	ADDI r1 1 ;		pop FUNC back from stack
	LOAD r2 r1 ;		...
	JL r0 r3 ;		return
	MOV r1 r2 ;		mark local variables as undeclared (just move STACK back)
	ADDI r1 1 ;		pop LINK back from stack
	LOAD r3 r1 ;		...
	ADDI r1 1 ;		pop FUNC back from stack
	LOAD r2 r1 ;		...
	JL r0 r3 ;		return
main: 
	LUI r22 0xFFDF ;		initialise STACK
	LLI r22 0xFFDF ;		
	MOV r1 r22 ;		
	SUBI r1 2 ;		    reserve space for local variables on stack
	LUI r22 0 ;		    load Constant
	LLI r22 65 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 1 ;		    load Constant
	LLI r22 1 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		s in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 49 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 50 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 51 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 52 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 53 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 54 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 55 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 56 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 62 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	ADDI r8 4 ;		    GOTO Keyboard
	STORE r0 r8 ;		
main_c_61_10_begin: 
	LOAD r10 r8 ;		prepare Keyboard
	BPOS r10 main_c_61_10_end ;		if new char is avalible -> exit loop
	LUI r22 main_c_61_10_begin ;		jump back to loop head
	LLI r22 main_c_61_10_begin ;		
	JL r0 r22 ;		just jump
main_c_61_10_end: 
	STORE r10 r8 ;		Schreibe wieder in den Speicher (prepare ende)
	SUBI r8 4 ;		    GOTO SW
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	LOAD r10 r15 ;		and load
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	ADDI r8 4 ;		    GOTO Keyboard
	STORE r0 r8 ;		
main_c_63_10_begin: 
	LOAD r10 r8 ;		prepare Keyboard
	BPOS r10 main_c_63_10_end ;		if new char is avalible -> exit loop
	LUI r22 main_c_63_10_begin ;		jump back to loop head
	LLI r22 main_c_63_10_begin ;		
	JL r0 r22 ;		just jump
main_c_63_10_end: 
	STORE r10 r8 ;		Schreibe wieder in den Speicher (prepare ende)
	SUBI r8 4 ;		    GOTO SW
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	LOAD r10 r15 ;		and load
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	ADDI r8 4 ;		    GOTO Keyboard
	STORE r0 r8 ;		
main_c_65_10_begin: 
	LOAD r10 r8 ;		prepare Keyboard
	BPOS r10 main_c_65_10_end ;		if new char is avalible -> exit loop
	LUI r22 main_c_65_10_begin ;		jump back to loop head
	LLI r22 main_c_65_10_begin ;		
	JL r0 r22 ;		just jump
main_c_65_10_end: 
	STORE r10 r8 ;		Schreibe wieder in den Speicher (prepare ende)
	SUBI r8 4 ;		    GOTO SW
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		ch in Compound 1
	LOAD r10 r15 ;		and load
	ADDI r7 12 ;		    GOTO VGA
	STORE r10 r7 ;		set new Char to screen
	SUBI r7 12 ;		    GOTO LEDR
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	JL r0 r0 ;		return
	JL r0 r0 ;		return
