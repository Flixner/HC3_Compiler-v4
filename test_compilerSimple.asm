#instructionsize 16
main: 
	LUI r22 0xFFDF ;		initialise STACK
	LLI r22 0xFFDF ;		
	MOV r1 r22 ;		
	SUBI r1 5 ;		    reserve space for local variables on stack
	LUI r22 1 ;		    load Constant
	LLI r22 1 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 3 ;		i in Compound 1
	STORE r10 r15 ;		and store result
test_compilerSimple_c_10_1_begin: 
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 3 ;		i in Compound 1
	LOAD r10 r15 ;		and load
	BZ r10 test_compilerSimple_c_10_1_false ;		if condition false
	BZ r0 test_compilerSimple_c_10_1_continue ;		jump to continue if not done
test_compilerSimple_c_10_1_false: 
	LUI r22 test_compilerSimple_c_10_1_end ;		jump to loop exit
	LLI r22 test_compilerSimple_c_10_1_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_10_1_continue: 
	LUI r22 0 ;		    load Constant
	LLI r22 65 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0x41 ;		    load Constant
	LLI r22 0x41 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		sub source B
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		if A == B ==> r10 == 0
	BZ r10 test_compilerSimple_c_74_8_one ;		creating a logical not
	MOV r10 r0 ;		result = FALSE
	BZ r0 test_compilerSimple_c_74_8_end ;		done
test_compilerSimple_c_74_8_one: 
	MOV r10 r0 ;		result = TRUE
	ADDI r10 1 ;		
test_compilerSimple_c_74_8_end: 
	BZ r10 test_compilerSimple_c_74_5_false ;		jump if condition false
	BZ r0 test_compilerSimple_c_74_5_then ;		jump to thenBlock if condition true
test_compilerSimple_c_74_5_false: 
	LUI r22 test_compilerSimple_c_74_5_else ;		jump to else Block
	LLI r22 test_compilerSimple_c_74_5_else ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_74_5_then: 
	LUI r22 0x80 ;		    load Constant
	LLI r22 0x80 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_74_5_end ;		jump over else Block
	LLI r22 test_compilerSimple_c_74_5_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_74_5_else: 
	LUI r22 15 ;		    load Constant
	LLI r22 15 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
test_compilerSimple_c_74_5_end: 
	LUI r22 2 ;		    load Constant
	LLI r22 2 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	MOV r12 r10 ;		Move to InputB
	LOAD r10 r15 ;		Load Variable
	ADD r10 r12 ;		add source B
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 67 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 5 ;		c1 in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	ADDI r1 1 ;		    Remove Arithmetic offset
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 5 ;		c1 in Compound 1
	LOAD r10 r15 ;		and load
	SUBI r1 1 ;		    Add Arithmetic offset
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		sub source B
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		if A == B ==> r10 == 0
	BZ r10 test_compilerSimple_c_87_8_one ;		creating a logical not
	MOV r10 r0 ;		result = FALSE
	BZ r0 test_compilerSimple_c_87_8_end ;		done
test_compilerSimple_c_87_8_one: 
	MOV r10 r0 ;		result = TRUE
	ADDI r10 1 ;		
test_compilerSimple_c_87_8_end: 
	BZ r10 test_compilerSimple_c_87_5_false ;		jump if condition false
	BZ r0 test_compilerSimple_c_87_5_then ;		jump to thenBlock if condition true
test_compilerSimple_c_87_5_false: 
	LUI r22 test_compilerSimple_c_87_5_else ;		jump to else Block
	LLI r22 test_compilerSimple_c_87_5_else ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_87_5_then: 
	LUI r22 0x100 ;		    load Constant
	LLI r22 0x100 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_87_5_end ;		jump over else Block
	LLI r22 test_compilerSimple_c_87_5_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_87_5_else: 
	LUI r22 15 ;		    load Constant
	LLI r22 15 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
test_compilerSimple_c_87_5_end: 
	LUI r22 0 ;		    load Constant
	LLI r22 65 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 2 ;		    load Constant
	LLI r22 2 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	ADD r10 r12 ;		add source B
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	MOV r12 r10 ;		Move to InputB
	LOAD r10 r15 ;		Load Variable
	SUB r10 r12 ;		sub source B
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		if A == B ==> r10 == 0
	BZ r10 test_compilerSimple_c_98_8_one ;		creating a logical not
	MOV r10 r0 ;		result = FALSE
	BZ r0 test_compilerSimple_c_98_8_end ;		done
test_compilerSimple_c_98_8_one: 
	MOV r10 r0 ;		result = TRUE
	ADDI r10 1 ;		
test_compilerSimple_c_98_8_end: 
	BZ r10 test_compilerSimple_c_98_5_false ;		jump if condition false
	BZ r0 test_compilerSimple_c_98_5_then ;		jump to thenBlock if condition true
