import re
from enum import StrEnum
from typing import Generator, Iterator


class TokenType(StrEnum):
    MUL = r"mul\((\d+),(\d+)\)"
    DO = r"do\(\)"
    DONT = r"dont\(\)"

    @classmethod
    def global_regex(cls) -> re.Pattern[str]:
        return re.compile("|".join(r for r in cls))
    
    @property
    def _regex(self) -> re.Pattern[str]:
        return re.compile(self)
    

class Tokeniser:
    def __init__(self, *, s: str, type: TokenType):
        self.s = s
        self.type = type

    def capture(self) -> Generator[re.Match[str], None, None]:
        for match in self.type._regex.finditer(self.s):
            yield match
        return None

    def tokenise(self) -> Generator["Token", None, None]:
        for token in self.capture():
            yield Token(token=token.group(), type=self.type)
    
    def can_tokenise(self) -> bool:
        return self.type._regex.match(self.s) is not None


class Token:
    def __init__(self, *, token: str, type: TokenType):
        self._tokeniser = Tokeniser(s=token, type=type)
        if not self._tokeniser.can_tokenise():
            raise ValueError(f"Invalid Token for Pattern. Token={token} Pattern={type}")
        self.type = type
        self.token = token


class Multiply(Token):
    type = TokenType.MUL

    def __init__(self, *, token: str):
        super().__init__(token=token, type=self.type)
        self._capture = next(self._tokeniser.capture())
        if len(self._capture.groups()) != 2:
            raise ValueError(f"Token needs comma separated digits: Token={token}")
        
    def __str__(self) -> str:
        return f"{self.l} * {self.r}"
    
    @property 
    def l(self) -> int:
        return int(self._capture.group(1))
    
    @property 
    def r(self) -> int:
        return int(self._capture.group(2))
    
    @property
    def result(self) -> int:
        return self.l * self.r
    
    @classmethod
    def tokenise(cls, s: str) -> Generator["Multiply", None, None]:
        for token in Tokeniser(s=s, type=cls.type).tokenise():
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
    tokens = [token for line in lines for token in Multiply.tokenise(line)]
    print(f"Token Sum: {sum(token.result for token in tokens)}")
