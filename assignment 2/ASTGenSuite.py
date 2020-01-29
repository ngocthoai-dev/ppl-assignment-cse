import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):
    def test_simple_var_declare(self):
        """test simple variable declaration"""
        input = """int main;"""
        expect = str(Program([VarDecl("main", IntType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 300))

    def test_simple_many_var_declare(self):
        """test simple many variable declarations"""
        input = """int i;
                    string str;
                    boolean boo;
                    float fl;"""
        expect = str(Program([VarDecl("i", IntType()), VarDecl("str", StringType()),
                              VarDecl("boo", BoolType()), VarDecl("fl", FloatType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 301))

    def test_simple_chain_var_declare(self):
        """test simple chain of variable declarations"""
        input = """int a, b, c, d;"""
        expect = str(Program([VarDecl("a", IntType()), VarDecl("b", IntType()),
                              VarDecl("c", IntType()), VarDecl("d", IntType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 302))

    def test_simple_func_declare(self):
        """test simple function declaration"""
        input = """int main() { }"""
        expect = str(Program([FuncDecl(Id("main"), [], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 303))

    def test_simple_func_declare_with_para(self):
        """test simple function declaration with parameter"""
        input = """int main(float a) {}"""
        expect = str(Program([FuncDecl(Id("main"), [VarDecl("a", FloatType())], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 304))

    def test_array_var_declare(self):
        """test array variable declaration"""
        input = """int main[2];"""
        expect = str(Program([VarDecl("main", ArrayType(2, IntType()))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 305))

    def test_array_and_normal_var_declare(self):
        """test array and normal variable declaration"""
        input = """boolean main, main1[2], main2[3], main3;"""
        expect = str(Program([VarDecl("main", BoolType()), VarDecl("main1", ArrayType(2, BoolType())),
                              VarDecl("main2", ArrayType(3, BoolType())),
                              VarDecl("main3", BoolType())]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 306))

    def test_input_para(self):
        """test array pointer type: input parameter"""
        input = """int main(int i[]) {}"""
        expect = str(
            Program([FuncDecl(Id("main"), [VarDecl("i", ArrayPointerType(IntType()))], IntType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 307))

    def test_input_normal_para(self):
        """test array pointer type: input parameter and normal parameter"""
        input = """void main(string s[], int i, boolean boo[]) {}"""
        expect = str(
            Program([FuncDecl(Id("main"), [VarDecl("s", ArrayPointerType(StringType())), VarDecl("i", IntType()),
                                           VarDecl("boo", ArrayPointerType(BoolType()))], VoidType(), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 308))

    def test_output_para(self):
        """test array pointer type: output parameter"""
        input = """int[] main() {}"""
        expect = str(Program([FuncDecl(Id("main"), [], ArrayPointerType(IntType()), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))

    def test_array_pointer_type(self):
        """test array pointer type: input & output parameter"""
        input = """int[] main(string s, boolean boo[]) {}"""
        expect = str(Program(
            [FuncDecl(Id("main"), [VarDecl("s", StringType()), VarDecl("boo", ArrayPointerType(BoolType()))],
                      ArrayPointerType(IntType()), Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))
