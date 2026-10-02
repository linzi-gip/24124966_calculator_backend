# -*- coding: utf-8 -*-
"""
calculator.py - 数学表达式解析与计算模块
========================================
作业要求：计算必须由后端完成，禁止使用 eval / exec 等危险执行函数。
本模块采用递归下降解析（Recursive Descent Parsing）实现表达式求值，
支持：
  - 四则运算 + - * /
  - 运算符优先级（* / 高于 + -）
  - 括号 ( )
  - 一元正负号，如 -5、3 * -2
  - 小数，如 0.1 + 0.2
  - 非法表达式检测（多余运算符、括号不匹配、非法字符等）
  - 除零检测

语法定义（简化版）：
  expression := term { ('+' | '-') term }
  term       := factor { ('*' | '/') factor }
  factor     := ('+' | '-') factor | primary
  primary    := NUMBER | '(' expression ')'
"""

import re


class ExpressionError(ValueError):
    """表达式非法时抛出的异常。"""
    pass


# ---------------------------------------------------------------------------
# 词法分析：把表达式字符串拆成 token 列表
# ---------------------------------------------------------------------------
def tokenize(expression):
    tokens = []
    i = 0
    length = len(expression)
    while i < length:
        ch = expression[i]
        if ch.isspace():                 # 跳过空白
            i += 1
            continue
        if ch.isdigit() or ch == '.':    # 数字（含小数）
            j = i
            while j < length and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            number_text = expression[i:j]
            # 拒绝 "1.2.3" 这种多个小数点的写法
            if number_text.count('.') > 1:
                raise ExpressionError("Invalid expression")
            # 拒绝孤零零的一个 "."，如 "1 + ."
            if number_text == '.':
                raise ExpressionError("Invalid expression")
            try:
                tokens.append(('NUM', float(number_text)))
            except ValueError:
                raise ExpressionError("Invalid expression")
            i = j
            continue
        if ch in '+-*/()':               # 运算符和括号
            tokens.append((ch, ch))
            i += 1
            continue
        # 出现其他字符（字母、汉字、= 等）一律视为非法表达式
        raise ExpressionError("Invalid expression")
    return tokens


# ---------------------------------------------------------------------------
# 语法分析：递归下降求值
# ---------------------------------------------------------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """查看当前 token（不移动位置）。"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        """取出当前 token 并移动位置。"""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse_expression(self):
        """expression := term { ('+' | '-') term }"""
        value = self.parse_term()
        while True:
            token = self.peek()
            if token is not None and token[0] in ('+', '-'):
                op = self.advance()[0]
                right = self.parse_term()
                if op == '+':
                    value = value + right
                else:
                    value = value - right
            else:
                break
        return value

    def parse_term(self):
        """term := factor { ('*' | '/') factor }"""
        value = self.parse_factor()
        while True:
            token = self.peek()
            if token is not None and token[0] in ('*', '/'):
                op = self.advance()[0]
                right = self.parse_factor()
                if op == '*':
                    value = value * right
                else:
                    if right == 0:
                        raise ZeroDivisionError("Division by zero")
                    value = value / right
            else:
                break
        return value

    def parse_factor(self):
        """factor := ('+' | '-') factor | primary，处理一元正负号"""
        token = self.peek()
        if token is not None and token[0] in ('+', '-'):
            op = self.advance()[0]
            value = self.parse_factor()
            return value if op == '+' else -value
        return self.parse_primary()

    def parse_primary(self):
        """primary := NUMBER | '(' expression ')'"""
        token = self.peek()
        if token is None:
            raise ExpressionError("Invalid expression")
        if token[0] == 'NUM':
            self.advance()
            return token[1]
        if token[0] == '(':
            self.advance()                    # 吃掉 '('
            value = self.parse_expression()
            # 必须紧跟一个 ')'，否则括号不匹配
            if self.peek() is None or self.advance()[0] != ')':
                raise ExpressionError("Invalid expression")
            return value
        # 出现 '+ - * /' 或 ')' 等不该在数字位置出现的东西
        raise ExpressionError("Invalid expression")


# ---------------------------------------------------------------------------
# 结果整理：避免浮点误差，如 0.1 + 0.2 = 0.30000000000000004
# ---------------------------------------------------------------------------
def clean_result(value):
    """整数结果返回 int，浮点结果最多保留 10 位小数。"""
    if abs(value - round(value)) < 1e-10:
        return int(round(value))
    return round(value, 10)


# ---------------------------------------------------------------------------
# 对外入口
# ---------------------------------------------------------------------------
def evaluate_expression(expression):
    """
    计算一个数学表达式，返回数值结果。

    参数:
        expression: 字符串，如 "(1+2)*3"、"-5+8"、"3*-2"、"0.1+0.2"

    返回:
        计算结果（int 或 float）

    异常:
        ExpressionError: 表达式非法
        ZeroDivisionError: 除零
    """
    if not isinstance(expression, str):
        raise ExpressionError("Invalid expression")
    expression = expression.strip()
    if not expression:
        raise ExpressionError("Invalid expression")
    # 预先过滤非法字符（白名单校验）
    if not re.fullmatch(r'[0-9+\-*/().\s]+', expression):
        raise ExpressionError("Invalid expression")
    tokens = tokenize(expression)
    if not tokens:
        raise ExpressionError("Invalid expression")
    parser = Parser(tokens)
    result = parser.parse_expression()
    # 解析完必须刚好消耗完所有 token，否则说明表达式尾部还有多余内容
    if parser.pos != len(parser.tokens):
        raise ExpressionError("Invalid expression")
    return clean_result(result)
