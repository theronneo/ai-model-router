# Local Laya router for Codex

A small learning project: give a coding request to [Laya](https://github.com/NandhaKishorM/laya), a local decision model, and get a suggested Codex model. Laya chooses between two **tiers**. This script maps `fast` to `gpt-6-luna` and `strong` to `gpt-6.1-sol` by default. It does not send your query to a paid Jev endpoint. Without `--launch`, it only recommends a model.

## Set up (about 10 minutes, plus the first checkpoint download)

From this directory, with [uv](https://docs.astral.sh/uv/) installed:

```sh
uv venv --python 3.14
uv pip install -r requirements.txt
.venv/bin/python -m src.router "Rename this variable for clarity"
```

Laya downloads a model checkpoint on the first prediction; later predictions reuse the local cache. The download needs internet access and enough disk space. No Laya API key is needed for local inference. If Python 3.14 is unavailable, use a supported Python 3.10+ version in the first command.

## Use it with Codex

For an **existing desktop app session**, run the command above in a terminal, then use the model control beneath the composer to select the recommended model. In an **existing Codex CLI session**, use `/model`. This script cannot silently change the model of a running Codex turn. [OpenAI Docs](https://learn.chatgpt.com/docs/models) describes those controls.

For a **new Codex CLI session**, let the script launch Codex after Laya decides:

```sh
.venv/bin/python -m src.router "Investigate a race condition in the cache" --launch
```

This starts `codex --model <Laya's selection> "<your query>"`. Codex still uses your normal sign-in and usage allowance. Model availability depends on your account and workspace. If either default is unavailable, pass `--fast-model MODEL` or `--strong-model MODEL` using names shown in your Codex model picker.

## Understand the decision

Open [`src/router.py`](src/router.py). `query` is the **state**: the text Laya judges. `QUESTION` is a **Choice** question. Its `criteria` give Laya two possible answers and describe when each fits. `Router.predict` returns `answers.model_tier.choice` plus probabilities and confidence. The script prints these signals, then uses a small Python mapping from tier to Codex model. Laya selects the tier; Python controls the final action.

Try a short edit and a complex debugging prompt. Compare Laya's choice with your own judgment. The stock checkpoint is a learning baseline, not a proven measure of task difficulty; its confidence is not a guarantee that the chosen Codex model will succeed. The [Laya project](https://github.com/NandhaKishorM/laya) reports that task-specific fine-tuning improves accuracy. Keep this two-tier example simple and collect real examples before adding thresholds or automatic policies.

## Check the code

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The tests replace only the local model call, so they run without a checkpoint or network access. They verify the Choice request and model mapping. They do not validate live Laya predictions or Codex account access.
