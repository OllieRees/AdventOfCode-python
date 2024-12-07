import re
from enum import StrEnum
from functools import cached_property
from typing import Generator, Iterator, Optional

from paprika import catch


class TokenType(StrEnum):
    MUL = r"mul\((\d+),(\d+)\)"
    DO = r"do\(\)"
    DONT = r"don't\(\)"  

    @classmethod
    @catch(exception=StopIteration, handler=lambda _: None)
    def from_token_str(cls, *, token: str) -> Optional["TokenType"]:
        return next(type for type in cls if type.is_valid_token(token=token))
    
    @classmethod
    def tokenise_all(cls, *, token_str: str) -> Generator["Token", None, None]:
        return Tokeniser(token_str=token_str, pattern=re.compile("|".join(r for r in cls))).tokenise()
    
    def tokenise(self, *, token_str: str) -> Generator["Token", None, None]:
        return Tokeniser(token_str=token_str, pattern=re.compile(self)).tokenise()
        
    def is_valid_token(self, *, token: str) -> bool:
        return re.compile(self).fullmatch(token) is not None


class Tokeniser:
    def __init__(self, token_str: str, pattern: re.Pattern[str]) -> None:
        self.token_str = token_str
        self.pattern = pattern
    
    def tokenise(self) -> Generator["Token", None, None]:
        for token in self.pattern.finditer(self.token_str):
            if type := TokenType.from_token_str(token=token.group()):
                yield Token(token=token.group(), type=type)
        return None


class Token:
    def __init__(self, *, token: str, type: TokenType):
        if not type.is_valid_token(token=token):
            raise ValueError(f"Invalid Token for Pattern. Token={token} Pattern={type}")
        self.type = type
        self.token = token

    @property
    def args(self) -> Iterator[str]:
        return iter(next(re.compile(self.type).finditer(self.token)).groups())
    

class Multiply(Token):
    type = TokenType.MUL

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type)
        self.l = next(self._args)
        self.r = next(self._args)

    def __str__(self) -> str:
        return f"{self.l} * {self.r}"

    @cached_property 
    def _args(self) -> Generator[int, None, None]:
        for i, arg in enumerate(self.args):
            if i >= 2:
                raise ValueError(f"Token needs comma separated digits: Token={self.token}")
            yield int(arg)
        raise ValueError(f"Token needs comma separated digits: Token={self.token}")

    @property
    def result(self) -> int:
        return self.l * self.r
    
    @classmethod
    def tokenise(cls, *, token_str: str) -> Generator["Multiply", None, None]:
        for token in cls.type.tokenise(token_str=token_str):
            yield Multiply(token=token.token)


class Do(Token):
    type = TokenType.DO

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type)
        
    def __str__(self) -> str:
        return "do"


class Dont(Token):
    type = TokenType.DONT

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type)
        
    def __str__(self) -> str:
        return "don't"


def main(lines: Iterator[str]) -> None:
    tokens = [token for line in lines for token in TokenType.tokenise_all(token_str=line)]
    print(f"Token Sum: {sum(Multiply(token=token.token).result for token in tokens if token.type == TokenType.MUL)}")

    # skip any muls between a don't and a do