import re
from enum import StrEnum
from functools import cached_property
from typing import Generator, Iterator, Optional


class TokenType(StrEnum):
    MUL = r"mul\((\d+),(\d+)\)"
    DO = r"do\(\)"
    DONT = r"don't\(\)"  

    @classmethod
    def from_token_str(cls, *, token: str) -> Optional["TokenType"]:
        try:
            return next(type for type in cls if type.is_valid_token(token=token))
        except StopIteration as no_type_found_err:
            raise ValueError(f"No token type found for {token}") from no_type_found_err
        
    @classmethod
    def tokenise_all(cls, *, token_str: str) -> Iterator["Token"]:
        return Tokeniser(token_str=token_str, pattern=re.compile("|".join(r for r in cls))).tokenise()
    
    def tokenise(self, *, token_str: str) -> Iterator["Token"]:
        return Tokeniser(token_str=token_str, pattern=re.compile(self)).tokenise()
        
    def is_valid_token(self, *, token: str) -> bool:
        return re.compile(self).fullmatch(token) is not None
    
    def is_enabled(self, *, is_enabled: bool) -> bool:
        match self:
            case TokenType.MUL:
                return is_enabled
            case TokenType.DONT:
                return False
            case _:
                return True
            
    def __str__(self) -> str:
        return self.name


class Tokeniser:
    def __init__(self, token_str: str, pattern: re.Pattern[str]) -> None:
        self.token_str = token_str
        self.pattern = pattern
    
    def tokenise(self) -> Iterator["Token"]:
        rv = []
        is_enabled = True
        for token in self.pattern.finditer(self.token_str):
            if type := TokenType.from_token_str(token=token.group()):
                is_enabled = type.is_enabled(is_enabled=is_enabled)
                rv.append(Token(token=token.group(), type=type, is_enabled=is_enabled))
        return iter(rv)
    

class Token:
    def __init__(self, *, token: str, type: TokenType, is_enabled: bool = True):
        if not type.is_valid_token(token=token):
            raise ValueError(f"Invalid Token for Pattern. Token={token} Pattern={type}")
        self.type = type
        self.token = token
        self.is_enabled = is_enabled

    @property
    def args(self) -> Iterator[str]:
        return iter(next(re.compile(self.type).finditer(self.token)).groups())
    
    @property
    def result(self) -> int:
        match self.type:
            case TokenType.MUL:
                return Multiply(token=self.token, is_enabled=self.is_enabled).result
        return 0
    
    def __str__(self):
        return f"Token <token={self.token} type={self.type}>" 

class Multiply(Token):
    type = TokenType.MUL

    def __init__(self, *, token: str, is_enabled: bool = True):
        super().__init__(token=token, type=self.type, is_enabled=is_enabled)
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


class Do(Token):
    type = TokenType.DO

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type, is_enabled=True)
        
    def __str__(self) -> str:
        return "do"


class Dont(Token):
    type = TokenType.DONT

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type, is_enabled=False)
        
    def __str__(self) -> str:
        return "don't"


def main(lines: Iterator[str]) -> None:
    tokens = [token for token in TokenType.tokenise_all(token_str="".join(lines))]
    print(f"Token Sum: {sum(token.result for token in tokens)}")
    print(f"Enabled Tokens Sum: {sum(token.result for token in tokens if token.is_enabled)}")