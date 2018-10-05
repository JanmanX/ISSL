grammar ISSL;

import ISSLLexerRules;

specification	:    specs* ;


specs   :       register_specification 
        |       clock_specification
        |       instruction_specification
        ;


// REGISTER SPECIFICATION
register_specification  :   access_specifier? r_type ID ('[' INT ']')? ;
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

access_specifier        :    'hidden' 
                        ;

// TYPES
r_type    :   TYPE_INT
        |   TYPE_FLOAT
        ;

TYPE_FLOAT  :   'f' INT ;
TYPE_INT    :   ('i'|'u') INT ;
