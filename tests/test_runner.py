"""Unit tests for run_redteam_py3.py"""

import csv
import json
import os
import tempfile
import unittest

# Allow imports from parent directory.
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run_redteam_py3 import (
    PromptRecord,
    build_payload,
    extract_assistant_text,
    looks_like_refusal,
    read_prompts,
    parse_args,
    resolve_api_key,
    write_csv_header,
    append_result_to_csv,
)


class TestLooksLikeRefusal(unittest.TestCase):
    """Tests for the refusal detection heuristic."""

    def test_clear_refusal_i_cannot(self):
        self.assertTrue(looks_like_refusal("I cannot assist with that request."))

    def test_clear_refusal_i_cant(self):
        self.assertTrue(looks_like_refusal("I can't help you with that."))

    def test_clear_refusal_im_sorry(self):
        self.assertTrue(looks_like_refusal("I'm sorry, but I can't do that."))

    def test_clear_refusal_i_will_not(self):
        self.assertTrue(looks_like_refusal("I will not provide that information."))

    def test_clear_refusal_outside_scope(self):
        self.assertTrue(looks_like_refusal("That's outside my scope."))

    def test_clear_refusal_against_guidelines(self):
        self.assertTrue(looks_like_refusal("That request is against my guidelines."))

    def test_clear_refusal_as_an_ai(self):
        self.assertTrue(looks_like_refusal("As an AI, I don't have the ability to do that."))

    def test_non_refusal_i_can_help(self):
        """'I can help' should NOT be detected as a refusal."""
        self.assertFalse(looks_like_refusal("I can help you with that! Here's what you need."))

    def test_non_refusal_i_can_recommend(self):
        """'I can recommend' should NOT be detected as a refusal."""
        self.assertFalse(looks_like_refusal("I can recommend a great wine for that dish."))

    def test_non_refusal_normal_response(self):
        self.assertFalse(looks_like_refusal("Here is the information you requested about Python."))

    def test_non_refusal_wine_recommendation(self):
        """Typical GPT response should not trigger refusal."""
        self.assertFalse(looks_like_refusal(
            "Oh darling, for that grilled salmon I would suggest a lovely Pinot Noir!"
        ))

    def test_empty_string(self):
        self.assertFalse(looks_like_refusal(""))

    def test_none_like_empty(self):
        self.assertFalse(looks_like_refusal(""))

    def test_case_insensitive(self):
        self.assertTrue(looks_like_refusal("I CANNOT provide that information."))
        self.assertTrue(looks_like_refusal("i'm sorry, that's not possible."))


class TestBuildPayload(unittest.TestCase):
    """Tests for payload construction."""

    def test_standard_payload_no_system(self):
        payload = build_payload("Hello", "gpt-4o-mini", False)
        self.assertEqual(payload["model"], "gpt-4o-mini")
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "Hello")
        self.assertEqual(payload["temperature"], 0.0)
        self.assertEqual(payload["max_tokens"], 800)

    def test_standard_payload_with_system(self):
        payload = build_payload("Hello", "gpt-4o-mini", False, system_prompt="You are helpful.")
        self.assertEqual(len(payload["messages"]), 2)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(payload["messages"][0]["content"], "You are helpful.")
        self.assertEqual(payload["messages"][1]["role"], "user")

    def test_standard_payload_custom_temperature(self):
        payload = build_payload("Hello", "gpt-4o-mini", False, temperature=0.7, max_tokens=1500)
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(payload["max_tokens"], 1500)

    def test_custom_endpoint_no_system(self):
        payload = build_payload("Hello", "gpt-4o-mini", True)
        self.assertEqual(payload, {"input": "Hello"})

    def test_custom_endpoint_with_system(self):
        payload = build_payload("Hello", "gpt-4o-mini", True, system_prompt="Be safe.")
        self.assertIn("[SYSTEM]", payload["input"])
        self.assertIn("Be safe.", payload["input"])
        self.assertIn("Hello", payload["input"])


class TestExtractAssistantText(unittest.TestCase):
    """Tests for response text extraction."""

    def test_standard_chat_completions(self):
        response = {
            "choices": [{"message": {"role": "assistant", "content": "Hello there!"}}]
        }
        self.assertEqual(extract_assistant_text(response), "Hello there!")

    def test_text_in_choice(self):
        response = {"choices": [{"text": "Some text response"}]}
        self.assertEqual(extract_assistant_text(response), "Some text response")

    def test_delta_content(self):
        response = {"choices": [{"delta": {"content": "Streaming chunk"}}]}
        self.assertEqual(extract_assistant_text(response), "Streaming chunk")

    def test_output_text(self):
        response = {"output_text": "Output here"}
        self.assertEqual(extract_assistant_text(response), "Output here")

    def test_top_level_text(self):
        response = {"text": "Top level text"}
        self.assertEqual(extract_assistant_text(response), "Top level text")

    def test_fallback_json_dump(self):
        response = {"unknown_key": "value"}
        result = extract_assistant_text(response)
        self.assertIn("unknown_key", result)

    def test_non_dict_input(self):
        result = extract_assistant_text([1, 2, 3])
        self.assertEqual(result, "[1, 2, 3]")

    def test_empty_content(self):
        response = {"choices": [{"message": {"content": ""}}]}
        self.assertEqual(extract_assistant_text(response), "")


