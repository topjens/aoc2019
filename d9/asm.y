%{
#include <stdio.h>

extern int yylex();
extern int yyparse();
extern FILE *yyin;

void yyerror(const char *s);

int opcode, mode1, mode2, mode3, arg1, arg2, arg3;

%}

%union {
	int i;
}

%token	<i>				INT RINT AINT
%token ADD
%token MUL
%token IN
%token OUT
%token JT
%token JF
%token LESS
%token EQU
%token ADB
%token HLT
%token NEWLINE

%start program

%%

program:		/* nothing */
		|		program line
		;

line:			NEWLINE
		|		expression NEWLINE
		;

expression:		ADD op1 ',' op2 ',' op3
				{
					opcode = 1;
					opcode += mode1 * 100;
					opcode += mode2 * 1000;
					opcode += mode3 * 10000;
					printf("%d,%d,%d,%d,", opcode, arg1, arg2, arg3);
				}
		|		MUL op1 ',' op2 ',' op3
				{
					opcode = 2;
					opcode += mode1 * 100;
					opcode += mode2 * 1000;
					opcode += mode3 * 10000;
					printf("%d,%d,%d,%d,", opcode, arg1, arg2, arg3);
				}
		|		IN op1
				{
					opcode = 3;
					opcode += mode1 * 100;
					printf("%d,%d,", opcode, arg1);
				}
		|		OUT op1
				{
					opcode = 4;
					opcode += mode1 * 100;
					printf("%d,%d,", opcode, arg1);
				}
		|		JT op1 ',' op2
				{
					opcode = 5;
					opcode += mode1 * 100;
					opcode += mode1 * 1000;
					printf("%d,%d,%d,", opcode, arg1, arg2);
				}
		|		JF op1 ',' op2
				{
					opcode = 6;
					opcode += mode1 * 100;
					opcode += mode1 * 1000;
					printf("%d,%d,%d,", opcode, arg1, arg2);
				}
		|		LESS op1 ',' op2 ',' op3
				{
					opcode = 7;
					opcode += mode1 * 100;
					opcode += mode2 * 1000;
					opcode += mode3 * 10000;
					printf("%d,%d,%d,%d,", opcode, arg1, arg2, arg3);
				}
		|		EQU op1 ',' op2 ',' op3
				{
					opcode = 8;
					opcode += mode1 * 100;
					opcode += mode2 * 1000;
					opcode += mode3 * 10000;
					printf("%d,%d,%d,%d,", opcode, arg1, arg2, arg3);
				}
		|		ADB op1
				{
					opcode = 9;
					opcode += mode1 * 100;
					printf("%d,%d,", opcode, arg1);
				}
		|		HLT
				{
					printf("99");
				}
		;

op1:			INT  { mode1 = 1; arg1 = $1; }
		|		RINT { mode1 = 2; arg1 = $1; }
		|		AINT { mode1 = 0; arg1 = $1; }
		;

op2:			INT  { mode2 = 1; arg2 = $1; }
		|		RINT { mode2 = 2; arg2 = $1; }
		|		AINT { mode2 = 0; arg2 = $1; }
		;

op3:			INT  { mode3 = 1; arg3 = $1; }
		|		RINT { mode3 = 2; arg3 = $1; }
		|		AINT { mode3 = 0; arg3 = $1; }
		;	
