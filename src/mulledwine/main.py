import re
from typing import Generator, Iterator


class Token:
    def __init__(self, *, token: str, tokeniser: "Tokeniser"):
        if not tokeniser.can_tokenise(token=token):
            raise ValueError(f"Invalid Token for Pattern. Token={token} Pattern={tokeniser.pattern}")
        self._tokeniser = tokeniser
        self._token = token

class Tokeniser:
    def __init__(self, *, pattern: str):
        self.pattern = pattern
        self._regex = re.compile(pattern)

    def tokenise(self, *, s: str) -> Generator[Token, None, None]:
        for token in self._regex.finditer(s):
            yield Token(token=token.group(), tokeniser=self)
    
    def can_tokenise(self, *, token: str) -> bool:
        return self._regex.match(token) is not None


class Multiply(Token):
    def __init__(self, *, token: str):
        super().__init__(token=token, tokeniser=Tokeniser(pattern=r"mul(\d+,\d+)"))

    @property
    def l(self) -> int:
        raise NotImplemented
    
    @property
    def r(self) -> int:
        raise NotImplemented

    @property
    def result(self) -> int:
        return self.l * self.r
    

def main(lines: Iterator[str]) -> None:
    pass