/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     PROGRAM = 258,
     LIST = 259,
     WHILE = 260,
     INT = 261,
     STRING = 262,
     CHAR = 263,
     FOR = 264,
     VAR = 265,
     IF = 266,
     ELSE = 267,
     OUT = 268,
     IN = 269,
     FINISH = 270,
     RETURN = 271,
     plus = 272,
     minus = 273,
     multiply = 274,
     divide = 275,
     modulo = 276,
     lessOrEqual = 277,
     moreOrEqual = 278,
     less = 279,
     more = 280,
     equal = 281,
     assign = 282,
     different = 283,
     isequal = 284,
     not = 285,
     plusequal = 286,
     minusequal = 287,
     divideequal = 288,
     timesequal = 289,
     or = 290,
     and = 291,
     leftCurlyBracket = 292,
     rightCurlyBracket = 293,
     leftRoundBracket = 294,
     rightRoundBracket = 295,
     leftBracket = 296,
     rightBracket = 297,
     semicolon = 298,
     comma = 299,
     colon = 300,
     apostrophe = 301,
     quote = 302,
     identifier = 303,
     integer_constant = 304,
     char_constant = 305,
     string_constant = 306
   };
#endif
/* Tokens.  */
#define PROGRAM 258
#define LIST 259
#define WHILE 260
#define INT 261
#define STRING 262
#define CHAR 263
#define FOR 264
#define VAR 265
#define IF 266
#define ELSE 267
#define OUT 268
#define IN 269
#define FINISH 270
#define RETURN 271
#define plus 272
#define minus 273
#define multiply 274
#define divide 275
#define modulo 276
#define lessOrEqual 277
#define moreOrEqual 278
#define less 279
#define more 280
#define equal 281
#define assign 282
#define different 283
#define isequal 284
#define not 285
#define plusequal 286
#define minusequal 287
#define divideequal 288
#define timesequal 289
#define or 290
#define and 291
#define leftCurlyBracket 292
#define rightCurlyBracket 293
#define leftRoundBracket 294
#define rightRoundBracket 295
#define leftBracket 296
#define rightBracket 297
#define semicolon 298
#define comma 299
#define colon 300
#define apostrophe 301
#define quote 302
#define identifier 303
#define integer_constant 304
#define char_constant 305
#define string_constant 306




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

