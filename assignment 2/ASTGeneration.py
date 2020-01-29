# 1652579
# Pham Ngoc Thoai
import functools
from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *


class ASTGeneration(MCVisitor):
    def visitProgram(self, ctx: MCParser.ProgramContext):
        # return Program([FuncDecl(Id(ctx.ID().getText()), [],
        # self.visit(ctx.mctype()),Block([self.visit(ctx.body())] if ctx.body() else []))])
        decl_list = [self.visit(x) for x in ctx.declaration()]
        res = functools.reduce(lambda x, y: x + y if isinstance(y, list) else x + [y], decl_list, [])
        return Program(res)

    def visitDeclaration(self, ctx: MCParser.DeclarationContext):
        return self.visitChildren(ctx)

    # =============================== Function declare =================================================
    def visitFunction_declare(self, ctx: MCParser.Function_declareContext):
        name = Id(ctx.ID().getText())
        return_type = self.visit(ctx.function_type())
        para = self.visit(ctx.parameter_decl())
        return FuncDecl(name, para, return_type, self.visit(ctx.block_statement()))

    def visitFunction_type(self, ctx: MCParser.Function_typeContext):
        if ctx.INTTYPE():
            return IntType()
        elif ctx.BOOLEANTYPE():
            return BoolType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.STRINGTYPE():
            return StringType()
        elif ctx.VOIDTYPE():
            return VoidType()
        else:
            return self.visit(ctx.array_output_pointer())

    def visitArray_output_pointer(self, ctx: MCParser.Array_output_pointerContext):
        return ArrayPointerType(self.visit(ctx.primitive_type()))

    def visitParameter_decl(self, ctx: MCParser.Parameter_declContext):
        return self.visit(ctx.parameter_list())

    def visitParameter_list(self, ctx: MCParser.Parameter_listContext):
        para_list = [self.visit(x) for x in ctx.parameter()]

        return para_list

    def visitParameter(self, ctx: MCParser.ParameterContext):
        return self.visitChildren(ctx) if ctx.getChildCount() == 1 else VarDecl(ctx.ID().getText(), self.visit(ctx.primitive_type()))

    def visitArray_input_parameter(self, ctx: MCParser.Array_input_parameterContext):
        type = self.visit(ctx.primitive_type())
        name = ctx.ID().getText()
        return VarDecl(name, ArrayPointerType(type))

    # =============================== Variable declare ==================================================
    def visitVariable_declare(self, ctx: MCParser.Variable_declareContext):
        type = self.visit(ctx.primitive_type())
        var_list = self.visit(ctx.variables_list())

        var_decl = [VarDecl(x[0], ArrayType(x[1], type)) if isinstance(x, list) else VarDecl(x, type) for x in var_list]
        return var_decl

    def visitPrimitive_type(self, ctx: MCParser.Primitive_typeContext):
        if ctx.INTTYPE():
            return IntType()
        elif ctx.BOOLEANTYPE():
            return BoolType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.STRINGTYPE():
            return StringType()

    def visitVariables_list(self, ctx: MCParser.Variables_listContext):
        return [self.visit(x) for x in ctx.variable()]

    def visitVariable(self, ctx: MCParser.VariableContext):
        return ctx.ID().getText() if ctx.getChildCount() == 1 else [ctx.ID().getText(), int(ctx.INTLIT().getText())]

    # =============================== Statements ===================================================
    def visitStatement(self, ctx: MCParser.StatementContext):
        return self.visitChildren(ctx)

    def visitIf_statement(self, ctx: MCParser.If_statementContext):
        return self.visit(ctx.no_else_if_statement()) if ctx.no_else_if_statement() else self.visit(ctx.have_else_if_statement())

    def visitNo_else_if_statement(self, ctx: MCParser.No_else_if_statementContext):
        exp = self.visit(ctx.exp())
        stmt = self.visit(ctx.statement())
        return If(exp, stmt)

    def visitHave_else_if_statement(self, ctx: MCParser.Have_else_if_statementContext):
        exp = self.visit(ctx.exp())
        stmt = self.visit(ctx.statement(0))
        else_stmt = self.visit(ctx.statement(1))
        return If(exp, stmt, else_stmt)

    def visitDowhile_statement(self, ctx: MCParser.Dowhile_statementContext):
        stmt = [self.visit(x) for x in ctx.statement()]
        exp = self.visit(ctx.exp())
        return Dowhile(stmt, exp)

    def visitFor_statement(self, ctx: MCParser.For_statementContext):
        exp1 = self.visit(ctx.exp(0))
        exp2 = self.visit(ctx.exp(1))
        exp3 = self.visit(ctx.exp(2))
        stmt = self.visit(ctx.statement())
        return For(exp1, exp2, exp3, stmt)

    def visitContinue_statement(self, crx: MCParser.Continue_statementContext):
        return Continue()

    def visitBreak_statement(self, crx: MCParser.Break_statementContext):
        return Break()

    def visitReturn_statement(self, ctx: MCParser.Return_statementContext):
        return Return(self.visit(ctx.exp())) if ctx.exp() else Return()

    def visitBlock_statement(self, ctx: MCParser.Block_statementContext):
        lst = [self.visit(x) for x in ctx.block_stmts()]
        stmt_list = functools.reduce(lambda x, y: x + y if isinstance(y, list) else x + [y], lst, [])
        return Block(stmt_list)

    def visitBlock_stmts(self, ctx: MCParser.Block_stmtsContext):
        return self.visitChildren(ctx)

    def visitExpression_statement(self, ctx: MCParser.Expression_statementContext):
        return self.visit(ctx.exp())

    # ===============================Expression======================================================
    # def visitExpression(self, ctx: MCParser.ExpressionContext):
    #     if ctx.getChildCount() == 1:
    #         return self.visit(ctx.operands())
    #     elif ctx.getChildCount() == 2:
    #         op = ctx.NOT().getText() if ctx.NOT() else ctx.MINUSOP().getText()
    #         body = self.visit(ctx.expression(0))
    #         return UnaryOp(op, body)
    #     elif ctx.getChildCount() == 3:
    #         if ctx.LB():
    #             return self.visit(ctx.expression(0))
    #         elif ctx.assoc_int_expression(0):
    #             lhs = self.visit(ctx.assoc_int_expression(0))
    #             rhs = self.visit(ctx.assoc_int_expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #         elif ctx.nonassoc_bool_expression(0):
    #             lhs = self.visit(ctx.nonassoc_bool_expression(0))
    #             rhs = self.visit(ctx.nonassoc_bool_expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #         else:
    #             lhs = self.visit(ctx.expression(0))
    #             rhs = self.visit(ctx.expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #     else:
    #         return ArrayCell(self.visit(ctx.expression(0)), self.visit(ctx.expression(1)))
    #
    # def visitAssoc_int_expression(self, ctx: MCParser.Assoc_int_expressionContext):
    #     if ctx.getChildCount() == 1:
    #         return self.visit(ctx.operands())
    #     elif ctx.getChildCount() == 2:
    #         op = ctx.NOT().getText() if ctx.NOT() else ctx.MINUSOP().getText()
    #         body = self.visit(ctx.assoc_int_expression(0))
    #         return UnaryOp(op, body)
    #     elif ctx.getChildCount() == 3:
    #         if ctx.LB():
    #             return self.visit(ctx.expression())
    #         elif ctx.assoc_int_expression(0):
    #             lhs = self.visit(ctx.assoc_int_expression(0))
    #             rhs = self.visit(ctx.assoc_int_expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #         elif ctx.nonassoc_bool_expression(0):
    #             lhs = self.visit(ctx.nonassoc_bool_expression(0))
    #             rhs = self.visit(ctx.nonassoc_bool_expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #     else:
    #         return ArrayCell(self.visit(ctx.assoc_int_expression(0)), self.visit(ctx.assoc_int_expression(1)))
    #
    # def visitNonassoc_bool_expression(self, ctx: MCParser.Nonassoc_bool_expressionContext):
    #     if ctx.getChildCount() == 1:
    #         if ctx.operands():
    #             return self.visit(ctx.operands())
    #         else:
    #             return self.visit(ctx.assoc_int_expression(0))
    #     elif ctx.getChildCount() == 2:
    #         op = ctx.NOT().getText() if ctx.NOT() else ctx.MINUSOP().getText()
    #         body = self.visit(ctx.nonassoc_bool_expression(0))
    #         return UnaryOp(op, body)
    #     elif ctx.getChildCount() == 3:
    #         if ctx.LB():
    #             return self.visit(ctx.expression())
    #         elif ctx.nonassoc_bool_expression(0):
    #             lhs = self.visit(ctx.nonassoc_bool_expression(0))
    #             rhs = self.visit(ctx.nonassoc_bool_expression(1))
    #             return BinaryOp(ctx.getChild(1).getText(), lhs, rhs)
    #     else:
    #         return ArrayCell(self.visit(ctx.nonassoc_bool_expression(0)), self.visit(ctx.nonassoc_bool_expression(1)))
    def visitExp(self, ctx: MCParser.ExpContext):
        return self.visit(ctx.exp1()) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                self.visit(ctx.exp1()),
                                                                                self.visit(ctx.exp()))

    def visitExp1(self, ctx: MCParser.Exp1Context):
        return self.visit(ctx.exp2()) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                self.visit(ctx.exp1()),
                                                                                self.visit(ctx.exp2()))

    def visitExp2(self, ctx: MCParser.Exp2Context):
        return self.visit(ctx.exp3()) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                self.visit(ctx.exp2()),
                                                                                self.visit(ctx.exp3()))

    def visitExp3(self, ctx: MCParser.Exp3Context):
        return self.visit(ctx.exp4(0)) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                 self.visit(ctx.exp4(0)),
                                                                                 self.visit(ctx.exp4(1)))

    def visitExp4(self, ctx: MCParser.Exp4Context):
        return self.visit(ctx.exp5(0)) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                 self.visit(ctx.exp5(0)),
                                                                                 self.visit(ctx.exp5(1)))

    def visitExp5(self, ctx: MCParser.Exp5Context):
        return self.visit(ctx.exp6()) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                self.visit(ctx.exp5()),
                                                                                self.visit(ctx.exp6()))

    def visitExp6(self, ctx: MCParser.Exp6Context):
        return self.visit(ctx.exp7()) if ctx.getChildCount() == 1 else BinaryOp(ctx.getChild(1).getText(),
                                                                                self.visit(ctx.exp6()),
                                                                                self.visit(ctx.exp7()))

    def visitExp7(self, ctx: MCParser.Exp7Context):
        return self.visit(ctx.exp8()) if ctx.getChildCount() == 1 else UnaryOp(ctx.getChild(0).getText(),
                                                                               self.visit(ctx.exp7()))

    def visitExp8(self, ctx: MCParser.Exp8Context):
        return self.visit(ctx.exp9()) if ctx.getChildCount() == 1 else ArrayCell(self.visit(ctx.exp9()),
                                                                                 self.visit(ctx.exp()))

    def visitExp9(self, ctx: MCParser.Exp9Context):
        return self.visit(ctx.operands()) if ctx.getChildCount() == 1 else self.visit(ctx.exp())

    # ===============================Operands=================================================
    def visitOperands(self, ctx: MCParser.OperandsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.funcall():
            return self.visit(ctx.funcall())
        elif ctx.literal():
            return self.visit(ctx.literal())
        else:
            return self.visit(ctx.array_element())

    def visitArray_element(self, ctx: MCParser.Array_elementContext):
        arr = self.visit(ctx.funcall()) if ctx.funcall() else Id(ctx.ID().getText())
        idx = self.visit(ctx.exp())
        return ArrayCell(arr, idx)

    def visitLiteral(self, ctx: MCParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        else:
            val = True if ctx.BOOLLIT().getText() == "true" else False
            return BooleanLiteral(val)

    def visitFuncall(self, ctx: MCParser.FuncallContext):
        return CallExpr(Id(ctx.ID().getText()), self.visit(ctx.expression_list()) if ctx.expression_list() else [])

    def visitExpression_list(self, ctx: MCParser.Expression_listContext):
        return [self.visit(x) for x in ctx.exp()]


