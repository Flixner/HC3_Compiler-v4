#instructionsize 16
main: 
	LUI r22 0xFFDF ;		initialise STACK
	LLI r22 0xFFDF ;		
	MOV r1 r22 ;		
	SUBI r1 3 ;		    reserve space for local variables on stack
	LUI r22 104 ;		    load Constant char
	LLI r22 104 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 1 ;		z in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 30 ;		    load Constant
	LLI r22 30 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		y in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 51 ;		    load Constant char
	LLI r22 51 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 3 ;		v in Compound 1
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	JL r0 r0 ;		return
	JL r0 r0 ;		return
