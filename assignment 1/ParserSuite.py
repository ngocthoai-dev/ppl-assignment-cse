import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):

    def test_int_declare(self):
        """test int declaration"""
        input = 'int i;'
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 201))

    def test_int_declare_and_initialize(self):
        """test int initialized beside declaration"""
        input = 'int i = 3;'
        expect = 'Error on line 1 col 6: ='
        self.assertTrue(TestParser.checkParser(input, expect, 202))

    def test_declare_many_float(self):
        """test float declaration with multiple vars"""
        input = 'float f, f1, f2, f3;'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 203))

    def test_boolean_array_declare(self):
        """test boolean array declaration"""
        input = 'boolean boo[3];'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 204))

    def test_string_array_declare_without_len(self):
        """test string declaration without size"""
        input = 'string s[];'
        expect = 'Error on line 1 col 9: ]'
        self.assertTrue(TestParser.checkParser(input, expect, 205))

    def test_float_declare_array_and_var(self):
        """test float declaration with array and normal"""
        input = 'float f[5], f1, f2;'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 206))

    def test_void_declare_var(self):
        """test void declaration for var"""
        input = 'void v;'
        expect = 'Error on line 1 col 6: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 207))

    def test_declare_without_ID(self):
        """test declaration without ID"""
        input = 'boolean ;'
        expect = 'Error on line 1 col 8: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 208))

    def test_declare_array_negative_len(self):
        """test declaration with negative array size"""
        input = 'float f[-4];'
        expect = 'Error on line 1 col 8: -'
        self.assertTrue(TestParser.checkParser(input, expect, 209))

    def test_all_var_type_declare(self):
        """test all var type declaration"""
        input = '''string s; int i; float f; boolean b;'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 210))

    def test_int_func_declare(self):
        """test simple function declaration"""
        input = 'int foo(){}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 211))

    def test_main_func_declare(self):
        """test void main function"""
        input = 'void main(){}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 212))

    def test_int_main_func_declare(self):
        """test int main function, here is not main for whole program"""
        input = 'int main(){}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 213))

    def test_float_declare(self):
        """test keyword for function name"""
        input = 'float int(){}'
        expect = 'Error on line 1 col 6: int'
        self.assertTrue(TestParser.checkParser(input, expect, 214))

    def test_semi_after_bool_func(self):
        """test semi after function declaration"""
        input = 'boolean test(){};'
        expect = 'Error on line 1 col 16: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 215))

    def test_func_with_simple_para(self):
        """test function with simple parameter"""
        input = 'int i(float f){}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 216))

    def test_func_with_arr_and_normal_para(self):
        """test function with 2 array and var float parameter"""
        input = 'int i(float f[], float f1){}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 217))

    def test_func_with_arr_with_len_para(self):
        """test function with array and size parameter"""
        input = 'boolean boo(float f[5]){}'
        expect = 'Error on line 1 col 20: 5'
        self.assertTrue(TestParser.checkParser(input, expect, 218))

    def test_func_and_built_in_func(self):
        """test function and built-in function"""
        input = 'string s(){putLn();}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 219))

    def test_two_dimensions_arr(self):
        """test 2 dimensions array"""
        input = 'void main() {i3[2][3];}'
        expect = 'Error on line 1 col 18: ['
        self.assertTrue(TestParser.checkParser(input, expect, 220))

    def test_assign_expression(self):
        """test assign"""
        input = 'void main() {i = 12 + ab - 32 + abc;}'
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 221))

    def test_declare_and_initial_var(self):
        """test declare and initial"""
        input = '''void main(){ float i; i = 12 + 32 + 235; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 222))

    def test_invocation_expression(self):
        """test invocation with expression parameter"""
        input = '''int foo(){ test(i = i + 23 + ab); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 223))

    def test_boolean_operator_assign(self):
        """test boolean assign"""
        input = '''int foo(){ i = (1||0); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 224))

    def test_invocation_with_float_para(self):
        """test invocation with float parameter"""
        input = '''int foo(float a){ foo(23.2e2); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 225))

    def test_two_times_assign(self):
        """test 2 assign expression"""
        input = '''int foo(){ a = b = c; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 226))

    def test_two_times_equality(self):
        """test 2 equality expression"""
        input = '''int foo(){ a == b == c; }'''
        expect = 'Error on line 1 col 18: =='
        self.assertTrue(TestParser.checkParser(input, expect, 227))

    def test_assign_and_equality(self):
        """test 2 assign with assign in middle"""
        input = '''int foo(){ a = b == c = d; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 228))

    def test_two_less_operator(self):
        """test 2 less than operators"""
        input = '''int foo(){ a < b < c; }'''
        expect = 'Error on line 1 col 17: <'
        self.assertTrue(TestParser.checkParser(input, expect, 229))

    def test_relational_operator_and_others(self):
        """test mixing operator"""
        input = '''int foo(){ a <= b + 2 == 1; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 230))

    def test_relational_equality(self):
        """test relational and equality expression"""
        input = '''int foo(){ a <= b == 3; }'''
        expect = 'Error on line 1 col 18: =='
        self.assertTrue(TestParser.checkParser(input, expect, 231))

    def test_assign_by_arr(self):
        """test assign by array"""
        input = '''int foo(){ int i[2]; a = i[1] + 1; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 232))

    def test_index_expression_func(self):
        """test index expression"""
        input = '''void main(){ foo(2)[3+x] = a[b[2]] +3; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 233))

    def test_relation_arr(self):
        """test relation between array with index expression with var"""
        input = '''int foo(){ a <= b[a+2]; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 234))

    def test_minus_negative_operator(self):
        """test -- operator"""
        input = '''int foo(){ a -- b[2]; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 235))

    def test_simple_if(self):
        """test simple if"""
        input = '''void main(){
                    if(x +3 < 5){
                        x+1;
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 236))

    def test_if_else(self):
        """test simple if else"""
        input = '''void main(){
                    if(x +3 < 5)
                        x = x + 1;
                    else {
                        x = x - 1;
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 237))

    def test_no_if_but_else(self):
        """test no if but else"""
        input = '''void main(){  float x; x = 2;
                    else x;
                }'''
        expect = 'Error on line 2 col 20: else'
        self.assertTrue(TestParser.checkParser(input, expect, 238))

    def test_if_ID(self):
        """test if identifier"""
        input = 'int if;'
        expect = 'Error on line 1 col 4: if'
        self.assertTrue(TestParser.checkParser(input, expect, 239))

    def test_if_else_no_paren(self):
        """test if no else then if else and return of void type"""
        input = '''void main() {
                    if(x<=5+a)
                        x = x + 1;
                    if(x>5)
                        x = x /2;
                    else
                        x = x%3;
                    return;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 240))

    def test_do_while(self):
        """test do while"""
        input = '''void main() {
                    do {
                        x = 0;
                    } while x;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 241))

    def test_for(self):
        """test for"""
        input = '''void main() {
                    for(i=0; i<5; i){
                        i = i+ 1;
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 242))

    def test_if_for(self):
        """test more complex for but error array without index"""
        input = '''void main() {
                    for(.2e-3; i<5; i){
                        if(i == 3)
                            i = i+ a[];
                    }
                }'''
        expect = 'Error on line 4 col 37: ]'
        self.assertTrue(TestParser.checkParser(input, expect, 243))

    def test_for_do_but_not_while(self):
        """test do inside for but lack while"""
        input = '''void main() {
                    for(i=0; i<5; i){
                        do {
                            i = i *2;
                        }
                    }
                }'''
        expect = 'Error on line 6 col 20: }'
        self.assertTrue(TestParser.checkParser(input, expect, 244))

    def test_if_for_without_paren(self):
        """test for inside if without parenthesis """
        input = '''void main() {
                    if(i<12)
                        for(0; i >= 12 + 3*a[1]; i){
                            i = getInt();
                        }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 245))

    def test_break_continue(self):
        """test break and continue"""
        input = '''void main() {
                    for(i=0; i<5; i){
                        break;
                        continue;
                        /*
                        comment
                        */
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 246))

    def test_for_semi(self):
        """test for has semi"""
        input = '''void main() {
                    for(i=0; i<5; i){
                        i = i *3.2;
                    };
                }'''
        expect = 'Error on line 4 col 21: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_lack_bracket_if(self):
        """test if condition lack close bracket"""
        input = '''void main() {
                    for(i=0; i<5; i){
                        if(!(i+3322111)
                            break;
                    }
                }'''
        expect = 'Error on line 4 col 28: break'
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_complex_do_while_for_if(self):
        """test complex do while, for and if no else"""
        input = '''void main() {
                    do {
                        for(i=0; i<5; i){
                            continue;
                        }
                        if(i>5)
                            break;
                        if(i<0)
                            continue;
                    } while(!0);
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test_continue_in_if(self):
        """test continue out of for"""
        input = '''void main() {
                    for(i;i<5;i)
                        continue;
                    if(i>5)
                        continue;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_return_many_func_but_one_error_type(self):
        """test return with many functions, one return int function with no exp"""
        input = '''int a;
                int f(){
                    return 1;
                }
                int b(){}
                int c(){
                    return;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 251))

    def test_empty_block_statement(self):
        """test block statement with no statement"""
        input = '''void main(){{}}'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 252))

    def test_exp_statement_without_semi(self):
        """test expression statement without semi"""
        input = 'int i'
        expect = 'Error on line 1 col 5: <EOF>'
        self.assertTrue(TestParser.checkParser(input, expect, 253))

    def test_assign_array_func(self):
        """test simple index statement"""
        input = '''void main(){ foo()[32] = abc; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 254))

    def test_more_assign_array_func(self):
        """test more complex index statement"""
        input = '''void main(){ 2 + foo(as[3])[2] = a + b + c; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 255))

    def test_built_in_newline_func(self):
        """test put new line outside any function"""
        input = 'putLn();'
        expect = 'Error on line 1 col 0: putLn'
        self.assertTrue(TestParser.checkParser(input, expect, 256))

    def test_built_in_put_int_func(self):
        """test putInt built in function"""
        input = '''void main(){ putInt(e); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 257))

    def test_built_in_put_int_outside_func(self):
        """test putIntLn outside function"""
        input = '''void main(){ int i; }
                putIntLn(a);'''
        expect = 'Error on line 2 col 16: putIntLn'
        self.assertTrue(TestParser.checkParser(input, expect, 258))

    def test_assign_by_built_in_func(self):
        """test initialize with getString function"""
        input = '''int test(){ string s = getString(); }'''
        expect = 'Error on line 1 col 21: ='
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test_complex_return_built_in_func(self):
        """test more complex built in function and return for non void type"""
        input = '''int test(){
                    if(a < 5)
                        putStringLn(s);
                    return getInt();
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 260))

    def test_simple_program(self):
        """test simple var declaration function"""
        input = '''void main(){ int i; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 261))

    def test_break_without_loop(self):
        """test break without loop"""
        input = '''int test(){
                    if(i=-5)
                        break;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 262))

    def test_assign_cmt_to_var(self):
        """test assign var by comment in function"""
        input = '''void main(){
                    int i ;
                    i = //test 2;
                }'''
        expect = 'Error on line 4 col 16: }'
        self.assertTrue(TestParser.checkParser(input, expect, 263))

    def test_many_simple_statement_in_program(self):
        """test more complex program"""
        input = '''void main(){
                    /* int i;
                    i = 5;
                    */
                    s = "string:";
                    putString(s);
                    boo = getBool();
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 264))

    def test_declare_many_and_assign(self):
        """test assign many times"""
        input = '''void main(){ a = b = c = 5; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 265))

    def test_ID_after_if_and_continue_with_no_loop(self):
        """test if no else then ID and continue outside loop"""
        input = '''void main(){
                    if(i = 5)_;
                    {
                        continue;
                    }
                    return;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 266))

    def test_assign_by_many_equality(self):
        """test assign by many equality expression"""
        input = '''void main(){ a = 5 == (b[0] == b[1]); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 267))

    def test_many_relation_equality(self):
        """test many relational and equality expression"""
        input = '''void main(){ a < (5 == 2) < 3; }'''
        expect = 'Error on line 1 col 26: <'
        self.assertTrue(TestParser.checkParser(input, expect, 268))

    def test_for_with_nothing(self):
        """test comment in for"""
        input = '''void main(){
                    for(a; a!=0; a){
                        // comment
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 269))

    def test_expression_without_semi_in_for(self):
        """test expression statement without semi in for"""
        input = '''void main(){ for("string"; !(a<=5); a ) { a = b = c = d[2] } }'''
        expect = 'Error on line 1 col 59: }'
        self.assertTrue(TestParser.checkParser(input, expect, 270))

    def test_global_declare(self):
        """test declare global variable"""
        input = '''int i;
                int test(){ }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 271))

    def test_semi_after_func(self):
        """test semi after function declaration"""
        input = '''int test(){ if(i>0) putLn(); };'''
        expect = 'Error on line 1 col 30: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 272))

    def test_one_declare_in_if(self):
        """test if only declare"""
        input = '''void main(){
                    if(i>0)
                        int foo;
                }'''
        expect = 'Error on line 3 col 24: int'
        self.assertTrue(TestParser.checkParser(input, expect, 273))

    def test_arr_para_and_arr_with_len_para(self):
        """test array size in parameter declaration"""
        input = '''int foo(string s[], int i[5]){}'''
        expect = 'Error on line 1 col 26: 5'
        self.assertTrue(TestParser.checkParser(input, expect, 274))

    def test_para_without_type_declare(self):
        """test parameter declaration without type"""
        input = ''' int i;
                int foo(int i, a){ return i; }'''
        expect = 'Error on line 2 col 31: a'
        self.assertTrue(TestParser.checkParser(input, expect, 275))

    def test_more_complex_func_call(self):
        """test invocation with two parameter var and float number"""
        input = '''int foo(int i[], float a){
                    if(a > (5 == 1)) return i[1];
                    return i[2];
                }
                void main(){ foo(i, 1.2e1); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 276))

    def test_string_func_return_and_int_func_return(self):
        """test more complex program"""
        input = ''' int i;
                int foo(){ return i; }
                string soo(){ return s + "__"; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test_nested_func(self):
        """test nested function"""
        input = ''' int i;
                void main(){
                    int foo(int i, int a){ return i; }
                }'''
        expect = 'Error on line 3 col 27: ('
        self.assertTrue(TestParser.checkParser(input, expect, 278))

    def test_invocation_in_do_while(self):
        """test do while and invocation inside"""
        input = '''void main(){
                    do {
                        foo(i[5], 12);
                    } while(a || b);
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 279))

    def test_do_while_for_with_empty_statement(self):
        """test if else, do while and for without statement"""
        input = '''void main(){
                    i = 5;
                    if(i>=12)
                        do {
                        } while(i||0);
                    else
                        for(i; i>5;i){
                        }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 280))

    def test_return_built_in_func(self):
        """test return built in function"""
        input = '''int foo(string s[]){ return getString(); }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 281))

    def test_recursive_index_func(self):
        """test recursive and index function"""
        input = '''int[] foo(int a, float b[]) {
                    if (a>0)
                        return foo(a-1,b);
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 282))

    def test_complex_if_no_else_arr_condition(self):
        """test complex if no else and if else"""
        input = '''void main(){
                    if(a[2])
                        a[0] = 0;
                    if(a[1])
                        a[2] = 0;
                    else{
                        a[1] = 0;
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 283))

    def test_complex_program_three_func(self):
        """test more complex program"""
        input = '''void main(){
                    stringTest("happy");
                    boolTest(a, 0.4);
                }
                void stringTest(string s){
                    putString(s);
                }
                boolean boolTest(int i[], float f){
                    if(!f){}
                    else
                        if(i[0] < f)
                            return i[0];
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 284))

    def test_main_func_main_var(self):
        """test function main and var main"""
        input = '''void main(){ int main; main = 1; }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 285))

    def test_index_func_with_arr_len_para(self):
        """test index function with array has size in parameter"""
        input = '''int[] foo(int i[5]){}'''
        expect = 'Error on line 1 col 16: 5'
        self.assertTrue(TestParser.checkParser(input, expect, 286))

    def test_illegal_escape_assign(self):
        """test illegal escape"""
        input = '''boolean boo(string s){
                    s = "test \\ ";
                }'''
        expect = 'test \\ '
        self.assertTrue(TestParser.checkParser(input, expect, 287))

    def test_complex_built_in_func(self):
        """test complex built in function"""
        input = '''void main ( ) {
                    main = f ( ) ;
                    putIntLn ( main ) ;
                    {
                        putIntLn    ( i ) ;
                    }
                    putIntLn ( main ) ;
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 288))

    def test_complex_nest_if(self):
        """test complex if nested"""
        input = '''void main(){
                    if(i < 5){
                        i = i + 1;
                    } else {
                        if(putBool(i))
                            if(i)
                                putIntLn(i);
                    }
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 289))

    def test_tail_call_optimization(self):
        """test simple tail call optimization"""
        input = '''int foo(float a, float b){
                    /* comment
                    */
                    if(a == 1 && a > 0)
                        return b;
                    return foo(a-1, a*b);
                }
                void main(){
                    // tail call opt
                    i = foo(getInt(), 1);
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 290))

    def test_lack_paren(self):
        """test unclosed parenthesis in main function"""
        input = '''void main(){'''
        expect = 'Error on line 1 col 12: <EOF>'
        self.assertTrue(TestParser.checkParser(input, expect, 291))

    def test_for_lack_paren(self):
        """test lack of close parenthesis"""
        input = '''void main(){
                    {
                        for(i; test< 5&&0;i){
                    }
                }'''
        expect = 'Error on line 5 col 17: <EOF>'
        self.assertTrue(TestParser.checkParser(input, expect, 292))

    def test_arr_lack_bracket(self):
        """test unclosed array index in index function"""
        input = '''float[] foo(int a[]){
                    {
                        a[i+1;
                    }
                }'''
        expect = 'Error on line 3 col 29: ;'
        self.assertTrue(TestParser.checkParser(input, expect, 293))

    def test_illegal_escape_string_assign(self):
        """test illegal escape"""
        input = '''int foo(){
                    s = " \\i ";
                }'''
        expect = ' \\i'
        self.assertTrue(TestParser.checkParser(input, expect, 294))

    def test_two_func_declare_like_var(self):
        """test two functions declaration like variables"""
        input = '''int foo0(){
                    return 1;
                }, foo1(){
                    return 2;
                }'''
        expect = 'Error on line 3 col 17: ,'
        self.assertTrue(TestParser.checkParser(input, expect, 295))

    def test_if_lack_bracket(self):
        """test lack of bracket of if statement"""
        input = '''int foo0(){
                    if(i<50
                        i;
                }'''
        expect = 'Error on line 3 col 24: i'
        self.assertTrue(TestParser.checkParser(input, expect, 296))

    def test_do_without_paren(self):
        """test do without parenthesis"""
        input = '''void main(){
                    do
                        test;
                    while(test);
                }'''
        expect = 'successful'
        self.assertTrue(TestParser.checkParser(input, expect, 297))

    def test_for_without_three_conditions(self):
        """test for with no condition for stopping"""
        input = '''void main() {
                    for(;;){
                        i = 1;
                    }
                }'''
        expect = "Error on line 2 col 24: ;"
        self.assertTrue(TestParser.checkParser(input, expect, 298))

    def test_if_without_condition(self):
        """test if with no condition and main lack close parenthesis"""
        input = '''void main () {
                    if(){
                        putFloat(1.e1);  }
                }'''
        expect = "Error on line 2 col 23: )"
        self.assertTrue(TestParser.checkParser(input, expect, 299))

    def test_complex_expression(self):
        """test function index call"""
        input = """int main(){
                        foo(3)[1 && false] > foo(2)[foo(3)[2] - true];
                   }"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 300))
