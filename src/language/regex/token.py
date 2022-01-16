
class Token:
    __name__ = ""

    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value
    
    def __str__(self) -> str:
        return f"T_{self.name}('{self.value}')"
