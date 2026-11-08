# pytextprep

A small, dependency-free text preprocessing library for NLP.
It has cleaning functions, tokenizers, a Porter stemmer, a rule-based
lemmatizer, and a `Pipeline` that runs steps by name.

Python standard library only. No third-party packages.

## Quick start

```python
from pytextprep import Pipeline

pipe = Pipeline([
    ("lowercase", {}),
    ("remove_urls", {}),
    ("remove_punctuation", {"keep_emojis": False}),
    ("remove_stopwords", {}),
    ("stem", {}),
])

print(pipe)
print(pipe.transform("Running to see www.iti.gov.eg/courses, NOW!"))
print(pipe.transform("Cats are running", return_tokens=True))
print(pipe.transform_batch(["Cats running", "Dogs barking"]))
```

Every step takes a `str` and returns a `str`.
Steps that need words split the text inside and rejoin it with single spaces.

## Errors

Mistakes are reported when the pipeline is **built**, not when it runs.

```python
Pipeline([("remove_url", {})])
# UnknownStepError: 'remove_url' is not a step. Did you mean 'remove_urls'?

Pipeline([("remove_punctuation", {"keep_emoji": False})])
# InvalidStepParamsError: 'remove_punctuation' got an unexpected parameter 'keep_emoji'. ...
```

## API reference

### Cleaning (`pytextprep/Steps/Cleaning.py`)

| Function | Description | Tested in |
| --- | --- | --- |
| `lowercase(text)` | Lowercase with `str.casefold()` | `tests/test_cleaning.py` |
| `normalize_whitespace(text)` | Tabs, newlines and repeated spaces become one space; ends stripped | `tests/test_cleaning.py` |
| `remove_urls(text, replace_with="")` | Removes `http://`, `https://` and `www.` links; trailing punctuation stays | `tests/test_cleaning.py` |
| `remove_emails(text, replace_with="")` | Removes `name@domain.tld` addresses | `tests/test_cleaning.py` |
| `remove_punctuation(text, keep_emojis=True)` | Deletes apostrophes; other punctuation becomes a space | `tests/test_cleaning.py` |
| `normalize_repeating_chars(text, keep=1)` | Cuts a letter repeated 3+ times to `keep` copies; doubles stay | `tests/test_cleaning.py` |
| `remove_html(text)` | Removes tags, then decodes entities | `tests/test_cleaning.py` |
| `remove_mentions(text)` | Removes `@user` handles, but not emails | `tests/test_cleaning.py` |
| `remove_hashtags(text, keep_word=False)` | Removes hashtags; `keep_word=True` keeps the word | `tests/test_cleaning.py` |
| `remove_digits(text)` | Removes all digits | `tests/test_cleaning.py` |
| `handle_emojis(text, mode="remove")` | `"remove"` deletes emojis; `"text"` replaces them with `:unicode_name:` | `tests/test_cleaning.py` |

### Tokenization and filtering (`pytextprep/Steps/Tokenization.py`)

| Function | Description | Tested in |
| --- | --- | --- |
| `word_tokenize(text)` | Splits into words; keeps internal apostrophes and hyphens | `tests/test_tokenization.py` |
| `sent_tokenize(text)` | Splits into sentences; skips abbreviations and numbers like `3.14` | `tests/test_tokenization.py` |
| `remove_stopwords(text, custom_words=None, extra_only=False)` | Case-insensitive stopword removal; keeps `not`, `no`, `nor` | `tests/test_tokenization.py` |
| `expand_contractions(text)` | Table-driven; handles `'` and `’`; keeps the first capital | `tests/test_tokenization.py` |

`word_tokenize` and `sent_tokenize` return lists, so they are not pipeline steps.
Call them directly.

### Stemming and lemmatizing

| Function | Description | Tested in |
| --- | --- | --- |
| `stem(text)` | Porter stemmer (original 1980 algorithm, steps 1a to 5b) | `tests/test_stemming.py` |
| `lemmatize(text)` | Rule-based: irregular forms first, then plural rules | `tests/test_lemmatization.py` |

### Pipeline (`pytextprep/pipeline.py`)

| Function | Description | Tested in |
| --- | --- | --- |
| `Pipeline(steps)` | Builds a pipeline from `(step_name, params)` pairs | `tests/test_pipeline.py` |
| `Pipeline.transform(text, return_tokens=False)` | Runs all steps in order on one text | `tests/test_pipeline.py` |
| `Pipeline.transform_batch(texts)` | Runs `transform` on a list of texts | `tests/test_pipeline.py` |
| `Pipeline.steps` | Returns the configured steps | `tests/test_pipeline.py` |

### Registry and exceptions

| Name | Description | Tested in |
| --- | --- | --- |
| `register_step(name)` | Decorator that registers a function as a step | `tests/test_pipeline.py` |
| `get_step(name)` | Returns a registered step or raises `UnknownStepError` | `tests/test_pipeline.py` |
| `available_steps()` | Returns the registered step names, sorted | `tests/test_pipeline.py` |
| `PyTextPrepError` | Base class of all package errors | `tests/test_pipeline.py` |
| `UnknownStepError` | Unknown step name, with a "did you mean" suggestion | `tests/test_pipeline.py` |
| `InvalidStepParamsError` | A step got a parameter it does not accept | `tests/test_pipeline.py` |

## Adding a new step

```python
from pytextprep.registry import register_step
from pytextprep.validation import requires_str

@register_step("uppercase")
@requires_str
def uppercase(text: str) -> str:
    return text.upper()
```

The `Pipeline` class does not need any change.

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT