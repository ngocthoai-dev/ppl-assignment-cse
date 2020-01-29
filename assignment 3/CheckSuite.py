"""1652579 Pham Ngoc Thoai"""
import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):
    """No Entry Point"""
    def test_no_void_main_func(self):
        """int foo() {
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([]))])
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_var_main_no_func(self):
        """int main;"""
        input = Program([VarDecl("main", IntType())])
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 401))

    """Redeclared"""
    def test_redeclared_function_name(self):
        """int foo(){
            }
            void main(){
            }
            int foo(){
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([])), FuncDecl(Id("foo"), [], IntType(), Block([]))])
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_redeclared_global_var(self):
        """int a;
            string b,c;
            float a;
            void main(){
            }"""
        input = Program([VarDecl("a", IntType()), VarDecl("b", StringType()), VarDecl("c", StringType()), VarDecl("a", FloatType()), VarDecl("main", IntType()), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_redeclared_global_arr_and_var(self):
        """int a[5];
            float a;
            void main(){
            }"""
        input = Program([VarDecl("a", ArrayType(5, IntType())), VarDecl("a", FloatType()), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_redeclared_global_array_pointer_func(self):
        """int foo(){
            }
            float[] foo(){
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([])), FuncDecl(Id("foo"), [], ArrayPointerType(FloatType()), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_mix_redeclared_global_decl(self):
        """int a,b;
            void foo(){
            }
            string a(){
            }
            int foo;
            void main(){
            }"""
        input = Program([VarDecl("a", IntType()), VarDecl("b", IntType()), FuncDecl(Id("foo"), [], VoidType(), Block([])), 
            FuncDecl(Id("a"), [], StringType(), Block([])), VarDecl("foo", IntType()), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Function: a"
        self.assertTrue(TestChecker.test(input, expect, 406))
    
    def test_redeclared_with_main(self):
        """int main(){
            } 
            void main(){
            }"""
        input = Program([FuncDecl(Id("main"), [], IntType(), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_redeclared_in_param(self):
        """int foo(float b, string b){
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("b", FloatType()), VarDecl("b", StringType())], VoidType(), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Parameter: b"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_redeclared_param_and_local(self):
        """void foo(int a, float b){ 
                string b; 
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", FloatType()), VarDecl("b", FloatType())], VoidType(), Block([VarDecl("b", StringType())])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 409))
    
    def test_redeclared_param_and_var_inside_block(self):
        """int foo(int a, float b){
                {
                    int a;
                    int b,c;
                    float c;    
                }
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", IntType()), VarDecl("b", FloatType())], IntType(), 
            Block([Block([VarDecl("a", IntType()), VarDecl("b", IntType()), VarDecl("c", IntType()), VarDecl("c", FloatType())])])), 
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Variable: c"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_redeclared_array_pointer_param(self):
        """int foo(int a, float a[]){
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", IntType()), VarDecl("a", ArrayPointerType(FloatType()))], IntType(), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 411))
    
    def test_redeclared_array_pointer_and_local(self):
        """int[] foo(float foo[]){ 
                int foo; 
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("foo", ArrayPointerType(FloatType()))], ArrayPointerType(IntType()), Block([VarDecl("foo", IntType())])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Redeclared Variable: foo"
        self.assertTrue(TestChecker.test(input, expect, 412))

    """Undeclared"""
    def test_simple_undeclared_func(self):
        """int fool(int foo) { 
                return foo; 
            }
            void main(){ 
                foo(); 
            }"""
        input = Program([FuncDecl(Id("fool"), [VarDecl("foo", IntType())], IntType(), Block([Return(Id("foo"))])),
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_undeclared_in_block_statement(self):
        """void main() {
                { 
                    c;
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Block([Id("c")])]))])
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_declared_late(self):
        """void main(){ 
                a; 
                int a; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Id("a"), VarDecl("a", IntType())]))])
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_declared_late_in_block(self):
        """void main(){
                int c;
                {
                    c;
                    d;
                    int d;
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("c", IntType()), Block([Id("c"), Id("d"), VarDecl("d", IntType())])]))])
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_declared_below_block(self):
        """void main(){ 
                { 
                    a; 
                } 
                int a; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Block([Id("a")]), VarDecl("a", IntType())]))])
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_undeclared_func(self):
        """void main(){ 
                foo(); 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_undeclared_pass_param(self):
        """void main(){ 
                foo(a); 
            }
            int foo(int a){
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [Id("a")])])), FuncDecl(Id("foo"), [VarDecl("a", IntType())], IntType(), Block([]))])
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 419))

    """type mismatch exp"""
    def test_type_mismatch_exp_arr_cell(self):
        """void main(){ 
                2[2]; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([ArrayCell(IntLiteral(2), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: ArrayCell(IntLiteral(2),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_var_type_mismatch_exp_arr_cell(self):
        """void main(){ 
                boolean a; 
                a[2]; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", BoolType()), ArrayCell(Id("a"), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_type_mismatch_exp_arr_cell_in_index(self):
        """void main(){ 
                boolean a[2]; 
                a[2.2]; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", BoolType()), ArrayCell(Id("a"), FloatLiteral(2.2))]))])
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),FloatLiteral(2.2))"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_boolean_in_plus_operator(self):
        """void main(){ 
                boolean a; 
                2+a; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", BoolType()), BinaryOp("+", IntLiteral(2), Id("a"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(+,IntLiteral(2),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_string_in_any_operator_except_assign(self):
        """void main(){ 
                2.3 * "2"; 
                2.3 - "2"; 
                2.3 != "2"; 
                2.3 == "2";
                !"2"; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("*", FloatLiteral(2.3), StringLiteral("2")),
            BinaryOp("-", FloatLiteral(2.3), StringLiteral("2")), BinaryOp("!=", FloatLiteral(2.3), StringLiteral("2")),
            BinaryOp("==", FloatLiteral(2.3), StringLiteral("2")), UnaryOp("!", StringLiteral("2"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(*,FloatLiteral(2.3),StringLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_not_bool_type_in_and_operator(self):
        """void main(){ 
                2&&3; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("&&", IntLiteral(2), IntLiteral(3))]))])
        expect = "Type Mismatch In Expression: BinaryOp(&&,IntLiteral(2),IntLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_not_bool_type_in_or_operator(self):
        """void main(){ 
                2.2||"3"; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("||", FloatLiteral(2.2), StringLiteral("3"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(||,FloatLiteral(2.2),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_equal_not_bool_or_int(self):
        """void main(){ 
                2.2=="3";
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("==", FloatLiteral(2.2), StringLiteral("3"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(==,FloatLiteral(2.2),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_equal_bool_in_one_side(self):
        """void main(){ 
                true=="3"; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("==", BooleanLiteral(True), StringLiteral("3"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(==,BooleanLiteral(true),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_var_invade_func_declare(self):
        """int foo(int foo) {
                return foo*foo(foo -1);   //Error
            }
            void main() {
                int foo;
                foo = 2;     
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("foo", IntType())], IntType(), Block([
                Return(BinaryOp("*", Id("foo"), CallExpr(Id("foo"), [BinaryOp("-", Id("foo"), IntLiteral(1))])))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("foo", IntType()), BinaryOp("=", Id("foo"), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[BinaryOp(-,Id(foo),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_not_equal_not_bool_or_int(self):
        """void main(){ 
                2!="3";
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("!=", IntLiteral(2), StringLiteral("3"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(!=,IntLiteral(2),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_not_equal_bool_or_int_in_one_side(self):
        """void main(){ 
                true!="3"; 
                2!=3.2; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("!=", BooleanLiteral(True), StringLiteral("3")), BinaryOp("!=", IntLiteral(2), FloatLiteral(3.2))]))])
        expect = "Type Mismatch In Expression: BinaryOp(!=,BooleanLiteral(true),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_less_than_on_bool_type(self):
        """void main(){ 
                3.2<true;
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("<", FloatLiteral(3.2), BooleanLiteral(True))]))])
        expect = "Type Mismatch In Expression: BinaryOp(<,FloatLiteral(3.2),BooleanLiteral(true))"
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_mod_not_int_type(self):
        """void main(){ 
                3.2%2;
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("%", FloatLiteral(3.2), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: BinaryOp(%,FloatLiteral(3.2),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_equal_different_type(self):
        """void main(){ 
                true==2; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([BinaryOp("==", BooleanLiteral(True), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: BinaryOp(==,BooleanLiteral(true),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_basic_operator_in_variable(self):
        """void main(){ 
                int a; 
                float b; 
                boolean c; 
                a+b-a*b;
                a/c; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", FloatType()), VarDecl("c", BoolType()), 
            BinaryOp("-", BinaryOp("+", Id("a"), Id("b")), BinaryOp("*", Id("a"), Id("b"))), 
            BinaryOp("/", Id("a"), Id("c"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(/,Id(a),Id(c))"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_and_or_in_int_type_var(self):
        """void main(){ 
                int a; 
                boolean b,c; 
                b||c&&a;
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", BoolType()), VarDecl("c", BoolType()),
            BinaryOp("||", Id("b"), BinaryOp("&&", Id("c"), Id("a")))]))])
        expect = "Type Mismatch In Expression: BinaryOp(&&,Id(c),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_equal_and_not_equal_float_type_var(self):
        """void main(){ 
                int a,b; 
                float c; 
                a!=b; 
                a==c; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", IntType()), VarDecl("c", FloatType()),
            BinaryOp("!=", Id("a"), Id("b")), BinaryOp("==", Id("a"), Id("c"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(==,Id(a),Id(c))"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_relational_not_in_int_or_float_type_var(self):
        """void main(){ 
                int a; 
                float b; 
                boolean c; 
                a<b; 
                b>=a; 
                a>b; 
                b<=c; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", FloatType()), VarDecl("c", BoolType()),
            BinaryOp("<", Id("a"), Id("b")), BinaryOp(">=", Id("b"), Id("a")),
            BinaryOp(">", Id("a"), Id("b")), BinaryOp("<=", Id("b"), Id("c"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(<=,Id(b),Id(c))"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_relational_on_another_exp(self):
        """void main(){ 
                int a; 
                (a<3.2)||true; 
                a+true;
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()),
            BinaryOp("||", BinaryOp("<", Id("a"), FloatLiteral(3.2)), BooleanLiteral(True)),
            BinaryOp("+", Id("a"), BooleanLiteral(True))]))])
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),BooleanLiteral(true))"
        self.assertTrue(TestChecker.test(input, expect, 439))
    
    def test_float_in_one_side_to_return_float_in_another_exp(self):
        """void main(){ 
                float a; 
                a/3>2; 
                a<"3"; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", FloatType()),
            BinaryOp(">", BinaryOp("/", Id("a"), IntLiteral(3)), IntLiteral(2)), 
            BinaryOp("<", Id("a"), StringLiteral("3"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(<,Id(a),StringLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_and_or_equal_in_another_exp(self):
        """void main(){ 
                boolean a,b; 
                a||b&&a==true; 
                a+2; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", BoolType()), VarDecl("b", BoolType()),
            BinaryOp("||", Id("a"), BinaryOp("&&", Id("b"), BinaryOp("==", Id("a"), BooleanLiteral(True)))),
            BinaryOp("+", Id("a"), IntLiteral(2))]))])
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_mod_return_int_in_another_exp(self):
        """void main(){ 
                int a; 
                a%2+3.2; 
                a%3.2; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()),
            BinaryOp("+", BinaryOp("%", Id("a"), IntLiteral(2)), FloatLiteral(3.2)),
            BinaryOp("%", Id("a"), FloatLiteral(3.2))]))])
        expect = "Type Mismatch In Expression: BinaryOp(%,Id(a),FloatLiteral(3.2))"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_not_without_bool_operand(self):
        """void main(){ 
                int a; 
                !a; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()),
            UnaryOp("!", Id("a"))]))])
        expect = "Type Mismatch In Expression: UnaryOp(!,Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_neg_without_int_and_float_operand(self):
        """void main(){ 
                float a,b; 
                -(a>b);
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", FloatType()), VarDecl("b", FloatType()),
            UnaryOp("-", BinaryOp(">", Id("a"), Id("b")))]))])
        expect = "Type Mismatch In Expression: UnaryOp(-,BinaryOp(>,Id(a),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_int_assign_to_float_but_not_vice_versa(self):
        """void main(){ 
                int a; 
                float b; 
                b=a; 
                a=b; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", FloatType()),
            BinaryOp("=", Id("b"), Id("a")),
            BinaryOp("=", Id("a"), Id("b"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_int_bool_string_assign_only_the_same_type(self):
        """void main(){ 
                int a; 
                boolean b; 
                string c; 
                a=2; 
                b=true; 
                c="c"; 
                a=b; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", BoolType()), VarDecl("c", StringType()),
            BinaryOp("=", Id("a"), IntLiteral(2)),
            BinaryOp("=", Id("b"), BooleanLiteral(True)),
            BinaryOp("=", Id("c"), StringLiteral("c")),
            BinaryOp("=", Id("a"), Id("b"))]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_assign_number_to_func(self):
        """void main(){ 
                int a[2]; 
                a[1] = 3;
                foo = 3; 
            }
            int foo(){
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", ArrayType(2, IntType())),
            BinaryOp("=", ArrayCell(Id("a"), IntLiteral(1)), IntLiteral(3)), BinaryOp("=", Id("foo"), IntLiteral(3))])),
            FuncDecl(Id("foo"), [], IntType(), Block([]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(foo),IntLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_assign_arr_pointer_not_prim_type(self):
        """int foo(int arr[]) {
                arr = 2; 
            }
            void main(){  
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("arr", ArrayPointerType(IntType()))], IntType(), Block([BinaryOp("=", Id("arr"), IntLiteral(2))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(arr),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input, expect, 448))
    
    def test_pass_wrong_type_to_func_call_in_func_call(self):
        """void foo(int a){
            }
            void main(){
                int a;
                foo(getInt(a)); // Error
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", IntType())], VoidType(), Block([])), 
            FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), CallExpr(Id("foo"), [CallExpr(Id("getInt"), [Id("a")])])]))])
        expect = "Type Mismatch In Expression: CallExpr(Id(getInt),[Id(a)])"
        self.assertTrue(TestChecker.test(input, expect, 449))
    
    """not left value"""
    def test_not_left_value_var(self):
        """void main(){
                int a;
                a = 3;
                3 = a; // Error
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            BinaryOp("=", Id("a"), IntLiteral(3)),
            BinaryOp("=", IntLiteral(3), Id("a"))]))])
        expect = "Not Left Value: IntLiteral(3)"
        self.assertTrue(TestChecker.test(input, expect, 450))
    
    def test_not_left_value_idx_exp(self):
        """void main(){
                int a[3];
                a[2] = 3; 
                "2.5" = 3; // Error
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", ArrayType(3, IntType())),
            BinaryOp("=", ArrayCell(Id("a"), IntLiteral(2)), IntLiteral(3)),
            BinaryOp("=", StringLiteral("2.5"), IntLiteral(3))]))])
        expect = "Not Left Value: StringLiteral(2.5)"
        self.assertTrue(TestChecker.test(input, expect, 451))
         
    """type mismatch stmt"""
    def test_test_type_mismatch_in_if_int_type_not_bool(self):
        """void main(){
                if(12){
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([If(IntLiteral(12), Block([]))]))])
        expect = "Type Mismatch In Statement: If(IntLiteral(12),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 452))
         
    def test_test_type_mismatch_in_if_variable_not_bool_type(self):
        """void main(){
                string a;
                if(a){
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", StringType()), If(Id("a"), Block([]))]))])
        expect = "Type Mismatch In Statement: If(Id(a),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 453))
         
    def test_type_mismatch_stmt_exp_1_in_for_not_int_type(self):
        """void main(){
                float fl;
                for(fl; 3<4; 3){
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("fl", FloatType()), For(Id("fl"), BinaryOp("<", IntLiteral(3), IntLiteral(4)), IntLiteral(3), Block([]))]))])
        expect = "Type Mismatch In Statement: For(Id(fl);BinaryOp(<,IntLiteral(3),IntLiteral(4));IntLiteral(3);Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 454))
         
    def test_type_mismatch_stmt_exp_2_in_for_not_bool_type(self):
        """void main(){
                int i;
                for(i; i; i){
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("i", IntType()), For(Id("i"), Id("i"), Id("i"), Block([]))]))])
        expect = "Type Mismatch In Statement: For(Id(i);Id(i);Id(i);Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 455))
         
    def test_type_mismatch_stmt_exp_3_in_for_not_int_type(self):
        """void main(){
                float fl;
                for(3; 3<4; fl){
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("fl", FloatType()), For(IntLiteral(3), BinaryOp("<", IntLiteral(3), IntLiteral(4)), Id("fl"), Block([]))]))])
        expect = "Type Mismatch In Statement: For(IntLiteral(3);BinaryOp(<,IntLiteral(3),IntLiteral(4));Id(fl);Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 456))
         
    def test_type_mismatch_stmt_exp_in_while_not_bool_type(self):
        """void main(){
                boolean boo;
                do {
                } while(boo);
                do {
                } while("s"); // Error
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("boo", BoolType()),
            Dowhile([Block([])], Id("boo")), Dowhile([Block([])], StringLiteral("s"))]))])
        expect = "Type Mismatch In Statement: Dowhile([Block([])],StringLiteral(s))"
        self.assertTrue(TestChecker.test(input, expect, 457))
         
    def test_type_mismatch_stmt_exp_in_return_void_type(self):
        """void main(){
                return 3; // Error
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Return(IntLiteral(3))]))])
        expect = "Type Mismatch In Statement: Return(IntLiteral(3))"
        self.assertTrue(TestChecker.test(input, expect, 458))
         
    def test_type_mismatch_stmt_return_not_float_or_int_type_in_float_func(self):
        """float bar(){
                return 2;
            }
            float foo(){ 
                boolean boo; 
                return boo; // Error
            }
            void main() { 
                foo(); 
            }"""
        input = Program([FuncDecl(Id("bar"), [], FloatType(), Block([Return(IntLiteral(2))])),
            FuncDecl(Id("foo"), [], FloatType(), Block([VarDecl("boo", BoolType()), Return(Id("boo"))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Type Mismatch In Statement: Return(Id(boo))"
        self.assertTrue(TestChecker.test(input, expect, 459))
         
    def test_type_mismatch_stmt_return_not_array_in_array_pointer_func(self):
        """int[] foo(int[] a){
                int b[2];
                return "s"; // Error
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", ArrayPointerType(IntType()))], ArrayPointerType(IntType()), Block([
            VarDecl("b", ArrayType(2, IntType())), Return(StringLiteral("s"))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Statement: Return(StringLiteral(s))"
        self.assertTrue(TestChecker.test(input, expect, 460))
         
    def test_type_mismatch_stmt_return_array_not_same_type_array_pointer_func(self):
        """int[] foo(float[] a){
                int b[2];
                return b;
                return a; // Error
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", ArrayPointerType(FloatType()))], ArrayPointerType(IntType()), Block([
            VarDecl("b", ArrayType(2, IntType())), Return(Id("b")), Return(Id("a"))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Statement: Return(Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 461))
         
    def test_type_mismatch_stmt_return_differ_type_to_func(self):
        """int foo(float[] a){
                int b;
                return b;
                return a; // Error
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", ArrayPointerType(FloatType()))], IntType(), Block([
            VarDecl("b", IntType()), Return(Id("b")), Return(Id("a"))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Statement: Return(Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 462))
         
    def test_type_mismatch_stmt_in_if_by_exp(self):
        """void main(){ 
                int a; 
                if(a==3){ 
                    if(a){
                    } // Error 
                } 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            If(BinaryOp("==", Id("a"), IntLiteral(3)), Block([If(Id("a"), Block([]))]))]))])
        expect = "Type Mismatch In Statement: If(Id(a),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 463))
         
    def test_type_mismatch_stmt_in_for_by_exp(self):
        """void main(){ 
                int a; 
                for(a-3; a=3; a*3){ // Error because a=3 return int not bool 
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            For(BinaryOp("-", Id("a"), IntLiteral(3)), BinaryOp("=", Id("a"), IntLiteral(3)), BinaryOp("*", Id("a"), IntLiteral(3)), Block([]))]))])
        expect = "Type Mismatch In Statement: For(BinaryOp(-,Id(a),IntLiteral(3));BinaryOp(=,Id(a),IntLiteral(3));BinaryOp(*,Id(a),IntLiteral(3));Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 464))
         
    def test_type_mismatch_stmt_in_dowhile_by_exp(self):
        """void main(){ 
                String a; 
                do {
                } while(a="s"); // Error because a="s" return string not bool 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", StringType()), 
            Dowhile([Block([])], BinaryOp("=", Id("a"), StringLiteral("s")))]))])
        expect = "Type Mismatch In Statement: Dowhile([Block([])],BinaryOp(=,Id(a),StringLiteral(s)))"
        self.assertTrue(TestChecker.test(input, expect, 465))
         
    def test_type_mismatch_stmt_for_in_if(self):
        """void main(){ 
                int a; 
                if(a==3){ 
                    for(a;a;a){
                    } // Error exp2 is not bool 
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            If(BinaryOp("==", Id("a"), IntLiteral(3)), Block([For(Id("a"), Id("a"), Id("a"), Block([]))]))]))])
        expect = "Type Mismatch In Statement: For(Id(a);Id(a);Id(a);Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 466))
         
    def test_type_mismatch_stmt_if_in_dowhile(self):
        """void main(){ 
                int a; 
                do 
                    if(a){
                    } // Error
                while(a==3);
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            Dowhile([If(Id("a"), Block([]))], BinaryOp("==", Id("a"), IntLiteral(3)))]))])
        expect = "Type Mismatch In Statement: If(Id(a),Block([]))"
        self.assertTrue(TestChecker.test(input, expect, 467))
         
    def test_type_mismatch_stmt_return_void_in_if(self):
        """void main(){ 
                int a; 
                if(a==3){ 
                    return a=3*2; // Error 
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), 
            If(BinaryOp("==", Id("a"), IntLiteral(3)), Block([Return(BinaryOp("=", Id("a"), BinaryOp("*", IntLiteral(3), IntLiteral(2))))]))]))])
        expect = "Type Mismatch In Statement: Return(BinaryOp(=,Id(a),BinaryOp(*,IntLiteral(3),IntLiteral(2))))"
        self.assertTrue(TestChecker.test(input, expect, 468))
         
    def test_type_mismatch_stmt_return_by_exp(self):
        """int foo(){ 
                int a; 
                if(a==3){ 
                    if(a<3){
                        return a+(2.3-a/2*a); // Error 
                    } 
                }
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([VarDecl("a", IntType()), 
            If(BinaryOp("==", Id("a"), IntLiteral(3)), Block([If(BinaryOp("==", Id("a"), IntLiteral(3)), 
                Block([Return(BinaryOp("+", Id("a"), 
                    BinaryOp("-", FloatLiteral(2.3), BinaryOp("*", BinaryOp("/", Id("a"), IntLiteral(2)), Id("a")))))]))]))])),
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,Id(a),BinaryOp(-,FloatLiteral(2.3),BinaryOp(*,BinaryOp(/,Id(a),IntLiteral(2)),Id(a)))))"
        self.assertTrue(TestChecker.test(input, expect, 469))
         
    def test_type_mismatch_stmt_return_wrong_type_in_for(self):
        """int main(){ 
                int a; 
                for(3; a>=3; a){ 
                    for(a=3; a<3; a+3){ 
                        return !true; // Error
                    } 
                } 
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([VarDecl("a", IntType()), 
            For(IntLiteral(3), BinaryOp(">=", Id("a"), IntLiteral(3)), Id("a"), Block([
                For(BinaryOp("=", Id("a"), IntLiteral(3)), BinaryOp("<", Id("a"), IntLiteral(3)), BinaryOp("+", Id("a"), IntLiteral(3)), 
                    Block([Return(UnaryOp("!", BooleanLiteral(True)))]))]))])),
            FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Type Mismatch In Statement: Return(UnaryOp(!,BooleanLiteral(true)))"
        self.assertTrue(TestChecker.test(input, expect, 470))

    """unreachable function"""
    def test_simple_unreachable_func_with_built_in_func(self):
        """float bar(){
                getInt();
                putLn();
                return getFloat();
            }
            float main(){
                return bar();
            }
            void foo(){
            }"""
        input = Program([FuncDecl(Id("bar"), [], FloatType(), Block([CallExpr(Id("getInt"), []), CallExpr(Id("putLn"), []), Return(CallExpr(Id("getFloat"), []))])),
            FuncDecl(Id("main"), [], FloatType(), Block([Return(CallExpr(Id("bar"), []))])),
            FuncDecl(Id("foo"), [], VoidType(), Block([]))])
        expect = "Unreachable Function: foo"
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_many_unreachable_func(self):
        """void foo(){
                voi();
            } 
            void main(){
            } 
            void voi(){
            } 
            void boo(){
                foo();
            } // unreach """
        input = Program([FuncDecl(Id("foo"), [], VoidType(), Block([CallExpr(Id("voi"), [])])), FuncDecl(Id("main"), [], VoidType(), Block([])),
            FuncDecl(Id("voi"), [], VoidType(), Block([])), FuncDecl(Id("boo"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Unreachable Function: boo"
        self.assertTrue(TestChecker.test(input, expect, 472))

    """break/continue not in loop"""
    def test_simple_break_not_in_loop(self):
        """void main(){ 
                break; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Break()]))])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 473))

    def test_simple_continue_not_in_loop(self):
        """void main(){ 
                continue; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Continue()]))])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_break_not_in_loop_but_if(self):
        """void main(){ 
                do {
                } while(false); 
                if(true) 
                    break; 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Dowhile([Block([])], BooleanLiteral(False)), If(BooleanLiteral(True), Break())]))])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_continue_in_if_in_loop(self):
        """void main(){ 
                do 
                    if(true) 
                        continue; 
                while(false); 
                break; // Error here
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Dowhile([If(BooleanLiteral(True), Continue())], BooleanLiteral(False)), Break()]))])
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 476))

    def test_break_in_loop_in_loop_in_if(self):
        """void main(){ 
                if(true) 
                    do 
                        for(3; 3<4; 4) 
                            break; 
                    while(false); 
                continue; // Error here
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([If(BooleanLiteral(True), 
            Dowhile([For(IntLiteral(3), BinaryOp("<", IntLiteral(3), IntLiteral(4)), IntLiteral(4), Break())], BooleanLiteral(False))), 
            Continue()]))])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 477))

    def test_break_in_if_in_loop_in_if(self):
        """void main(){ 
                if(true) 
                    do 
                        if(false) 
                            break; 
                    while(false); 
                continue; // Error here
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([If(BooleanLiteral(True), 
            Dowhile([If(BooleanLiteral(False), Break())], BooleanLiteral(False))), 
            Continue()]))])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_complex_break_not_in_loop(self):
        """void main(){ 
                if(true) 
                    if(3==3) 
                        do 
                            for(3; 3<4; 4) 
                            if(false) 
                                if(true) 
                                    break; 
                        while(false); 
                continue; // Error here
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([If(BooleanLiteral(True), If(BinaryOp("==", IntLiteral(3), IntLiteral(3)),
            Dowhile([For(IntLiteral(3), BinaryOp("<", IntLiteral(3), IntLiteral(4)), IntLiteral(4), 
                If(BooleanLiteral(False), If(BooleanLiteral(True), Break())))], BooleanLiteral(False)))), 
            Continue()]))])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 479))

    """function not return"""
    def test_simple_func_not_return(self):
        """int foo(){
            }
            void main(){
                foo();
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 480))

    def test_array_func_not_return(self):
        """float[] foo(){
            }
            void main(){
            }"""
        input = Program([FuncDecl(Id("foo"), [], ArrayPointerType(FloatType()), Block([])), FuncDecl(Id("main"), [], VoidType(), Block([]))])
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 481))

    def test_func_not_return_in_if_not_else(self):
        """string str(){ 
                if(2==2){ 
                    return "s"; 
                } 
                // Error
            }
            void main(){ 
                str(); 
            }"""
        input = Program([FuncDecl(Id("str"), [], StringType(), Block([If(BinaryOp("==", IntLiteral(2), IntLiteral(2)), Block([Return(StringLiteral("s"))]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Function str Not Return "
        self.assertTrue(TestChecker.test(input, expect, 482))

    def test_return_on_if_and_not_else(self):
        """int foo(){  
                if(2==2){ 
                    return 2; 
                }
                else {
                }
            }
            void main(){
                foo();
            }"""
        input = Program([FuncDecl(Id("foo"), [], IntType(), Block([If(BinaryOp("==", IntLiteral(2), IntLiteral(2)), Block([Return(IntLiteral(2))]), Block([]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("foo"), [])]))])
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_return_in_for(self):
        """string str(){ 
                for(2; 2==2; 2){ 
                    return "s";
                } // Error
            }
            void main(){
                str();
            }"""
        input = Program([FuncDecl(Id("str"), [], StringType(), Block([ 
                For(IntLiteral(2), BinaryOp("==", IntLiteral(2), IntLiteral(2)), IntLiteral(2), Block([Return(StringLiteral("s"))]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Function str Not Return "
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_complex_return_in_else_not_if(self):
        """string str(){ 
                int a, b;
                if(2==2){ 
                    {
                        return "s";
                    }
                } else {
                    if(a>b)
                        return "str";
                    else
                        if(a<=b)
                            "s"; // Error
                        else
                            return "s";
                } 
            }
            void main(){
                str();
            }"""
        input = Program([FuncDecl(Id("str"), [], StringType(), Block([VarDecl("a", IntType()), VarDecl("b", IntType()), 
                If(BinaryOp("==", IntLiteral(2), IntLiteral(2)), Block([Block([Return(StringLiteral("s"))])]), 
                    Block([If(BinaryOp(">", Id("a"), Id("b")), Return(StringLiteral("str")), 
                        If(BinaryOp("<=", Id("a"), Id("b")), StringLiteral("s"), Return(StringLiteral("s"))))]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Function str Not Return "
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test_return_in_block_in_for_in_block_not_outside(self):
        """string str(){ 
                { 
                    for(2; 2==2; 2){ 
                        { 
                            return "s"; 
                        } 
                    } 
                } 
                // Error
            }
            void main(){
                str();
            }"""
        input = Program([FuncDecl(Id("foo"), [], StringType(), Block([Block([ 
            For(IntLiteral(2), BinaryOp("==", IntLiteral(2), IntLiteral(2)), IntLiteral(2), Block([Block([Return(StringLiteral("s"))])]))])])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_func_not_return_in_if_in_for(self):
        """string str(){ 
                for(2; 2==2; 2){ 
                    if(2==2){ 
                        return "s";    
                    } 
                } // Error not return
            }
            void main(){ 
                str(); 
            }"""
        input = Program([FuncDecl(Id("foo"), [], StringType(), Block([
            For(IntLiteral(2), BinaryOp("==", IntLiteral(2), IntLiteral(2)), IntLiteral(2), Block([
                If(BinaryOp("==", IntLiteral(2), IntLiteral(2)), Block([Return(StringLiteral("s"))]))]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_complex_mismatch_in_return(self):
        """int[] foo(int a, int b[]){
                return b;
            }
            int foo1(int a){
                int c[5];
                return foo(a,c)[10]; 
            }
            float foo2(int a){
                return foo1(a); 
            }
            boolean foo3(int a){
                return foo1(a) + 2.2;      // Error because return float
            }
            void main(){
                int a;
                foo3(a);
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a", IntType()), VarDecl("b", ArrayPointerType(IntType()))], ArrayPointerType(IntType()), Block([Return(Id("b"))])), 
            FuncDecl(Id("foo1"), [VarDecl("a", IntType())], IntType(), Block([VarDecl("c", ArrayType(5, IntType())), Return(ArrayCell(CallExpr(Id("foo"), [Id("a"), Id("c")]), IntLiteral(10)))])), 
            FuncDecl(Id("foo2"), [VarDecl("a", IntType())], FloatType(), Block([Return(CallExpr(Id("foo1"), [Id("a")]))])), 
            FuncDecl(Id("foo3"), [VarDecl("a", IntType())], BoolType(), Block([Return(BinaryOp("+", CallExpr(Id("foo1"), [Id("a")]), FloatLiteral(2.2)))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), CallExpr(Id("foo3"), [Id("a")])]))])
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,CallExpr(Id(foo1),[Id(a)]),FloatLiteral(2.2)))"
        self.assertTrue(TestChecker.test(input, expect, 488))

    """mix all"""
    def test_return_array_pointer(self):
        """int[] foo(){ 
                return foo()[]; 
            };
            void main(){ 
                return foo()[2]; // Error 
            }"""
        input = Program([FuncDecl(Id("foo"), [], ArrayPointerType(IntType()), Block([Return(CallExpr(Id("foo"), []))])),
            FuncDecl(Id("main"), [], VoidType(), Block([Return(ArrayCell(CallExpr(Id("foo"), []), IntLiteral(2)))]))])
        expect = "Type Mismatch In Statement: Return(ArrayCell(CallExpr(Id(foo),[]),IntLiteral(2)))"
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_type_mismatch_complex_unary_exp(self):
        """boolean a(){ 
                return d; 
            } 
            int b; 
            int c; 
            boolean d; 
            void main(){ 
                do 
                    a(); 
                    { 
                        -!!!!!!!!!!a(); // Error
                    } 
                while(b > c); 
            }"""
        input = Program([FuncDecl(Id("a"), [], BoolType(), Block([Return(Id("d"))])), 
            VarDecl("b", IntType()), VarDecl("c", IntType()), VarDecl("d", BoolType()), 
            FuncDecl(Id("main"), [], VoidType(), Block([Dowhile([CallExpr(Id("a"), []), 
                Block([UnaryOp("-", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", UnaryOp("!", CallExpr(Id("a"), []))))))))))))])], BinaryOp(">", Id("b"), Id("c")))]))])
        expect = "Type Mismatch In Expression: UnaryOp(-,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,UnaryOp(!,CallExpr(Id(a),[]))))))))))))"
        self.assertTrue(TestChecker.test(input, expect, 490))
    
    def test_diff_num_of_param_in_call_builtin_expr(self):
        """void main(){
                putIntLn(3, getInt(), 3);
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("putIntLn"), [IntLiteral(3),  CallExpr(Id("getInt"), []), IntLiteral(3)])]))])
        expect = "Type Mismatch In Expression: CallExpr(Id(putIntLn),[IntLiteral(3),CallExpr(Id(getInt),[]),IntLiteral(3)])"
        self.assertTrue(TestChecker.test(input, expect, 491))
    
    def test_complex_continue_and_break_not_in_loop(self):
        """void main() { 
                do 
                    break; 
                while(true); 
                int a; int b; 
                {{{ 
                    for(a;true;b) break; 
                    {{{ 
                        continue; // Error
                    }}}  
                }}} 
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([Dowhile([Break()], BooleanLiteral(True)), 
            VarDecl("a", IntType()), VarDecl("b", IntType()), 
            Block([Block([Block([
                For(Id("a"), BooleanLiteral(True), Id("b"), Break()),
                Block([Block([Block([Continue()])])])])])])]))])
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 492))
    
    def test_complex_redeclared_var_and_func(self):
        """int a; 
            float b;
            int foo(){ 
                int a;
            }
            void main(){ 
                int main; 
            }
            void b(){
            }"""
        input = Program([VarDecl("a", IntType()), VarDecl("b", FloatType()), 
            FuncDecl(Id("foo"), [], IntType(), Block([VarDecl("a", IntType())])), 
            FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("main", IntType())])), 
            FuncDecl(Id("b"), [], VoidType(), Block([]))])
        expect = "Redeclared Function: b"
        self.assertTrue(TestChecker.test(input, expect, 493))
    
    def test_complex_undeclared_func(self):
        """int a;
            int foo(){ 
                flo(); 
                return a; 
            }
            float flo(){ 
                foo(); 
                return flo(); 
            }
            void main(){ 
                str(); 
            }"""
        input = Program([VarDecl("a",IntType()), 
            FuncDecl(Id("foo"), [], IntType(), Block([CallExpr(Id("flo"), []), Return(Id("a"))])), 
            FuncDecl(Id("flo"), [], FloatType(), Block([CallExpr(Id("foo"), []), Return(CallExpr(Id("flo"), []))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])]))])
        expect = "Undeclared Function: str"
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_complex_mix_all_exp(self):
        """int[] foo(int a){ 
                int arr[2]; 
                return arr; 
            }
            void main(){
                int b[10], a[10];
                int c, d, x;
                (1 - 3/4*5 % 6) == 2;  
                !true || !false != true;      
                foo(2)[3] = a[2] + 3;
                a[3] / c != b[9] * d;
                foo(3)[true && false] == a[1] - b[1] * x; //Error can not access array not integer
            }"""
        input = Program([FuncDecl(Id("foo"), [VarDecl("a",IntType())], ArrayPointerType(IntType()), Block([VarDecl("arr", ArrayType(2, IntType())), Return(Id("arr"))])),
            FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("b", ArrayType(10, IntType())), VarDecl("a", ArrayType(10, IntType())),
                VarDecl("c", IntType()), VarDecl("d", IntType()), VarDecl("x", IntType()),
                BinaryOp("==", BinaryOp("-", IntLiteral(1), BinaryOp("%", BinaryOp("*", BinaryOp("/", IntLiteral(3), IntLiteral(4)), IntLiteral(5)), IntLiteral(6))), IntLiteral(2)),
                BinaryOp("||", UnaryOp("!", BooleanLiteral(True)), BinaryOp("!=", UnaryOp("!", BooleanLiteral(False)), BooleanLiteral(True))),
                BinaryOp("=", ArrayCell(CallExpr(Id("foo"), [IntLiteral(2)]), IntLiteral(3)), BinaryOp("+", ArrayCell(Id("a"), IntLiteral(2)), IntLiteral(3))),
                BinaryOp("!=", BinaryOp("/", ArrayCell(Id("a"), IntLiteral(3)), Id("c")), BinaryOp("*", ArrayCell(Id("b"), IntLiteral(9)), Id("d"))),
                BinaryOp("==", ArrayCell(CallExpr(Id("foo"), [IntLiteral(3)]), BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False))), BinaryOp("-", ArrayCell(Id("a"), IntLiteral(1)), BinaryOp("*", ArrayCell(Id("b"), IntLiteral(1)), Id("x"))))]))])
        expect = "Type Mismatch In Expression: ArrayCell(CallExpr(Id(foo),[IntLiteral(3)]),BinaryOp(&&,BooleanLiteral(true),BooleanLiteral(false)))"
        self.assertTrue(TestChecker.test(input, expect, 495))
    
    def test_complex_unreachable_func(self):
        """boolean boo() { // Unreach
                if(a==2)
                    str();
                else 
                    return boo();
                return flo() > fl;
            }
            int a;
            int foo(){ 
                flo(); 
                return a; 
            }
            float flo(){ 
                foo(); 
                return fl; 
            }
            void main(){ 
                str(); 
            }
            string str() { 
                return s; 
            }
            string s;
            float fl;"""
        input = Program([FuncDecl(Id("boo"), [], BoolType(), Block([If(BinaryOp("==", Id("a"), IntLiteral(2)), 
                CallExpr(Id("str"), []), Return(CallExpr(Id("boo"), []))), Return(BinaryOp(">", CallExpr(Id("flo"), []), Id("fl")))])), 
            VarDecl("a", IntType()), 
            FuncDecl(Id("foo"), [], IntType(), Block([CallExpr(Id("flo"), []), Return(Id("a"))])), 
            FuncDecl(Id("flo"), [], FloatType(), Block([CallExpr(Id("foo"), []), Return(Id("fl"))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("str"), [])])), 
            FuncDecl(Id("str"), [], StringType(), Block([Return(Id("s"))])), 
            VarDecl("s", StringType()), 
            VarDecl("fl", FloatType())])
        expect = "Unreachable Function: boo"
        self.assertTrue(TestChecker.test(input, expect, 496))
    
    def test_complex_mix_stmt(self):
        """void main(){ 
                int a,b;
                float fl;
                {
                    if(a>b){
                        {
                            for(a; b<a; b){
                                if(fl>2.2)
                                    a=b;
                            }
                        }
                    } else {
                        do
                            fl = fl * a + b / fl;
                            if(a==b) 
                                fl = fl--1;
                            else 
                                fl;
                        while(true);
                        return (fl-b); // type mismatch
                    }
                }
            }"""
        input = Program([FuncDecl(Id("main"), [], VoidType(), Block([VarDecl("a", IntType()), VarDecl("b", IntType()), VarDecl("fl", FloatType()),
            Block([If(BinaryOp(">", Id("a"), Id("b")), Block([
                For(Id("a"), BinaryOp("<", Id("b"), Id("a")), Id("b"), Block([If(BinaryOp(">", Id("fl"), FloatLiteral(2.2)), BinaryOp("=", Id("a"), Id("b")))]))]),
                Block([Dowhile([BinaryOp("=", Id("fl"), BinaryOp("+", BinaryOp("*", Id("fl"), Id("a")), BinaryOp("/", Id("b"), Id("fl")))), 
                    If(BinaryOp("==", Id("a"), Id("b")), BinaryOp("=", Id("fl"), BinaryOp("-", Id("fl"), UnaryOp("-", IntLiteral(1)))), Id("fl"))], 
                    BooleanLiteral(True)), Return(BinaryOp("-", Id("fl"), Id("b")))]))])]))])
        expect = "Type Mismatch In Statement: Return(BinaryOp(-,Id(fl),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 497))
    
    def test_small_mix_program(self):
        """boolean boo(boolean boo) {
                if(boo) 
                    boo = flo() + foo(a) >= flo();
                else 
                    return boo;
                return flo() > fl;
            }
            int a;
            int foo(int foo){ 
                flo(); 
                return a+foo; 
            }
            float flo(){ 
                foo(a); 
                return fl; 
            }
            void main(){ 
                if(boo(true))
                    s;
                else
                    s = fl; // Error
            }
            string s;
            float fl;"""
        input = Program([FuncDecl(Id("boo"), [VarDecl("boo", BoolType())], BoolType(), Block([If(Id("boo"), 
            BinaryOp("=", Id("boo"), BinaryOp(">=", BinaryOp("+", CallExpr(Id("flo"), []), CallExpr(Id("foo"), [Id("a")])), CallExpr(Id("flo"), []))), 
                Return(Id("boo"))), Return(BinaryOp(">", CallExpr(Id("flo"), []), Id("fl")))])), 
            VarDecl("a", IntType()), 
            FuncDecl(Id("foo"), [VarDecl("foo", IntType())], IntType(), Block([CallExpr(Id("flo"), []), Return(BinaryOp("+", Id("a"), Id("foo")))])), 
            FuncDecl(Id("flo"), [], FloatType(), Block([CallExpr(Id("foo"), [Id("a")]), Return(Id("fl"))])),
            FuncDecl(Id("main"), [], VoidType(), Block([If(CallExpr(Id("boo"), [BooleanLiteral(True)]), Id("s"), BinaryOp("=", Id("s"), Id("fl")))])), 
            VarDecl("s", StringType()),
            VarDecl("fl", FloatType())])
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(s),Id(fl))"
        self.assertTrue(TestChecker.test(input, expect, 498))
    
    def test_complex_program(self):
        """boolean boo(boolean boo) {
                if(a==2) {
                    {
                        if(boo) {
                            for(a; boo; a){
                                return boo;
                            }
                            return boo;
                        }
                        return boo;
                    }
                }
                else 
                    return boo;
                return flo() > fl;
            }
            int a;
            float flo() {
                do
                    if(a==2) {
                        {
                            if(bool) {
                                for(a; bool; a){
                                    return fl;
                                }
                                return flo();
                            }
                            return flo();
                        }
                    }
                    else {
                        if(bool) {
                            return fl*fl;
                        }
                        else bool;               // Error not return in path else
                    }
                while(boo(bool));
            }
            void main() {
                boo(true);
            }
            float fl;
            boolean bool;"""
        input = Program([FuncDecl(Id("boo"), [VarDecl("boo", BoolType())], BoolType(), Block([If(BinaryOp("==", Id("a"), IntLiteral(2)),
                Block([Block([If(Id("boo"), Block([For(Id("a"), Id("boo"), Id("a"), Block([Return(Id("boo"))])), 
                    Return(Id("boo"))]), Return(Id("boo")))])]), Return(Id("boo"))), Return(BinaryOp(">", CallExpr(Id("flo"), []), Id("fl")))])), 
            VarDecl("a", IntType()), 
            FuncDecl(Id("flo"), [], FloatType(), Block([Dowhile([If(BinaryOp("==", Id("a"), IntLiteral(2)),
                    Block([Block([If(Id("bool"), Block([For(Id("a"), Id("bool"), Id("a"), Block([Return(Id("fl"))])), 
                        Return(CallExpr(Id("flo"), []))]), Return(CallExpr(Id("flo"), [])))])]),
                    Block([If(Id("bool"), Block([Return(BinaryOp("*", Id("fl"), Id("fl")))]), Id("bool"))]))], CallExpr(Id("boo"), [Id("bool")]))])), 
            FuncDecl(Id("main"), [], VoidType(), Block([CallExpr(Id("boo"), [BooleanLiteral(True)])])), 
            VarDecl("fl", FloatType()),
            VarDecl("bool", BoolType())])
        expect = "Function flo Not Return "
        self.assertTrue(TestChecker.test(input, expect, 499))