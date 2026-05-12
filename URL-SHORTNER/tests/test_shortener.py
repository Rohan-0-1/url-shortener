import pytest

import shortener as sh


@pytest.fixture(autouse=True)
def reset_store():
    """Clear the store before every test to ensure isolation."""
    sh.clear()
    yield
    sh.clear()


class TestGenerateCode:
    def test_returns_six_characters(self):
        code = sh.generate_code("https://example.com")
        assert len(code) == 6

    def test_same_url_gives_same_code(self):
        url = "https://example.com"
        assert sh.generate_code(url) == sh.generate_code(url)

    def test_different_urls_give_different_codes(self):
        code1 = sh.generate_code("https://example.com")
        code2 = sh.generate_code("https://google.com")
        assert code1 != code2

    def test_code_is_lowercase_hex(self):
        code = sh.generate_code("https://example.com")
        assert all(c in "0123456789abcdef" for c in code)

    def test_trailing_slash_url_differs_from_without(self):
        code1 = sh.generate_code("https://example.com")
        code2 = sh.generate_code("https://example.com/")
        assert code1 != code2


class TestShorten:
    def test_returns_a_code(self):
        code = sh.shorten("https://example.com")
        assert code is not None
        assert len(code) == 6

    def test_code_matches_generate_code(self):
        url = "https://example.com"
        assert sh.shorten(url) == sh.generate_code(url)

    def test_shortening_same_url_twice_returns_same_code(self):
        url = "https://example.com"
        assert sh.shorten(url) == sh.shorten(url)

    def test_stores_the_url(self):
        url = "https://example.com"
        code = sh.shorten(url)
        assert sh.resolve(code) == url


class TestResolve:
    def test_returns_none_for_unknown_code(self):
        assert sh.resolve("xxxxxx") is None

    def test_returns_correct_url_after_storing(self):
        url = "https://openai.com"
        code = sh.shorten(url)
        assert sh.resolve(code) == url

    def test_resolve_is_isolated_between_tests(self):
        # store is cleared by autouse fixture — nothing should persist
        assert sh.resolve("abc123") is None

    def test_multiple_urls_resolve_independently(self):
        url1 = "https://github.com"
        url2 = "https://gitlab.com"
        code1 = sh.shorten(url1)
        code2 = sh.shorten(url2)
        assert sh.resolve(code1) == url1
        assert sh.resolve(code2) == url2
