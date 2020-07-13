grammar PER;

/*
 * Parser
 */

per                 : (statement | lone_comment | WHITESPACE)+ EOF ;
statement           : OPEN command CLOSE ;
lone_comment        : COMMENT ;
command             : ( defrule | defconst | load | load_random_list ) ;
defrule             : DEFRULE whitespace_comment+ proposition_list DEFRULE_SEPARATOR whitespace_comment* action_list ;
proposition_list    : ( proposition whitespace_comment+ )+ ;
proposition         : OPEN SYMBOL proposition_arg* whitespace_comment? CLOSE ;
proposition_arg     : ( whitespace_comment (REL_OP | SYMBOL | SHORT | proposition) ) ;
action_list         : ( action whitespace_comment+ )+ ;
action              : OPEN SYMBOL action_arg* whitespace_comment? CLOSE ;
action_arg          : ( whitespace_comment (SYMBOL | SHORT | STRING) ) ;
defconst            : DEFCONST whitespace_comment+ SYMBOL whitespace_comment+ SHORT ;
load                : ( LOAD | LOADRANDOM ) whitespace_comment+ STRING whitespace_comment* ; // Treat load-random with only default as a load
load_random_list    : LOADRANDOM whitespace_comment+ random_file_list (whitespace_comment+ STRING)? whitespace_comment* ;
random_file_list    : ( random_file whitespace_comment+ )+ ;
random_file         : ( SHORT whitespace_comment+ STRING ) ;
whitespace_comment  : ( WHITESPACE+ COMMENT? WHITESPACE* ) ; // Allows comments to appear within this whitespace, COMMENT enforces a newline

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

LOAD                : 'load' ;
LOADRANDOM          : 'load-random' ;

STRING              : '"' ~["]* '"' ;
SHORT               : '-'? [0-9]+ ; // This needs to go at the bottom to make it lowere precedence than FACT_ARG... but that probably breaks defconst... FIXME
SYMBOL              : [a-zA-Z0-9\-]+ ; // This is likely too restrictive, but covers all of the values actually defined in the TC guide
