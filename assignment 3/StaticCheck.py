"""1652579 Pham Ngoc Thoai"""
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return 'MType([' + ','.join([str(i) for i in self.partype]) + '],' + str(self.rettype) + ')'

class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype # MType, int, float, bool, string, array, arraypointer

    def __str__(self):
        return 'Symbol(' + self.name + ',' + str(self.mtype) + ')'

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
        Symbol("getInt", MType([], IntType())),
        Symbol("putInt", MType([IntType()], VoidType())),
        Symbol("putIntLn", MType([IntType()], VoidType())),
        Symbol("getFloat", MType([], FloatType())),
        Symbol("putFloat", MType([FloatType()], VoidType())),
        Symbol("putFloatLn", MType([FloatType()], VoidType())),
        Symbol("putBool", MType([BoolType()], VoidType())),
        Symbol("putBoolLn", MType([BoolType()], VoidType())),
        Symbol("putString", MType([StringType()], VoidType())),
        Symbol("putStringLn", MType([StringType()], VoidType())),
        Symbol("putLn", MType([], VoidType()))
    ]
            
    
    def __init__(self,ast):
        #print(ast)
        #print(ast)
        #print()
        self.ast = ast
 
    
    def check(self):
        return self.visit(self.ast, StaticChecker.global_envi)

    def flatten(self, lst):
        if not lst:
            return []
        return lst[0] + self.flatten(lst[1:])

    def visitProgram(self, ast, builtin):
        funcDecl = self.flatten(list(map(lambda decl: self.visit(decl, ([[]], True)), filter(lambda decl: type(decl) is FuncDecl, ast.decl))))
        declarations = reduce(lambda env, decl: [self.visit(decl, (env, True)) + env[0]], ast.decl, [[]])
        declarations[0] = declarations[0] + builtin
        mainFunc = self.lookup("main", funcDecl, lambda x: x.name)
        if mainFunc is None:
            raise NoEntryPoint()
        invokedList = [mainFunc]
        list(map(lambda decl: self.visit(decl, (declarations, False, invokedList)), filter(lambda decl: type(decl) is FuncDecl, ast.decl)))
        if len(funcDecl) != len(invokedList):
            raise UnreachableFunction(list(filter(lambda func: func.name not in list(map(lambda func: func.name, invokedList)), funcDecl))[0].name)
        return []

    def visitFuncDecl(self, ast, track_global):
        try:
            paramLst = reduce(lambda env, param: [env[0] + self.visit(param, (env, False))], ast.param, [[]])
        except Redeclared as e:
            raise Redeclared(Parameter(), e.n)
        if track_global[1]:
            if ast.name.name in [globalDecl.name for globalDecl in self.flatten(track_global[0])]:
                raise Redeclared(Function(), ast.name.name)
            return [Symbol(ast.name.name, MType([x.mtype for x in self.flatten(paramLst)], ast.returnType))]
        func = self.lookup(ast.name.name, list(filter(lambda decl: type(decl.mtype) is MType, self.flatten(track_global[0]))), lambda x: x.name)
        env = paramLst + track_global[0]
        isReturned = []
        for member in ast.body.member:
            if type(member) is VarDecl:
                env = [self.visit(member, (env, False)) + env[0], env[1]]
            else:
                # first param is env, second is get return value, third is the current function, the fourth is in loop scope checking, and the last is invokedList
                isReturned += self.visit(member, (env, False, func, False, track_global[2]))
        if not any(isReturned) and type(func.mtype.rettype) is not VoidType:
            raise FunctionNotReturn(func.name)
        return []

    def visitVarDecl(self, ast, track_decl):
        if ast.variable in [var.name for var in track_decl[0][0]]:
            raise Redeclared(Variable(), ast.variable)
        return [Symbol(ast.variable, ast.varType)]

    def visitBinaryOp(self, ast, track_exp):
        leftType = self.visit(ast.left, (track_exp[0], True, track_exp[2], track_exp[3], track_exp[4]))
        rightType = self.visit(ast.right, (track_exp[0], True, track_exp[2], track_exp[3], track_exp[4]))
        if ast.op in ['+', '-', '*', '/', '<', '<=', '>', '>=']:
            if type(leftType) not in [FloatType, IntType] or type(rightType) not in [FloatType, IntType]:
                raise TypeMismatchInExpression(ast)
            if ast.op in ['<', '<=', '>', '>=']:
                leftType = BoolType()
            elif FloatType in [type(leftType), type(rightType)]:
                leftType = FloatType()
        elif ast.op in ['&&', '||']:
            if type(leftType) is not BoolType or type(rightType) is not BoolType:
                raise TypeMismatchInExpression(ast)
            leftType = BoolType()
        elif ast.op in ['==', '!=']:
            if type(leftType) not in [IntType, BoolType] or type(rightType) not in [IntType, BoolType]:
                raise TypeMismatchInExpression(ast)
            if type(leftType) != type(rightType):
                raise TypeMismatchInExpression(ast)
            leftType = BoolType()
        elif ast.op is '%':
            if type(leftType) is not IntType or type(rightType) is not IntType:
                raise TypeMismatchInExpression(ast)
            leftType = IntType()
        else:
            if type(ast.left) not in [Id, ArrayCell]:
                raise NotLeftValue(ast.left)
            if type(leftType) not in [IntType, FloatType, BoolType, StringType]:
                raise TypeMismatchInExpression(ast)
            if type(leftType) in [IntType, BoolType, StringType] and type(rightType) != type(leftType):
                raise TypeMismatchInExpression(ast)
            if type(leftType) is FloatType and (type(rightType) not in [IntType, FloatType]):
                raise TypeMismatchInExpression(ast)
        if track_exp[1] == True:
            return leftType
        return []

    def visitUnaryOp(self, ast, track_exp):
        bodyType = self.visit(ast.body, (track_exp[0], True, track_exp[2], track_exp[3], track_exp[4]))
        if (ast.op == '!' and type(bodyType) is not BoolType) or (ast.op == '-' and type(bodyType) not in [FloatType, IntType]):
            raise TypeMismatchInExpression(ast)
        if track_exp[1] is True:
            return bodyType
        return []

    def visitCallExpr(self, ast, track_decl): 
        func = self.lookup(ast.method.name, self.flatten(track_decl[0]), lambda x: x.name)
        if func is None:
            raise Undeclared(Function(), ast.method.name)
        if type(func.mtype) is not MType:
            raise TypeMismatchInExpression(ast)
        if func.name != track_decl[2].name and func not in StaticChecker.global_envi and func.name not in [func.name for func in track_decl[4]]:
            track_decl[4].append(func)
        formerParam = func.mtype.partype
        actualParam = [self.visit(x, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4])) for x in ast.param]
        if len(formerParam) != len(actualParam):
            raise TypeMismatchInExpression(ast)
        else:
            for idx in range(len(formerParam)):
                leftType = formerParam[idx]
                rightType = actualParam[idx]
                if type(leftType) is ArrayPointerType:
                    if type(rightType) not in [ArrayPointerType, ArrayType]:
                        raise TypeMismatchInExpression(ast)
                    elif type(rightType.eleType) is not type(leftType.eleType):
                        raise TypeMismatchInExpression(ast)
                if type(leftType) in [IntType, BoolType, StringType] and type(rightType) != type(leftType):
                    raise TypeMismatchInExpression(ast)
                if type(leftType) is FloatType and (type(rightType) not in [IntType, FloatType]):
                    raise TypeMismatchInExpression(ast)
        if track_decl[1] is True:
            return func.mtype.rettype
        return []

    def visitArrayCell(self, ast, track_exp):
        arrType = self.visit(ast.arr, (track_exp[0], True, track_exp[2], track_exp[3], track_exp[4]))
        idxType = self.visit(ast.idx, (track_exp[0], True, track_exp[2], track_exp[3], track_exp[4]))
        if (type(idxType) is not IntType) or (type(arrType) is not ArrayType and type(arrType) is not ArrayPointerType):
            raise TypeMismatchInExpression(ast)
        if track_exp[1] is True:
            return arrType.eleType
        return []

    def visitIf(self, ast, track_decl):
        expr = self.visit(ast.expr, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
        if type(expr) is not BoolType:
            raise TypeMismatchInStatement(ast)
        thenStmtHasReturn = self.visit(ast.thenStmt, (track_decl[0], False, track_decl[2], track_decl[3], track_decl[4]))
        elseStmtHasReturn = self.visit(ast.elseStmt, (track_decl[0], False, track_decl[2], track_decl[3], track_decl[4])) if ast.elseStmt is not None else []
        return [all((thenStmtHasReturn if thenStmtHasReturn == [True] else [False]) + (elseStmtHasReturn if elseStmtHasReturn == [True] else [False]))]

    def visitFor(self, ast, track_decl):
        expr1 = self.visit(ast.expr1, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
        expr2 = self.visit(ast.expr2, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
        expr3 = self.visit(ast.expr3, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
        if type(expr1) is not IntType or type(expr3) is not IntType or type(expr2) is not BoolType:
            raise TypeMismatchInStatement(ast)
        self.visit(ast.loop, (track_decl[0], False, track_decl[2], True, track_decl[4]))
        return []

    def visitDowhile(self, ast, track_decl):
        exp = self.visit(ast.exp, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
        stmtList = []
        if type(exp) is not BoolType:
            raise TypeMismatchInStatement(ast)
        env = [[]] + track_decl[0]
        for member in ast.sl:
            if type(member) is VarDecl:
                env = [self.visit(member, (env, False, track_decl[2], track_decl[3], track_decl[4])) + env[0]] + track_decl[0]
            else:
                stmtList += self.visit(member, (env, False, track_decl[2], True, track_decl[4]))
        return [any(stmtList)] if any(stmtList) else []

    def visitBreak(self, ast, inLoop):
        if not inLoop[3]:
            raise BreakNotInLoop()
        return []

    def visitContinue(self, ast, inLoop):
        if not inLoop[3]:
            raise ContinueNotInLoop()
        return []

    def visitReturn(self, ast, track_decl):
        if type(track_decl[2].mtype.rettype) is VoidType:
            if ast.expr is not None:
                raise TypeMismatchInStatement(ast)
        else:
            if ast.expr is None:
                raise TypeMismatchInStatement(ast)
            exprType = self.visit(ast.expr, (track_decl[0], True, track_decl[2], track_decl[3], track_decl[4]))
            if type(track_decl[2].mtype.rettype) is FloatType:
                if type(exprType) not in [IntType, FloatType]:
                    raise TypeMismatchInStatement(ast)
            elif type(track_decl[2].mtype.rettype) is ArrayPointerType:
                if type(exprType) not in [ArrayType, ArrayPointerType]:
                    raise TypeMismatchInStatement(ast)
                elif type(track_decl[2].mtype.rettype.eleType) is not type(exprType.eleType):
                    raise TypeMismatchInStatement(ast)
            elif type(track_decl[2].mtype.rettype) != type(exprType):
                raise TypeMismatchInStatement(ast)
        return [True]

    def visitIntLiteral(self,ast, track_decl):
        if track_decl[1] is True:
            return IntType()
        return []
    
    def visitFloatLiteral(self,ast, track_decl): 
        if track_decl[1] is True:
            return FloatType()
        return []

    def visitBooleanLiteral(self,ast, track_decl):
        if track_decl[1] is True:
            return BoolType()
        return []
    
    def visitStringLiteral(self,ast, track_decl):
        if track_decl[1] is True:
            return StringType()
        return []

    def visitId(self, ast, track_decl):
        var = self.lookup(ast.name, self.flatten(track_decl[0]), lambda x: x.name)
        if var is None:
            raise Undeclared(Identifier(), ast.name)
        if track_decl[1] is True:
            return var.mtype
        return []

    def visitBlock(self, ast, track_decl):
        env = [[]] + track_decl[0]
        stmtList = []
        for member in ast.member:
            if type(member) is VarDecl:
                env = [self.visit(member, (env, False, track_decl[2], track_decl[3], track_decl[4])) + env[0]] + track_decl[0]
            else:
                stmtList += self.visit(member, (env, False, track_decl[2], track_decl[3], track_decl[4]))
        return [any(stmtList)] if any(stmtList) else []
