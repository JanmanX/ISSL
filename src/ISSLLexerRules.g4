lexer grammar ISSLLexerRules;


// ID
ID  : ID_LETER (ID_LETER | DIGIT)*;

// Numbers
INT     : DIGIT+ ;
FLOAT   : DIGIT+ '.' DIGIT*
        | '.' DIGIT+
        ;

// Strings
STRING  : '"' ( ESC | .)*? '"'; // Notice the non-greedy notation *?

// Comments
COMMENT : '//' .*? '\n' -> skip;
// COMMENT_BLOCK        : '/*' .*? '*/' -> skip;

// Whitespaces
WS      : [ \t\n\r]+ -> skip;

// Operators
OP_ADD  : '+' ;
OP_SUB  : '-' ;
OP_MUL  : '*' ;
OP_DIV  : '/' ;
OP_EQ   : '==' ;
OP_NEQ  : '!=' ;


// Fragments
fragment DIGIT      : '0'..'9';
fragment ID_LETER   : 'a'..'z' | 'A'..'Z' | '_';
fragment ESC        : '\\' [btnr"\\] ; // Escape sequences, such as \b, \t, \n etc.
