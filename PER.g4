grammar PER;

/*
 * Parser
 */

per                 : (statement | comment | WHITESPACE)+ EOF ;
statement           : OPEN command CLOSE ;
comment             : COMMENT ;
command             : ( defrule | defconst ) ;
defrule             : DEFRULE WHITESPACE+ proposition_list DEFRULE_SEPARATOR WHITESPACE* action_list ;
proposition_list    : ( proposition WHITESPACE+ )+ ;
proposition         : OPEN SYMBOL ( WHITESPACE (REL_OP | SYMBOL | SHORT) )+ WHITESPACE? CLOSE ;
action_list         : ( action WHITESPACE+ )+ ;
action              : OPEN SYMBOL ( WHITESPACE (SYMBOL | SHORT | STRING) )+ WHITESPACE? CLOSE ;
defconst            : DEFCONST WHITESPACE+ SYMBOL WHITESPACE+ SHORT ;

/*
 * Lexer
 */

OPEN                : '(' ;
CLOSE               : ')' ;
WHITESPACE          : ( ' ' | '\t' | NEWLINE ) ;
NEWLINE             : ( '\n' | '\r\n' ) ;

COMMENT             : ';' ~[\r\n]* NEWLINE ;

DEFRULE             : 'defrule' ;
DEFRULE_SEPARATOR   : '=>' ;

REL_OP              : ( REL_OP_FULL | REL_OP_SHORT ) ;
REL_OP_FULL         : ( 'less-than' | 'less-or-equal' | 'greater-than' | 'greater-or-equal' | 'equal' | 'not-equal' ) ;
REL_OP_SHORT        : ( '<' | '<=' | '>' | '>=' | '==' | '!=' ) ;

DEFCONST            : 'defconst' ;

STRING              : '"' ~["]* '"' ;
SHORT               : '-'? [0-9]+ ; // This needs to go at the bottom to make it lowere precedence than FACT_ARG... but that probably breaks defconst... FIXME
SYMBOL              : [a-z0-9\-]+ ; // This is likely too restrictive, but covers all of the values actually defined in the TC guide
