#instructionsize 16
main: 
	LUI r22 0xFFDF ;		initialise STACK
	LLI r22 0xFFDF ;		
	MOV r1 r22 ;		
	SUBI r1 3 ;		    reserve space for local variables on stack
	LOAD r10 r8 ;		get SW
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		a in Compound 1
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		a in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r7 ;		set LEDR
	LUI f0 19008 ;		     load Constant
	LLI f0 19008 ;		     load Constant
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		b in Compound 1
	MOV f0 r10 ;		force cast by Hardware
	STORE f0 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		b in Compound 1
	LOAD f0 r15 ;		and load
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 3 ;		c in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	JL r0 r0 ;		return
	JL r0 r0 ;		return
