#instructionsize 16
test: 
	STORE r2 r1 ;		function entry-point
	SUBI r1 1 ;		together with above: save(push) FUNC on stack
	STORE r3 r1 ;		push LINK on stack (just in case)
	SUBI r1 1 ;		...
	MOV r2 r1 ;		set Function Basepointer = STACK on calltime
	SUBI r1 1 ;		    reserve space for local variables on stack
	LUI r22 1 ;		    load Constant
	LLI r22 1 ;		    load Constant
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
	LUI r22 10 ;		    load Constant
	LLI r22 10 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		y in Compound 1
	MOV r12 r10 ;		Move to InputB
	LOAD r10 r15 ;		Load Variable
	ADD r10 r12 ;		add source B
	SLOI r10 8 ;		    Cast short to char
	SARIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	JL r0 r0 ;		return
	JL r0 r0 ;		return
