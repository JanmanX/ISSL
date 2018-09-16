grammar SMEDSL;

import SMEDSLLexerRules;

specification	:       register_specification* 
                        clock_specification*
                        instruction_specification*
                        ;


// REGISTER SPECIFICATION
register_specification  :   type ID ('[' INT ']')? ;
register    :   ID ('[' INT ']') ; 


// CLOCK SPECIFICATION
clock_specification     :       'clock' '{' stat* '}' ;


// INSTRUCTION SPECIFICATION
instruction_specification   : ID ('(' ID (',' ID)* ')')? ':' (stat | '{' stat* '}') ;


// OTHER
stat    :    'while' '(' expr ')' stat          # while
        |    'if' '(' expr ')' stat             # if
        |    '{' stat* '}'                      # block
        |    ID '=' expr                        # assign
        ;


expr    :   '(' expr ')'                        # parens
        |   expr op=(OP_MUL | OP_DIV) expr      # MulDiv
        |   expr op=(OP_ADD | OP_SUB) expr      # AddSub
        |   expr op=(OP_EQ  | OP_NEQ) expr      # EqNeq
        |   ID                                  # id
        |   INT                                 # int
        ;

// TYPES
type    :   TYPE_INT
        |   TYPE_FLOAT
        ;

TYPE_FLOAT  :   'f' ('8'|'16'|'32'|'64'|'128'|'256'|'512') ;
TYPE_INT    :   ('i'|'u') ('8'|'16'|'32'|'64'|'128'|'256'|'512') ;
