from unittest import TestCase

import pytest

from mulledwine.main import Multiply, Token, TokenType


class TestTokenType(TestCase):
    def test_token_type_from_str(self) -> None:
        assert TokenType.from_token_str(token="mul(2,3)") == TokenType.MUL
        assert TokenType.from_token_str(token="do()") == TokenType.DO
        assert TokenType.from_token_str(token="don't()") == TokenType.DONT

    def test_token_type_from_invalid_str(self) -> None:
        with pytest.raises(ValueError):
            TokenType.from_token_str(token="do")

    def test_valid_token(self) -> None:
        assert TokenType.MUL.is_valid_token(token="mul(2,3)")
        assert TokenType.DO.is_valid_token(token="do()")
        assert TokenType.DONT.is_valid_token(token="don't()")

    def test_valid_token_for_wrong_type(self) -> None:
        assert not TokenType.MUL.is_valid_token(token="do()")
        assert not TokenType.MUL.is_valid_token(token="don't()")
        assert not TokenType.DO.is_valid_token(token="mul(2,3)")
        assert not TokenType.DO.is_valid_token(token="don't()")
        assert not TokenType.DONT.is_valid_token(token="mul(2,3)")
        assert not TokenType.DONT.is_valid_token(token="do()")

    def test_valid_token_bad_str(self) -> None:
        assert not TokenType.MUL.is_valid_token(token="hi team :)")
        assert not TokenType.DO.is_valid_token(token="hi team :)")
        assert not TokenType.DONT.is_valid_token(token="hi team :)")

    def test_mul_is_enabled(self) -> None:
        assert TokenType.MUL.is_enabled(is_enabled=True)
        assert not TokenType.MUL.is_enabled(is_enabled=False)

    def test_enabling_tokens_is_enabled(self) -> None:
        assert TokenType.DO.is_enabled(is_enabled=True)
        assert TokenType.DO.is_enabled(is_enabled=False)
        assert not TokenType.DONT.is_enabled(is_enabled=True)
        assert not TokenType.DONT.is_enabled(is_enabled=False)

    def test_tokenise_all(self) -> None:
        token_str = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        tokens: list[str] = [str(token) for token in TokenType.tokenise_all(token_str=token_str)]
        assert tokens == [
            "Token <token=mul(2,4) type=MUL>",
            "Token <token=don't() type=DONT>",
            "Token <token=mul(5,5) type=MUL>",
            "Token <token=mul(11,8) type=MUL>",
            "Token <token=do() type=DO>",
            "Token <token=mul(8,5) type=MUL>",
        ]


class TestToken(TestCase):
    def test_valid_token(self) -> None:
        assert Token(token="mul(2,3)", type=TokenType.MUL)

    def test_invalid_token(self) -> None:
        with pytest.raises(ValueError):
            Token(token="hi", type=TokenType.MUL)

    def test_result(self) -> None:
        assert Token(token="mul(2,3)", type=TokenType.MUL).result == 6
        assert Token(token="do()", type=TokenType.DO).result == 0
        assert Token(token="don't()", type=TokenType.DONT).result == 0


class TestMultiply(TestCase):
    def test_two_int_operands(self) -> None:
        str(Multiply(token="mul(2,3)")) == "2 * 3"

    def test_one_int_operand(self) -> None:
        with pytest.raises(ValueError):
            Multiply(token="mul(2)")

    def test_three_int_operands(self) -> None:
        with pytest.raises(ValueError):
            Multiply(token="mul(2,3,4)")

    def test_space_after_comma(self) -> None:
        with pytest.raises(ValueError):
            Multiply(token="mul(2, 3)")

    def test_two_str_operands(self) -> None:
        with pytest.raises(ValueError):
            Multiply(token="mul(two, three)")

    def test_result(self) -> None:
        assert Multiply(token="mul(2,3)").result == 6
