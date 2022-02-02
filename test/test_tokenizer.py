import pytest

from src.language.tokenizer import Tokenizer


def test_1():
    case1 = "number a = 3.34"

    tokens = Tokenizer()(case1)

    assert len(tokens) == 4

    assert tokens[3].lexeme == "3.34"

def test_2():
    case2 = "function number fibo(number n) -> {\nif n lte 1 -> {\n return 1 \n} return fibo(n- 1) + fibo(n - 2)}"
    
    tokens = Tokenizer()(case2)
    
    assert len(tokens) == 36

