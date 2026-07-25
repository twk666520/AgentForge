"""Tests for all tool functions."""
from __future__ import annotations
from dev_toolkit_skill import tools


class TestJsonTools:
    def test_format(self):
        r = tools.json_format('{"a":1,"b":2}')
        assert r["valid"] is True
        assert "  " in r["output"]

    def test_validate_valid(self):
        r = tools.json_validate('{"a": 1}')
        assert r["valid"] is True

    def test_validate_invalid(self):
        r = tools.json_validate("{bad}")
        assert r["valid"] is False

    def test_minify(self):
        r = tools.json_minify('{"a": 1, "b": 2}')
        assert " " not in r["output"]


class TestBase64Tools:
    def test_encode_decode_roundtrip(self):
        r1 = tools.base64_encode("hello")
        r2 = tools.base64_decode(r1["output"])
        assert r2["output"] == "hello"


class TestJWT:
    def test_decode(self):
        import base64 as b64
        h = b64.urlsafe_b64encode(b'{"alg":"HS256"}').rstrip(b"=").decode()
        p = b64.urlsafe_b64encode(b'{"sub":"123"}').rstrip(b"=").decode()
        token = f"{h}.{p}.sig"
        r = tools.jwt_decode(token)
        assert "HS256" in r["output"]


class TestUUID:
    def test_generate_v4(self):
        r = tools.uuid_generate()
        assert len(r["output"]) == 36


class TestHash:
    def test_md5(self):
        r = tools.hash_text("hello", algorithm="md5")
        assert r["output"] == "5d41402abc4b2a76b9719d911017c592"


class TestRegex:
    def test_match(self):
        r = tools.regex_test(r"\d+", "abc123def456")
        assert r["metadata"]["matches"] == 2

    def test_no_match(self):
        r = tools.regex_test(r"\d+", "abc")
        assert r["output"] == "No matches"


class TestMarkdownTable:
    def test_basic(self):
        r = tools.markdown_table(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
        assert "|Name|Age|" in r["output"]
        assert "|Alice|30|" in r["output"]