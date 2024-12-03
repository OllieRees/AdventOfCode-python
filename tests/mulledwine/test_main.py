from unittest import TestCase

import pytest

from mulledwine.main import Multiply, Token, Tokeniser


class TestTokeniser(TestCase):
    def test_tokenise_no_char_skip(self) -> None:
        next(Tokeniser(pattern=r"\d").tokenise(s="23 45")) == "2"
        next(Tokeniser(pattern=r"\d").tokenise(s="23 45")) == "3"
        next(Tokeniser(pattern=r"\d").tokenise(s="23 45")) == "4"
        next(Tokeniser(pattern=r"\d").tokenise(s="23 45")) == "5"

    def test_tokenise_char_skip(self) -> None:
        assert next(Tokeniser(pattern=r"\d").tokenise(s="h1 :)")).token == "1"

    def test_tokenise_no_valid_token(self) -> None:
        with pytest.raises(ValueError):
            next(Tokeniser(pattern=r"\d").tokenise(s="hi"))

    def test_token_exists_in_string(self) -> None:
        assert Tokeniser(pattern=r"\d").can_tokenise(token="23 tokens")

    def test_token_doesnt_exist_in_string(self) -> None:
        assert not Tokeniser(pattern=r"\d").can_tokenise(token="twenty-three tokens")

    def test_no_token_given(self) -> None:
        assert not Tokeniser(pattern=r"\d").can_tokenise(token="")


class TestToken(TestCase):
    def test_valid_token(self) -> None:
        assert Token(token="2", tokeniser=Tokeniser(pattern=r"\d"))

    def test_invalid_token(self) -> None:
        with pytest.raises(ValueError):
            Token(token="hi", tokeniser=Tokeniser(pattern=r"\d"))


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