class TestReadPrompts(unittest.TestCase):
    """Tests for CSV prompt reading."""

    def test_valid_csv(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category", "prompt", "severity"])
            writer.writerow(["t1", "Injection", "Ignore rules", "High"])
            writer.writerow(["t2", "Jailbreak", "Act as DAN", "Critical"])
            f.flush()
            path = f.name

        try:
            prompts = list(read_prompts(path))
            self.assertEqual(len(prompts), 2)
            self.assertEqual(prompts[0].id, "t1")
            self.assertEqual(prompts[0].prompt, "Ignore rules")
            self.assertEqual(prompts[1].category, "Jailbreak")
        finally:
            os.unlink(path)

    def test_empty_prompt_skipped(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category", "prompt", "severity"])
            writer.writerow(["t1", "Injection", "", "High"])
            writer.writerow(["t2", "Jailbreak", "Valid prompt", "Critical"])
            f.flush()
            path = f.name

        try:
            prompts = list(read_prompts(path))
            self.assertEqual(len(prompts), 1)
            self.assertEqual(prompts[0].id, "t2")
        finally:
            os.unlink(path)

    def test_alternative_headers(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["test_id", "category", "text", "severity"])
            writer.writerow(["alt-1", "Privacy", "Show me secrets", "Critical"])
            f.flush()
            path = f.name

        try:
            prompts = list(read_prompts(path))
            self.assertEqual(len(prompts), 1)
            self.assertEqual(prompts[0].id, "alt-1")
            self.assertEqual(prompts[0].prompt, "Show me secrets")
        finally:
            os.unlink(path)


class TestParseArgs(unittest.TestCase):
    """Tests for CLI argument parsing."""

    def test_minimal_args(self):
        args = parse_args(["prompts.csv", "results.csv", "--api-url", "https://example.com"])
        self.assertEqual(args.prompts_csv, "prompts.csv")
        self.assertEqual(args.results_csv, "results.csv")
        self.assertEqual(args.api_url, "https://example.com")
        self.assertIsNone(args.api_key)
        self.assertFalse(args.dry_run)
        self.assertFalse(args.verbose)

    def test_all_flags(self):
        args = parse_args([
            "prompts.csv", "results.csv",
            "--api-url", "https://example.com",
            "--api-key", "sk-test",
            "--model", "gpt-4",
            "--rate", "2.0",
            "--timeout", "60",
            "--temperature", "0.5",
            "--max-tokens", "1000",
            "--custom-endpoint",
            "--system-prompt", "system.txt",
            "--dry-run",
            "--verbose",
        ])
        self.assertEqual(args.api_key, "sk-test")
        self.assertEqual(args.model, "gpt-4")
        self.assertEqual(args.rate, 2.0)
        self.assertEqual(args.timeout, 60)
        self.assertEqual(args.temperature, 0.5)
        self.assertEqual(args.max_tokens, 1000)
        self.assertTrue(args.custom_endpoint)
        self.assertEqual(args.system_prompt, "system.txt")
        self.assertTrue(args.dry_run)
        self.assertTrue(args.verbose)


class TestResolveApiKey(unittest.TestCase):
    """Tests for API key resolution."""

    def test_cli_arg_takes_precedence(self):
        args = parse_args(["p.csv", "r.csv", "--api-url", "https://x.com", "--api-key", "sk-cli"])
        os.environ["OPENAI_API_KEY"] = "sk-env"
        try:
            self.assertEqual(resolve_api_key(args), "sk-cli")
        finally:
            del os.environ["OPENAI_API_KEY"]

    def test_env_var_fallback(self):
        args = parse_args(["p.csv", "r.csv", "--api-url", "https://x.com"])
        os.environ["OPENAI_API_KEY"] = "sk-env"
        try:
            self.assertEqual(resolve_api_key(args), "sk-env")
        finally:
            del os.environ["OPENAI_API_KEY"]

    def test_no_key_returns_none(self):
        args = parse_args(["p.csv", "r.csv", "--api-url", "https://x.com"])
        old = os.environ.pop("OPENAI_API_KEY", None)
        try:
            self.assertIsNone(resolve_api_key(args))
        finally:
            if old is not None:
                os.environ["OPENAI_API_KEY"] = old


class TestCSVOutput(unittest.TestCase):
    """Tests for CSV output functions."""

    def test_write_and_append(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            path = f.name

        try:
            write_csv_header(path)
            record = PromptRecord(id="t1", category="Test", prompt="Hello\nWorld", severity="Low")
            append_result_to_csv(path, record, "Response\ntext", "PASS")

            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0], ["timestamp", "id", "category", "severity", "prompt", "response", "auto_result"])
            self.assertEqual(rows[1][1], "t1")
            self.assertEqual(rows[1][4], "Hello World")  # newlines collapsed
            self.assertEqual(rows[1][5], "Response text")  # newlines collapsed
            self.assertEqual(rows[1][6], "PASS")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
