# 1652579 - Pham Ngoc Thoai
'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
# literal, expr, stmt, var declaration(global, local, param), array pointer type, array local, array global, short-circuit
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

class CodeGenerator(Utils):
  def __init__(self):
    self.libName = "io"

  def init(self):
    return [
      Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
      Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
      Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
      Symbol("getFloat", MType(list(), FloatType()), CName(self.libName)),
      Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
      Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
      Symbol("putBool", MType([BoolType()], VoidType()), CName(self.libName)),
      Symbol("putBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
      Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
      Symbol("putStringLn", MType([StringType()], VoidType()), CName(self.libName)),
      Symbol("putLn", MType([], VoidType()), CName(self.libName))
    ]

  def gen(self, ast, dir_):
    #ast: AST
    #dir_: String

    gl = self.init()
    gc = CodeGenVisitor(ast, gl, dir_)
    gc.visit(ast, None)

class ClassType(Type):
  def __init__(self, cname):
    #cname: String
    self.cname = cname

  def __str__(self):
    return "ClassType"

  def accept(self, v, param):
    return v.visitClassType(self, param)

class SubBody():
  def __init__(self, frame, sym):
    #frame: Frame
    #sym: List[Symbol]

    self.frame = frame
    self.sym = sym

class Access():
  def __init__(self, frame, sym, isLeft, isFirst, labelShortCircuit=(None, None)):
    #frame: Frame
    #sym: List[Symbol]
    #isLeft: Boolean
    #isFirst: Boolean
    #labelShortCircuit: (op, label)

    self.frame = frame
    self.sym = sym
    self.isLeft = isLeft
    self.isFirst = isFirst
    self.labelShortCircuit = labelShortCircuit

class Val(ABC):
  pass

class Index(Val):
  def __init__(self, value):
    #value: Int

    self.value = value

class CName(Val):
  def __init__(self, value):
    #value: String

    self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
  def __init__(self, astTree, env, dir_):
    #astTree: AST
    #env: List[Symbol] built in function from codegenerator
    #dir_: File

    self.astTree = astTree
    self.env = env
    self.className = "MCClass"
    self.path = dir_
    self.emit = Emitter(self.path + "/" + self.className + ".j")
    self.globalArrayVarList = []

  def getDeclType(self, varType):
    return ArrayPointerType(varType.eleType) if type(varType) is ArrayType else varType

  def visitProgram(self, ast, c):
    #ast: Program
    #c: Any
    
    # print(ast)
    self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
    staticDeclList = self.env
    for decl in ast.decl:
      if type(decl) is FuncDecl:
        paramType = [paramTemp.varType for paramTemp in decl.param]
        staticDeclList = [Symbol(decl.name.name, MType(paramType, decl.returnType), CName(self.className))] + staticDeclList
      else:
        varSym = self.visit(decl, (SubBody(None, self.env), "global"))
        staticDeclList = [varSym] + staticDeclList
    env = SubBody(None, staticDeclList)
    self.genMETHOD(FuncDecl(Id("<init>"), list(), None, Block(list())), c, Frame("<init>", VoidType))
    if self.globalArrayVarList:
      self.genMETHOD(FuncDecl(Id("<clinit>"), list(), None, Block(list())), c, Frame("<clinit>", VoidType))
    list(map(lambda func: self.visit(func, env), filter(lambda decl: type(decl) is FuncDecl, ast.decl)))
    self.emit.emitEPILOG()
    return c

  # declaration
  def genMETHOD(self, consdecl, globalEnv, frame):
    #consdecl: FuncDecl
    #globalEnv: Any
    #frame: Frame

    methodName = consdecl.name.name
    isInit = consdecl.returnType is None and methodName == "<init>"
    isClassInit = consdecl.returnType is None and methodName == "<clinit>"
    isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
    returnType = VoidType() if isInit or isClassInit else consdecl.returnType
    inType = [ArrayPointerType(StringType())] if isMain else [self.getDeclType(decl.varType) for decl in consdecl.param]
    mtype = MType(inType, returnType)

    self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

    frame.enterScope(True)

    # Generate code for parameter declarations
    if isInit:
      self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
    if isMain:
      self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
    varList = SubBody(frame, globalEnv)
    for param in consdecl.param:
      varList = self.visit(param, (varList, "parameter"))
      if type(param.varType) is ArrayType:
        name = varList.sym[0].name
        idx = varList.sym[0].value.value
        varType = varList.sym[0].mtype
        self.emit.printout(self.emit.emitVAR(idx, name, varType, frame.getStartLabel(), frame.getEndLabel(), frame))

    self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
    # Generate code for statements
    body = consdecl.body
    if isInit:
      self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
      self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
    if isClassInit:
      for arrayVar in self.globalArrayVarList:
        # emitINITNEWARRAY(self, name, frame, varType, varSize)
        self.emit.printout(self.emit.emitINITNEWARRAY(self.className + "." + arrayVar.variable, frame, arrayVar.varType.eleType, arrayVar.varType.dimen))
    for member in body.member:
      if type(member) is VarDecl:
        varList = self.visit(member, (varList, "local"))
        if type(member.varType) is ArrayType:
          idx = varList.sym[0].value.value
          varType = varList.sym[0].mtype.eleType
          self.emit.printout(self.emit.emitINITNEWARRAY(idx, frame, varType, member.varType.dimen, "local"))
      else:
        self.visit(member, varList)
        if frame.getStackSize() and type(member) is Expr:
          self.emit.printout(self.emit.emitPOP(frame))
          
    self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
    if type(returnType) is VoidType:
      self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
    self.emit.printout(self.emit.emitENDMETHOD(frame))
    frame.exitScope()

  def visitFuncDecl(self, ast, subGlobal):
    subGlobalTemp = subGlobal
    frame = Frame(ast.name.name, ast.returnType)
    self.genMETHOD(ast, subGlobalTemp.sym, frame)

  def visitVarDecl(self, ast, trackSubBody):
    subctxt = trackSubBody[0]
    frame = subctxt.frame
    varName = ast.variable
    varType = ast.varType
    if trackSubBody[1] == "global":
      self.emit.printout(self.emit.emitATTRIBUTE(varName, self.getDeclType(varType), False, ""))
      if type(ast.varType) is ArrayType: 
        self.globalArrayVarList.append(ast)
      return Symbol(varName, varType)
    elif trackSubBody[1] == "parameter": # param
      idx = frame.getNewIndex()
      self.emit.printout(self.emit.emitVAR(idx, varName, self.getDeclType(varType), frame.getStartLabel(), frame.getEndLabel(), frame))
      return SubBody(frame, [Symbol(varName, varType, Index(idx))] + subctxt.sym)      
    else: # local
      idx = frame.getNewIndex()
      localVarLabel = frame.getNewLabel()
      self.emit.printout(self.emit.emitVAR(idx, varName, self.getDeclType(varType), localVarLabel, frame.getEndLabel(), frame))
      self.emit.printout(self.emit.emitLABEL(localVarLabel, frame))
      return SubBody(frame, [Symbol(varName, varType, Index(idx))] + subctxt.sym)

  # statement
  def visitCallExpr(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym
    sym = self.lookup(ast.method.name, symLst, lambda x: x.name)
    cname = sym.value.value
    ctype = sym.mtype

    paramsCode = ""
    for i in range(len(ast.param)):
      paramCode, paramType = self.visit(ast.param[i], Access(frame, symLst, False, True))
      if type(sym.mtype.partype[i]) is FloatType and type(paramType) is IntType:
        paramCode = paramCode + self.emit.emitI2F(frame)
      paramsCode += paramCode
    result = paramsCode + self.emit.emitINVOKESTATIC(cname + "/" + sym.name, ctype, frame)
    if type(ctxt) is SubBody: self.emit.printout(result)
    else: return result, ctype.rettype

  def visitBlock(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym

    frame.enterScope(False)
    self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
    varList = SubBody(frame, symLst)
    # Generate code for statements
    for member in ast.member:
      if type(member) is VarDecl:
        varList = self.visit(member, (varList, "local"))
        if type(member.varType) is ArrayType:
          idx = varList.sym[0].value.value
          varType = varList.sym[0].mtype.eleType
          self.emit.printout(self.emit.emitINITNEWARRAY(idx, frame, varType, member.varType.dimen, "local"))
      else:
        self.visit(member, varList)
        if frame.getStackSize() and type(member) is Expr:
          self.emit.printout(self.emit.emitPOP(frame))
    self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
    frame.exitScope()

  def visitIf(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym

    labelTrue = frame.getNewLabel()
    labelEnd = frame.getNewLabel()
    exprCode, exprType = self.visit(ast.expr, Access(frame, symLst, False, True))

    self.emit.printout(exprCode)
    self.emit.printout(self.emit.emitIFTRUE(labelTrue, frame))
    if ast.elseStmt is not None:
      self.visit(ast.elseStmt, ctxt)
    self.emit.printout(self.emit.emitGOTO(labelEnd, frame))
    self.emit.printout(self.emit.emitLABEL(labelTrue, frame))
    self.visit(ast.thenStmt, ctxt)
    self.emit.printout(self.emit.emitLABEL(labelEnd, frame))

  def visitDowhile(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym
    
    labelStart = frame.getNewLabel()
    labelEnd = frame.getNewLabel()
    expCode, expType = self.visit(ast.exp, Access(frame, symLst, False, True))

    frame.enterLoop()
    self.emit.printout(self.emit.emitLABEL(labelStart, frame))
    list(map(lambda x: self.visit(x, ctxt), ast.sl))
    self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
    self.emit.printout(expCode)
    self.emit.printout(self.emit.emitIFFALSE(labelEnd, frame))
    self.emit.printout(self.emit.emitGOTO(labelStart, frame))
    self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
    self.emit.printout(self.emit.emitLABEL(labelEnd, frame))
    frame.exitLoop()

  def visitFor(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym
    
    labelStart = frame.getNewLabel()
    labelEnd = frame.getNewLabel()
    expr1Code, expr1Type = self.visit(ast.expr1, Access(frame, symLst, False, True))
    expr2Code, expr2Type = self.visit(ast.expr2, Access(frame, symLst, False, True))
    expr3Code, expr3Type = self.visit(ast.expr3, Access(frame, symLst, False, True))

    self.emit.printout(expr1Code)
    self.emit.printout(self.emit.emitPOP(frame))
    frame.enterLoop()
    self.emit.printout(self.emit.emitLABEL(labelStart, frame))
    self.emit.printout(expr2Code)
    self.emit.printout(self.emit.emitIFFALSE(labelEnd, frame))
    self.visit(ast.loop, ctxt)
    self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
    self.emit.printout(expr3Code)
    self.emit.printout(self.emit.emitPOP(frame))
    self.emit.printout(self.emit.emitGOTO(labelStart, frame))
    self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
    self.emit.printout(self.emit.emitLABEL(labelEnd, frame))
    frame.exitLoop()

  def visitBreak(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    self.emit.printout(self.emit.emitGOTO(frame.getBreakLabel(), frame))

  def visitContinue(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    self.emit.printout(self.emit.emitGOTO(frame.getContinueLabel(), frame))

  def visitReturn(self, ast, trackSubBody):
    ctxt = trackSubBody
    frame = ctxt.frame
    symLst = ctxt.sym
    returnType = frame.returnType
    if not type(returnType) is VoidType:
      exprCode, exprType = self.visit(ast.expr, Access(frame, symLst, False, True))
      if type(returnType) is FloatType and type(exprType) is IntType:
        exprCode = exprCode + self.emit.emitI2F(frame)
      self.emit.printout(exprCode)
    self.emit.printout(self.emit.emitRETURN(returnType, frame))

  # expression
  def visitBinaryOp(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    op = ast.op
    symLst = ctxt.sym
    if op in ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=']:
      leftCode, leftType = self.visit(ast.left, Access(frame, symLst, False, False))
      rightCode, rightType = self.visit(ast.right, Access(frame, symLst, False, False))
      returnType = FloatType() if FloatType in [type(leftType), type(rightType)] else IntType()
      if type(leftType) is IntType and type(returnType) != type(leftType): 
        leftCode = leftCode + self.emit.emitI2F(frame)
      if type(rightType) is IntType and type(returnType) != type(rightType): 
        rightCode = rightCode + self.emit.emitI2F(frame)
      if op in ['+', '-', '*', '/', '%']:
        if op in ['+', '-']:
          return leftCode + rightCode + self.emit.emitADDOP(op, returnType, frame), returnType
        elif op in ['*', '/']:
          return leftCode + rightCode + self.emit.emitMULOP(op, returnType, frame), returnType
        elif op == '%':
          return leftCode + rightCode + self.emit.emitMOD(frame), IntType()
      else:
        return leftCode + rightCode + self.emit.emitREOP(op, returnType, frame), BoolType()
    elif op in ['||', '&&']:
      # short-circuit
      preOp = ctxt.labelShortCircuit[0] if type(o) is Access else None
      labelShortCircuit = ctxt.labelShortCircuit[1] if type(o) is Access else None
      if op != preOp:
        labelShortCircuit = frame.getNewLabel()
      leftCode, leftType = self.visit(ast.left, Access(frame, symLst, False, False, (op, labelShortCircuit)))
      rightCode, rightType = self.visit(ast.right, Access(frame, symLst, False, False, (op, labelShortCircuit)))
      if op != preOp:
        if op == '||':
          return leftCode + self.emit.emitDUP(frame) + self.emit.emitIFTRUE(labelShortCircuit, frame) + self.emit.emitPOP(frame) + rightCode + self.emit.emitLABEL(labelShortCircuit, frame), BoolType()
        else:
          return leftCode + self.emit.emitDUP(frame) + self.emit.emitIFFALSE(labelShortCircuit, frame) + self.emit.emitPOP(frame) + rightCode + self.emit.emitLABEL(labelShortCircuit, frame), BoolType()          
      else:
        if op == '||':
          return leftCode + self.emit.emitDUP(frame) + self.emit.emitIFTRUE(labelShortCircuit, frame) + self.emit.emitPOP(frame) + rightCode, BoolType()
        else:
          return leftCode + self.emit.emitDUP(frame) + self.emit.emitIFFALSE(labelShortCircuit, frame) + self.emit.emitPOP(frame) + rightCode, BoolType()
    else:
      rightCode, rightType = self.visit(ast.right, Access(frame, symLst, False, False))
      leftCode, leftType = self.visit(ast.left, Access(frame, symLst, True, False))
      isArrayType = type(leftType) in [ArrayType, ArrayPointerType]
      if isArrayType:
        leftType = leftType.eleType
      if type(leftType) is FloatType and type(rightType) is IntType:
        rightCode = rightCode + self.emit.emitI2F(frame)
      if type(ctxt) is SubBody:
        if isArrayType:
          returnOp = leftCode[0] + rightCode + leftCode[1]
          [frame.push() for i in range(2)]
        else:
          returnOp = rightCode + leftCode
        self.emit.printout(returnOp)
        if isArrayType: [frame.pop() for i in range(2)]
      else:
        if isArrayType:
          returnOp = rightCode
          returnOp += leftCode[0] + rightCode + leftCode[1]
          [frame.push() for i in range(2)] # keep arr for right to assign
        else:
          returnOp = rightCode + self.emit.emitDUP(frame) + leftCode
        returnType = leftType
        return returnOp, returnType

  def visitUnaryOp(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    symLst = ctxt.sym
    op = ast.op
    binaryCode, binaryType = self.visit(ast.body, Access(frame, symLst, False, True))
    if op == '-': return binaryCode + self.emit.emitNEGOP(binaryType, frame), binaryType
    if op == '!': return binaryCode + self.emit.emitNOT(binaryType, frame), binaryType

  def visitId(self, ast, ctxtId):
    ctxt = ctxtId
    frame = ctxt.frame
    symLst = ctxt.sym
    sym = self.lookup(ast.name, symLst, lambda x: x.name)
    varType = self.getDeclType(sym.mtype)
    if type(ctxt) is not SubBody:
      isLeft = ctxt.isLeft
      isFirst = ctxt.isFirst
      if isLeft: frame.push()
      if sym.value is None:
        if isLeft and type(sym.mtype) not in [ArrayType, ArrayPointerType]: returnCode = self.emit.emitPUTSTATIC(self.className + "." + sym.name, varType, frame)
        else: returnCode = self.emit.emitGETSTATIC(self.className + "." + sym.name, varType, frame)
      else:
        if isLeft and type(sym.mtype) not in [ArrayType, ArrayPointerType]: returnCode = self.emit.emitWRITEVAR(sym.name, varType, sym.value.value, frame)
        else: returnCode = self.emit.emitREADVAR(sym.name, varType, sym.value.value, frame)
    else:
      if sym.value is None:
        returnCode = self.emit.emitGETSTATIC(self.className + "." + sym.name, varType, frame)
      else:
        returnCode = self.emit.emitREADVAR(sym.name, varType, sym.value.value, frame)
    return returnCode, sym.mtype

  def visitArrayCell(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    symLst = ctxt.sym
    isLeft = ctxt.isLeft
    isFirst = ctxt.isFirst
    
    arrCode, arrType = self.visit(ast.arr, Access(frame, symLst, True, True))
    idxCode, idxType = self.visit(ast.idx, Access(frame, symLst, False, True))
    if isLeft:
      return [arrCode + idxCode, self.emit.emitASTORE(arrType.eleType, frame)], arrType
    # stack to keep right code if assign in another op
    [frame.push() for i in range(2)]
    return arrCode + idxCode + self.emit.emitALOAD(arrType.eleType, frame), arrType.eleType

  def visitIntLiteral(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    return self.emit.emitPUSHICONST(ast.value, frame), IntType()

  def visitFloatLiteral(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

  def visitBooleanLiteral(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    return self.emit.emitPUSHICONST(str(ast.value), frame), BoolType()

  def visitStringLiteral(self, ast, o):
    ctxt = o
    frame = ctxt.frame
    return self.emit.emitPUSHCONST(ast.value, StringType(), frame), StringType()
