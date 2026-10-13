"""Ask a local Laya model which Codex model tier fits a prompt."""

import argparse
import os


QUESTION = {
    "model_tier": {
        "type": "choice",
        "instructions": "Which Codex model tier best fits this user's coding request?",
        "criteria": {
            "fast": "A small, clear edit or straightforward question with limited scope.",
            "strong": "A complex bug, architecture decision, broad change, or ambiguous task needing deeper reasoning.",
        },
    }
}


def choose_model(query, laya_router, fast_model, strong_model):
    """Return the selected Codex model and Laya's raw decision signals."""
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty")

    result = laya_router.predict(query, QUESTION)
    try:
        answer = result["answers"]["model_tier"]
        tier = answer["choice"]
    except (KeyError, TypeError) as exc:
        raise ValueError("invalid Laya answer") from exc
    if tier not in ("fast", "strong"):
        raise ValueError(f"unexpected Laya choice: {tier}")

    return {
        "tier": tier,
        "model": fast_model if tier == "fast" else strong_model,
        "probabilities": answer["probabilities"],
        "confidence": answer["confidence"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Choose a Codex model with local Laya inference")
    parser.add_argument("query", help="The task you plan to give Codex")
    parser.add_argument("--fast-model", default="gpt-6-luna")
    parser.add_argument("--strong-model", default="gpt-6.1-sol")
    parser.add_argument("--launch", action="store_true", help="Start a new Codex CLI session")
    args = parser.parse_args(argv)

    try:
        from laya import Router
    except ImportError:
        parser.exit(1, "Laya is not installed. Run: uv pip install laya\n")

    try:
        decision = choose_model(args.query, Router(default="english"), args.fast_model, args.strong_model)
    except ValueError as exc:
        parser.exit(1, f"Routing failed: {exc}\n")

    print(f"Laya choice: {decision['tier']}", flush=True)
    print(f"Codex model: {decision['model']}", flush=True)
    print(f"Probabilities: {decision['probabilities']}", flush=True)
    print(f"Confidence: {decision['confidence']}", flush=True)
    if args.launch:
        os.execvp("codex", ["codex", "--model", decision["model"], args.query])
    print("For an existing Codex session, select this model in the composer or with /model.")


if __name__ == "__main__":
    main()
