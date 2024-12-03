import re
from typing import Generator, Iterator


class Token:
    def __init__(self, *, token: str, tokeniser: "Tokeniser"):
        if not tokeniser.can_tokenise(token=token):
            raise ValueError(f"Invalid Token for Pattern. Token={token} Pattern={tokeniser.pattern}")
        self._tokeniser = tokeniser
        self.token = token

class Tokeniser:
    def __init__(self, *, pattern: str):
        self.pattern = pattern
        self._regex = re.compile(pattern)

    def capture(self, s: str) -> Generator[re.Match[str], None, None]:
        for match in self._regex.finditer(s):
            yield match

    def tokenise(self, s: str) -> Generator[Token, None, None]:
        for token in self._regex.finditer(s):
            yield Token(token=token.group(), tokeniser=self)
    
    def can_tokenise(self, *, token: str) -> bool:
        return self._regex.match(token) is not None


class Multiply(Token):
    tokeniser = Tokeniser(pattern=r"mul\((\d+),(\d+)\)")

    def __init__(self, *, token: str):
        super().__init__(token=token, tokeniser=self.tokeniser)
        self._capture = next(self._tokeniser.capture(token))
        if len(self._capture.groups()) != 2:
            raise ValueError(f"Token needs comma separated digits: Token={token}")
        
    @property 
    def l(self) -> int:
        return int(self._capture.group(1))
    
    @property 
    def r(self) -> int:
        return int(self._capture.group(2))
    
    @property
    def result(self) -> int:
        return self.l * self.r
    
    def __str__(self) -> str:
        return f"{self.l} * {self.r}"

def main(lines: Iterator[str]) -> None:
    tokens = [Multiply(token=token.token) for line in lines for token in Multiply.tokeniser.tokenise(line)]
    print(f"Token Sum: {sum(token.result for token in tokens)}")
