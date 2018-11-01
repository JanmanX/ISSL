grammar ISSL;

import ISSLLexerRules;

specification	:    specs* ;


specs   :       bus_specification 
        |       clock_specification     
        |       stage_specification
        ;


// BUS SPECIFICATION
bus_specification  :      modifier='exposed'? 'bus' ID '{' channel_specification* '}'     ; 
channel_specification  :   r_type ID ; // TODO: ('[' INT ']')? ;


// CLOCK SPECIFICATION
clock_specification     :       'clock' '{' clock_stage* '}'     ;
clock_stage             :       ID    ;


// STAGE SPECIFICATION
stage_specification     :       ID '{' stat* '}'        ;


// OTHER
stat    :    'for' '(' iterator=qualified_id '=' from_=expr 'to' to=expr ')' stat  # for
        |    'if' '(' expr ')' stat             # if
        |    '{' stat* '}'                      # block
        |    qualified_id '=' expr              # assign
        |    datatype ID ('=' expr)?              # varDecl 
        ;

expr    :   '(' expr ')'                        # parens
        |   left=expr op=(OP_MUL | OP_DIV) right=expr  # MulDiv
        |   left=expr op=(OP_ADD | OP_SUB) right=expr  # AddSub
        |   left=expr op=(OP_EQ  | OP_NEQ) right=expr  # EqNeq
        |   qualified_id                        # id
        |   INT                                 # int
        |   '[' first=expr (',' rest+=expr)* ']'            # initializerList
        ;


// TYPES
qualified_id    :   ID ('.' ID)*    
                |   qualified_id '[' expr ']';  // array index


datatype    :   r_type array_specifier*;
r_type  :   TYPE_INT 
        |   TYPE_FLOAT
        ;
array_specifier    : '[' INT? ']'   ;

TYPE_FLOAT  :   'f' INT ;
TYPE_INT    :   ('i'|'u') INT ;

