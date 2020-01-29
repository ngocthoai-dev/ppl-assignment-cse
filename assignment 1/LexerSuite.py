import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):

    def test_all_lowercase_identifier(self):
        """test identifier"""
        self.assertTrue(TestLexer.checkLexeme("abc", "abc,<EOF>", 101))

    def test_identifier_with_sensitive_case(self):
        """test identifier with sensitive case"""
        self.assertTrue(TestLexer.checkLexeme("aCBbdc", "aCBbdc,<EOF>", 102))

    def test_underscore_letter_digit_identifier(self):
        """test identifier with underscore, characters and digit"""
        self.assertTrue(TestLexer.checkLexeme("_aAsVN12", "_aAsVN12,<EOF>", 103))

    def test_digit_begin_identifier(self):
        """test identifier with number at first -> it's not number it's separate token to INTLIT and ID"""
        self.assertTrue(TestLexer.checkLexeme("12_abc", "12,_abc,<EOF>", 104), 'not ID and ID')

    def test_digit_then_letter(self):
        """test integer with ID on middle -> token integer + ID"""
        self.assertTrue(TestLexer.checkLexeme("123a123", "123,a123,<EOF>", 105))

    def test_identifier_with_letter_digit(self):
        """test integer at the end of ID -> ID"""
        self.assertTrue(TestLexer.checkLexeme("abC321", "abC321,<EOF>", 106))

    def test_integer_space_identifier(self):
        """test integer and ID by \t and space -> INTLIT, ID and INTLIT """
        self.assertTrue(TestLexer.checkLexeme("12   abs 555", "12,abs,555,<EOF>", 107))

    def test_integer_underscore_identifier_space(self):
        """test integer and ID by underscore and space -> INTLIT, ID and INTLIT"""
        self.assertTrue(TestLexer.checkLexeme("12__abs 555", "12,__abs,555,<EOF>", 108))

    def test_simple_float(self):
        """test simple float"""
        self.assertTrue(TestLexer.checkLexeme("012.123", "012.123,<EOF>", 109))

    def test_left_side_decimal_point(self):
        """test float without fractional number"""
        self.assertTrue(TestLexer.checkLexeme("12.", "12.,<EOF>", 110))

    def test_right_side_decimal_point(self):
        """test float without left part"""
        self.assertTrue(TestLexer.checkLexeme(".12", ".12,<EOF>", 111))

    def test_float_with_all_parts(self):
        """test float with all parts"""
        self.assertTrue(TestLexer.checkLexeme("1.12e1", "1.12e1,<EOF>", 112))

    def test_exponent_after_decimal_point(self):
        """test float missing number before exponent but have decimal point instead"""
        self.assertTrue(TestLexer.checkLexeme("12.e1", "12.e1,<EOF>", 113))

    def test_minus_exponent(self):
        """test float with minus after exponent"""
        self.assertTrue(TestLexer.checkLexeme("12.120e-12", "12.120e-12,<EOF>", 114))

    def test_negative_float(self):
        """test negative float"""
        self.assertTrue(TestLexer.checkLexeme("-12.12e-12", "-,12.12e-12,<EOF>", 115))

    def test_zero_before_exponent(self):
        """test float number 0 before exponent"""
        self.assertTrue(TestLexer.checkLexeme("000E1", "000E1,<EOF>", 116))

    def test_exponent_without_left_side(self):
        """test float without left part but enough the rest"""
        self.assertTrue(TestLexer.checkLexeme(".12E-1", ".12E-1,<EOF>", 117))

    def test_exponent_without_digit_right_side(self):
        """test float without any digit or dot before exponent -> not float"""
        self.assertTrue(TestLexer.checkLexeme("e-12", "e,-,12,<EOF>", 118), 'Wrong float literal')

    def test_two_decimal_point(self):
        """test float with double dot -> error character"""
        self.assertTrue(TestLexer.checkLexeme("12E2.34", "Error Token 12E2.", 119), 'Error float token')

    def test_true(self):
        """test boolean true"""
        self.assertTrue(TestLexer.checkLexeme("true", "true,<EOF>", 120))

    def test_true_false(self):
        """test boolean true and false"""
        self.assertTrue(TestLexer.checkLexeme("true false", "true,false,<EOF>", 121))

    def test_true_false_sensitive_letter(self):
        """test boolean true and false in sensitive case -> ID"""
        self.assertTrue(TestLexer.checkLexeme("TrUe False", "TrUe,False,<EOF>", 122), 'Wrong boolean literal')

    def test_uppercase_true_false(self):
        """test boolean true and false in upper case -> ID"""
        self.assertTrue(TestLexer.checkLexeme("TRUE FALSE", "TRUE,FALSE,<EOF>", 123), 'Wrong boolean literal')

    def test_simple_string_with_space(self):
        """test simple string"""
        self.assertTrue(TestLexer.checkLexeme('''"a  _"''', 'a  _,<EOF>', 124))

    def test_string_and_unclosed_string(self):
        """test string and unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('"abc!"abd"ab', 'abc!,abd,Unclosed String: ab', 125))

    def test_form_feed_escape(self):
        """test string with escape form feed"""
        self.assertTrue(TestLexer.checkLexeme('"test \\f string!"', 'test \\f string!,<EOF>', 126))

    def test_illegal_escape(self):
        """test string with illegal escape"""
        self.assertTrue(TestLexer.checkLexeme('"test \\i string!"', 'Illegal Escape In String: test \\i', 127),
                        'illegal escape \\i')

    def test_newline_escape(self):
        """test string with escape newline"""
        self.assertTrue(TestLexer.checkLexeme('"test \\n string!"', 'test \\n string!,<EOF>', 128))

    def test_slash_and_newline_escape(self):
        """test string with many escapes: backslash and newline"""
        self.assertTrue(TestLexer.checkLexeme('"test \\\\\\n string!"', 'test \\\\\\n string!,<EOF>', 129))

    def test_all_escape(self):
        """test string with all escapes"""
        self.assertTrue(TestLexer.checkLexeme('"test \\b\\f\\r\\n\\t\\"\\\\ string!"',
                                              'test \\b\\f\\r\\n\\t\\"\\\\ string!,<EOF>', 130))

    def test_two_string_and_ID(self):
        """test strings and ID"""
        self.assertTrue(TestLexer.checkLexeme('"abs12"  test  "13"', 'abs12,test,13,<EOF>', 131))

    def test_form_feed_one_slash(self):
        """test form feed"""
        self.assertTrue(TestLexer.checkLexeme('"test \f string!"', 'test \f string!,<EOF>', 132))

    def test_string_and_float(self):
        """test string and float"""
        self.assertTrue(TestLexer.checkLexeme('"test \\f string ??" 3e1 2.e3',
                                              'test \\f string ??,3e1,2.e3,<EOF>', 133))

    def test_unclosed_string(self):
        """test string unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('"test string!', 'Unclosed String: test string!', 134), 'unclosed string')

    def test_special_character(self):
        """test string with special character"""
        self.assertTrue(TestLexer.checkLexeme('"test \b string_"', 'test \b string_,<EOF>', 135))

    def test_slash_illegal_escape(self):
        """test string illegal escape"""
        self.assertTrue(TestLexer.checkLexeme('"test \\\\\\v string!"',
                                              'Illegal Escape In String: test \\\\\\v', 136),
                        'illegal escape \\v')

    def test_void(self):
        """test void type"""
        self.assertTrue(TestLexer.checkLexeme("void", "void,<EOF>", 137))

    def test_boolean(self):
        """test boolean type"""
        self.assertTrue(TestLexer.checkLexeme("boolean", "boolean,<EOF>", 138))

    def test_all_types(self):
        """test all types"""
        self.assertTrue(TestLexer.checkLexeme("int boolean void float string",
                                              "int,boolean,void,float,string,<EOF>", 139))

    def test_String_type(self):
        """test string uppercase"""
        self.assertTrue(TestLexer.checkLexeme("String", "String,<EOF>", 140), "not string type")

    def test_line_cmt(self):
        """test line comment"""
        self.assertTrue(TestLexer.checkLexeme("//a", "<EOF>", 141))

    def test_line_block_cmt(self):
        """test line comment and block commnent"""
        self.assertTrue(TestLexer.checkLexeme("//a/*test*/", "<EOF>", 142))

    def test_block_cmt(self):
        """test block comment"""
        self.assertTrue(TestLexer.checkLexeme('''/*
        ab * * %%^ cd
        */''', "<EOF>", 143))

    def test_normal_operators(self):
        """test normal operators"""
        self.assertTrue(TestLexer.checkLexeme("+- */%", "+,-,*,/,%,<EOF>", 144))

    def test_more_operators(self):
        """test not and sub operators"""
        self.assertTrue(TestLexer.checkLexeme("++-- -!", "+,+,-,-,-,!,<EOF>", 145))

    def test_relational_equality_operators(self):
        """test relational and equality operators"""
        self.assertTrue(TestLexer.checkLexeme("<<=>>= ==!=", "<,<=,>,>=,==,!=,<EOF>", 146))

    def test_boolean_assign_operators(self):
        """test boolean and assign operators"""
        self.assertTrue(TestLexer.checkLexeme("&&|| =", "&&,||,=,<EOF>", 147))

    def test_simple_math(self):
        """test simple equation"""
        self.assertTrue(TestLexer.checkLexeme("a = a+b", "a,=,a,+,b,<EOF>", 148))

    def test_math_with_different_type(self):
        """test simple mathematics"""
        self.assertTrue(TestLexer.checkLexeme("1+a+12.123", "1,+,a,+,12.123,<EOF>", 149))

    def test_complex_assign(self):
        """test normal operators"""
        self.assertTrue(TestLexer.checkLexeme("i = + ab - + abc;",
                                              "i,=,+,ab,-,+,abc,;,<EOF>", 150))

    def test_many_operators(self):
        """test normal operators"""
        self.assertTrue(TestLexer.checkLexeme("/+* 23", "/,+,*,23,<EOF>", 151))

    def test_string_operator(self):
        """test normal operators with string"""
        self.assertTrue(TestLexer.checkLexeme('"abs12" + -  13', 'abs12,+,-,13,<EOF>', 152))

    def test_operator_in_string(self):
        """test string operators"""
        self.assertTrue(TestLexer.checkLexeme('"+ ab - -&& 12"', '+ ab - -&& 12,<EOF>', 153))

    def test_square_bracket(self):
        """test separator"""
        self.assertTrue(TestLexer.checkLexeme("[]", "[,],<EOF>", 154))

    def test_all_separators(self):
        """test all separators"""
        self.assertTrue(TestLexer.checkLexeme("[]{}();,", "[,],{,},(,),;,,,<EOF>", 155))

    def test_other_and_separators(self):
        """test separators and others"""
        self.assertTrue(TestLexer.checkLexeme("ab,[12];ab,(34);",
                                              "ab,,,[,12,],;,ab,,,(,34,),;,<EOF>", 156))

    def test_string_and_separators(self):
        """test separators and others"""
        self.assertTrue(TestLexer.checkLexeme('"ab, ab"; ab_123)', 'ab, ab,;,ab_123,),<EOF>', 157))

    def test_break_continue_keywords(self):
        """test keywords"""
        self.assertTrue(TestLexer.checkLexeme("break continue", "break,continue,<EOF>", 158))

    def test_all_keyword(self):
        """test all keywords"""
        self.assertTrue(TestLexer.checkLexeme(
            "boolean break continue else for float if int return void do while true false string",
            "boolean,break,continue,else,for,float,if,int,return,void,do,while,"
            "true,false,string,<EOF>", 159))

    def test_keyword_in_sensitive_case(self):
        """test keywords in sensitive case"""
        self.assertTrue(TestLexer.checkLexeme("break Break BREAK", "break,Break,BREAK,<EOF>", 160),
                        "first one is keyword but the others two are ID")

    def test_simple_unclosed_string(self):
        """test unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('"abccd', 'Unclosed String: abccd', 161), "Unclosed string")

    def test_unclosed_string_by_newline_character(self):
        """test unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('"abcd \r"', 'Unclosed String: abcd ', 162),
                        "Unclosed string lexer")

    def test_error_character_and_string(self):
        """test error char"""
        self.assertTrue(TestLexer.checkLexeme('"+ 23" $ "- * 12"', '+ 23,Error Token $', 163),
                        "Error char")

    def test_illegal(self):
        """test illegal escape"""
        self.assertTrue(TestLexer.checkLexeme('" ab\\qccd "', 'Illegal Escape In String:  ab\\q', 164),
                        "Illegal escape")

    def test_two_illegal_escape(self):
        """test illegal escape"""
        self.assertTrue(TestLexer.checkLexeme('"abccd \\a" + "\\c"', 'Illegal Escape In String: abccd \\a', 165),
                        "Illegal escape")

    def test_declare_int(self):
        """test declare int"""
        self.assertTrue(TestLexer.checkLexeme('int i;', 'int,i,;,<EOF>', 166))

    def test_array_assign(self):
        """test equation"""
        self.assertTrue(TestLexer.checkLexeme('i = 3+ 2*+ int[3]',
                                              'i,=,3,+,2,*,+,int,[,3,],<EOF>', 167))

    def test_func_declare(self):
        """test main declare"""
        self.assertTrue(TestLexer.checkLexeme('void main() { }', 'void,main,(,),{,},<EOF>', 168))

    def test_array_declare(self):
        """test int array declare"""
        self.assertTrue(TestLexer.checkLexeme('int i[5]', 'int,i,[,5,],<EOF>', 169))

    def test_bool_array_declare(self):
        """test boolean array declare"""
        self.assertTrue(TestLexer.checkLexeme('boolean i[2]', 'boolean,i,[,2,],<EOF>', 170))

    def test_index_function(self):
        """test index expression"""
        self.assertTrue(TestLexer.checkLexeme('int []test() {}', 'int,[,],test,(,),{,},<EOF>', 171))

    def test_error_int_declare(self):
        """test int declare without size"""
        self.assertTrue(TestLexer.checkLexeme('int i[]', 'int,i,[,],<EOF>', 172))

    def test_func_declare_with_para(self):
        """test function name declare"""
        self.assertTrue(TestLexer.checkLexeme('int test(int i, float ab[])',
                                              'int,test,(,int,i,,,float,ab,[,],),<EOF>', 173))

    def test_string_have_keyword(self):
        """test string"""
        self.assertTrue(TestLexer.checkLexeme('"int {test all}"', 'int {test all},<EOF>', 174))

    def test_float_add_string(self):
        """test float and string"""
        self.assertTrue(TestLexer.checkLexeme('1.e-+ "string"', '1.,e,-,+,string,<EOF>', 175))

    def test_float_have_two_dot(self):
        """test error char"""
        self.assertTrue(TestLexer.checkLexeme('23.23e2.2e2', 'Error Token 23.23e2.', 176))

    def test_declare_int_var(self):
        """test int declare"""
        self.assertTrue(TestLexer.checkLexeme('int test10;', 'int,test10,;,<EOF>', 177))

    def test_wrong_right_side_assign(self):
        """test assign operation"""
        self.assertTrue(TestLexer.checkLexeme('test= 3.2e- + + 43;',
                                              'test,=,3.2,e,-,+,+,43,;,<EOF>', 178))

    def test_slash_quote_and_quote_nothing(self):
        """test slash quote and single quote"""
        self.assertTrue(TestLexer.checkLexeme('"test\t10++;\""', 'test\t10++;,Unclosed String: ', 179))

    def test_float_declare(self):
        """test float declare"""
        self.assertTrue(TestLexer.checkLexeme('float test11;', 'float,test11,;,<EOF>', 180))

    def test_many_assign_expression(self):
        """test assign sequence"""
        self.assertTrue(TestLexer.checkLexeme('test= 3.3e-+ - 12< !false;',
                                              'test,=,3.3,e,-,+,-,12,<,!,false,;,<EOF>', 181))

    def test_float_declare2(self):
        """test float declare"""
        self.assertTrue(TestLexer.checkLexeme('float test12;', 'float,test12,;,<EOF>', 182))

    def test_assign_ID(self):
        """test assign var"""
        self.assertTrue(TestLexer.checkLexeme('test12 = test10 + test11;',
                                              'test12,=,test10,+,test11,;,<EOF>', 183))

    def test_many_float_literal(self):
        """test float literal"""
        self.assertTrue(TestLexer.checkLexeme('1 .2 2. 3e1 .1e2 12 2 .e1',
                                              '1,.2,2.,3e1,.1e2,12,2,Error Token  .e', 184),
                        'Error float token')

    def test_built_in_func(self):
        """test built in function not support expression parameter"""
        self.assertTrue(TestLexer.checkLexeme('putBoolean((a || b) && (c || d));',
                                              'putBoolean,(,(,a,||,b,),&&,(,'
                                              'c,||,d,),),;,<EOF>', 185))

    def test_for(self):
        """test for"""
        self.assertTrue(TestLexer.checkLexeme('for (a=1; a<=3;) a=a+1;',
                                              'for,(,a,=,1,;,a,<=,3,;,),'
                                              'a,=,a,+,1,;,<EOF>', 186))

    def test_operators_and_cmt(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme('''// /* + - * % / 
                                                < > */ <= >=''', '<,>,*,/,<=,>=,<EOF>', 187))

    def test_cmt_line_vs_block_cmt(self):
        """test comment line and block"""
        self.assertTrue(TestLexer.checkLexeme('''// test
                                            /* // 123
                                            abc
                                            test123
                                            */''', '<EOF>', 188))

    def test_small_block_statement(self):
        """test small block statement"""
        self.assertTrue(TestLexer.checkLexeme('''{
                                                int a,b,c;
                                                a = b = c = 5;
                                                float f[5];
                                                if((a==b)||(b==c)) f[0] = 1.0;
                                            }''',
                                              '{,int,a,,,b,,,c,;,a,=,b,=,c,'
                                              '=,5,;,float,f,[,5,],;,if,(,(,'
                                              'a,==,b,),||,(,b,==,c,),),f,[,'
                                              '0,],=,1.0,;,},<EOF>', 189))

    def test_many_statements(self):
        """test some statements"""
        self.assertTrue(TestLexer.checkLexeme('''int a;
                                            a = foo;
                                            foo = func();
                                            putInt(a);''',
                                              'int,a,;,a,=,foo,;,foo,=,func,(,),'
                                              ';,putInt,(,a,),;,<EOF>', 190))

    def test_string_error_token_unclosed_string(self):
        """test string, error token, unclosed string"""
        self.assertTrue(TestLexer.checkLexeme('''"ab "  __#"''', "ab ,__,Error Token #", 191))

    def test_two_slash_quote(self):
        """test slash quote instead quote"""
        self.assertTrue(TestLexer.checkLexeme('''\"\"''', ',<EOF>', 192))

    def test_for_and_others(self):
        """test many statements"""
        self.assertTrue(TestLexer.checkLexeme('''float f;
                                            f = getFloat();
                                            for(float f1=0; f1>f; f1=f1%f){
                                                putFloat(f1);
                                            }''',
                                              'float,f,;,f,=,getFloat,(,),;,for,(,float,f1,=,0,;,f1,>,f,;,f1,=,f1,%,'
                                              'f,),{,putFloat,(,f1,),;,},<EOF>', 193))

    def test_do_while(self):
        """test many statements"""
        self.assertTrue(TestLexer.checkLexeme('''int i;
                                            i = getInt();
                                            do {
                                                putIntLn(i);
                                                i = i - getInt();
                                            } while(i >= 0 && i <= 10);''',
                                              'int,i,;,i,=,getInt,(,),;,do,{,putIntLn,(,i,),;,i,=,i,-,getInt,('
                                              ',),;,},while,(,i,>=,0,&&,i,<=,10,),;,<EOF>', 194))

    def test_for_if_intertwined(self):
        """test many statements"""
        self.assertTrue(TestLexer.checkLexeme('''float f;
                                            f = getFloat();
                                            for(float f1=0; f1>f; f1=f1%f){
                                                if(f < 0) {
                                                    break;
                                                } else {
                                                    continue;
                                                }
                                                putFloat(f1);
                                            }''',
                                              'float,f,;,f,=,getFloat,(,),;,for,(,float,f1,=,0,;,f1,>,f,;,f1,=,f1,%,'
                                              'f,),{,if,(,f,<,0,),{,break,;,},else,{,continue,;,},putFloat,(,f1,),'
                                              ';,},<EOF>', 195))

    def test_not_float(self):
        """test exponent without number after"""
        self.assertTrue(TestLexer.checkLexeme('13E', '13,E,<EOF>', 196))

    def test_error_token(self):
        """test ~"""
        self.assertTrue(TestLexer.checkLexeme('1231~2', '1231,Error Token ~', 197))

    def test_func_call(self):
        """test function call*"""
        self.assertTrue(TestLexer.checkLexeme('foo();', 'foo,(,),;,<EOF>', 198))

    def test_many_empty_string(self):
        """test empty string"""
        self.assertTrue(TestLexer.checkLexeme(''' "" "" "" ''', ',,,<EOF>', 199))

    def test_if_else_no_paren(self):
        """test more complex if in main function*"""
        self.assertTrue(TestLexer.checkLexeme('''void main() {
                                                if(x<=5+a)
                                                    x;
                                                if(x>5)
                                                    x;
                                                else
                                                    return x;
                                            }''',
                                              'void,main,(,),{,if,(,x,<=,5,+,a,),x,;,if,(,x,>,5,),x,;,'
                                              'else,return,x,;,},<EOF>', 200))
