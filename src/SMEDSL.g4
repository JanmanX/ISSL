grammar SMEDSL;

import SMEDSLLexerRules;


specification	:   register_specification*;


register_specification  :   type ID '[' INT ']' ;



// TYPES
type    :   TYPE_INT
        |   TYPE_FLOAT
        ;

TYPE_FLOAT  :   'f' ('32' | '64') ;
TYPE_INT    :   ('i'|'u') ('8'|'16'|'32'|'64'|'128'|'256'|'512') ;
