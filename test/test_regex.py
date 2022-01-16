from src.language.regex import compile, match

char_re = {
    "a": [("a", True), ("b", False), ("aa", False), ("", False)],
    }

def test_char():
    for _ in char_re.keys():
        case = char_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]

alt_re = {
    "a|b": [("b", True), ("a", True), ("ab", False), ("aaa", False), ("", False)], 
    "a|b|c": [("b", True), ("a", True), ("c", True), ("ab", False), ("ac", False), ('bc', False), ("", False), ("abc", False), ("cc", False), ("ca", False)]
}
def test_alt():
    for _ in alt_re.keys():
        case = alt_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]

concat_re = {
    "ab": [("a", False), ("b", False), ("ab", True), ("abab", False), ("ba", False), ("", False)],
    "abc": [("a", False), ("b", False), ("c", False), ("ab", False), ("bc", False), ("abc", True), ("abcabc", False), ("cba", False)]
}
def test_concat():
    for _ in concat_re.keys():
        case = concat_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]

plus_re = {
    "a+": [("a", True), ("aa", True), ("a"*100, True), ("", False), ("ab", False)],
    "ba+": [("baba", False), ("ba", True), ("baa", True), ("baaaab", False)],
    "(ba)+": [("baa", False), ("baba", True)]
}
def test_plus():
    for _ in plus_re.keys():
        case = plus_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]

qmark_re = {
    "a?": [("a", True), ("", True), ("aa", False), ("b", False)]
}
def test_qmark():
    for _ in qmark_re.keys():
        case = qmark_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]

star_re = {
    "a*": [("", True), ("a", True), ("a" * 10, True), ("a"*10 + "b", False)]
}
def test_star():
    for _ in star_re.keys():
        case = star_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]


mix_re = {
    "ab+c": [('ab', False), ("bbbc", False), ("abc", True), ("abbbbbbc", True), ("", False)], 
    " a": [("a", False), (" ", False), (" a", True)],
    "a∗(baa∗)∗(b?)": [("bab", True), ("aba", True), ("baabaaaaaab", True), ("bb", False)],
    "b.a": [("aa", False), ("b.a", True), ("bba", True), ("ba", False)],
    "\++": [("", False), ("+", True), ("\+", False), ("\++", False), ("+"*10, True), ]
}
def test_mix():
    for _ in star_re.keys():
        case = star_re[_]
        for c in case:
            result = match(_, c[0])
            assert result == c[1]