test_compilerSimple_c_98_5_false: 
	LUI r22 test_compilerSimple_c_98_5_else ;		jump to else Block
	LLI r22 test_compilerSimple_c_98_5_else ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_98_5_then: 
	LUI r22 0x200 ;		    load Constant
	LLI r22 0x200 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_98_5_end ;		jump over else Block
	LLI r22 test_compilerSimple_c_98_5_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_98_5_else: 
	LUI r22 15 ;		    load Constant
	LLI r22 15 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
test_compilerSimple_c_98_5_end: 
	LUI r22 0 ;		    load Constant
	LLI r22 70 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	LUI r22 2 ;		    load Constant
	LLI r22 2 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	MOV r12 r10 ;		Move to InputB
	LOAD r10 r15 ;		Load Variable
	DIV r10 r12 ;		div by source B
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 35 ;		    load Constant
	LLI r22 35 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		sub source B
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		if A == B ==> r10 == 0
	BZ r10 test_compilerSimple_c_111_8_one ;		creating a logical not
	MOV r10 r0 ;		result = FALSE
	BZ r0 test_compilerSimple_c_111_8_end ;		done
test_compilerSimple_c_111_8_one: 
	MOV r10 r0 ;		result = TRUE
	ADDI r10 1 ;		
test_compilerSimple_c_111_8_end: 
	BZ r10 test_compilerSimple_c_111_5_false ;		jump if condition false
	BZ r0 test_compilerSimple_c_111_5_then ;		jump to thenBlock if condition true
test_compilerSimple_c_111_5_false: 
	LUI r22 test_compilerSimple_c_111_5_else ;		jump to else Block
	LLI r22 test_compilerSimple_c_111_5_else ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_111_5_then: 
	LUI r22 0x400 ;		    load Constant
	LLI r22 0x400 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_111_5_end ;		jump over else Block
	LLI r22 test_compilerSimple_c_111_5_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_111_5_else: 
	LUI r22 15 ;		    load Constant
	LLI r22 15 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
test_compilerSimple_c_111_5_end: 
	LUI r22 2 ;		    load Constant
	LLI r22 2 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	MOV r12 r10 ;		Move to InputB
	LOAD r10 r15 ;		Load Variable
	MUL r10 r12 ;		mul source B
	SLOI r10 8 ;		    Cast short to char
	SLOIR r10 8 ;		    Cast short to char
	STORE r10 r15 ;		and store result
	LUI r22 0 ;		    load Constant
	LLI r22 70 ;		    load Constant char
	MOV r10 r22 ;		move to expected position
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	ADDI r1 1 ;		    Remove Arithmetic offset
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 4 ;		c0 in Compound 1
	LOAD r10 r15 ;		and load
	SUBI r1 1 ;		    Add Arithmetic offset
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		sub source B
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	STORE r10 r15 ;		and store result
	MOV r15 r1 ;		calculate Adress of
	ADDI r15 2 ;		erg in Compound 1
	LOAD r10 r15 ;		and load
	STORE r10 r1 ;		push result of left node on stack
	SUBI r1 1 ;		in order to not interfer with right Node a
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r12 r10 ;		result is new inputB
	ADDI r1 1 ;		pop result of left node
	LOAD r10 r1 ;		and put in register for result
	SUB r10 r12 ;		if A == B ==> r10 == 0
	BZ r10 test_compilerSimple_c_124_8_one ;		creating a logical not
	MOV r10 r0 ;		result = FALSE
	BZ r0 test_compilerSimple_c_124_8_end ;		done
test_compilerSimple_c_124_8_one: 
	MOV r10 r0 ;		result = TRUE
	ADDI r10 1 ;		
test_compilerSimple_c_124_8_end: 
	BZ r10 test_compilerSimple_c_124_5_false ;		jump if condition false
	BZ r0 test_compilerSimple_c_124_5_then ;		jump to thenBlock if condition true
test_compilerSimple_c_124_5_false: 
	LUI r22 test_compilerSimple_c_124_5_else ;		jump to else Block
	LLI r22 test_compilerSimple_c_124_5_else ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_124_5_then: 
	LUI r22 0x800 ;		    load Constant
	LLI r22 0x800 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_124_5_end ;		jump over else Block
	LLI r22 test_compilerSimple_c_124_5_end ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_124_5_else: 
	LUI r22 15 ;		    load Constant
	LLI r22 15 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
test_compilerSimple_c_124_5_end: 
	LUI r22 0xF00 ;		    load Constant
	LLI r22 0xF00 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	STORE r10 r7 ;		set LEDR
	LUI r22 test_compilerSimple_c_10_1_begin ;		jump back to comparison
	LLI r22 test_compilerSimple_c_10_1_begin ;		
	JL r0 r22 ;		just jump
test_compilerSimple_c_10_1_end: 
	LUI r22 0 ;		    load Constant
	LLI r22 0 ;		    load Constant
	MOV r10 r22 ;		move to expected position
	MOV r4 r10 ;		move result into Return Register
	JL r0 r0 ;		return
	JL r0 r0 ;		return
