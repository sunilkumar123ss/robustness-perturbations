# Robustness perturbation harness

Generate case, whitespace, and typographic-quote variations, then compare externally supplied outputs with their baseline. The fixture responses are hand-written synthetic labels, not model-generated measurements.

~~~sh
python3 main.py --input example.json --mode generate
python3 main.py --input example.json --mode score
python3 -m unittest -v
~~~

The harness never calls a model or manufactures missing observations. It reports measured coverage separately from exact-output stability, ignoring only surrounding output whitespace. Missing responses remain missing, and zero measurements produce null stability. Replace the response section with your own actual observations after generating and reviewing the suite.

These transformations are candidates for invariance tests, not guaranteed meaning-preserving edits: case, whitespace, and quotes can matter in code, identifiers, or specialized text. Exact output equality is most useful for structured labels; it is too strict for many free-form answers. Stable outputs can still be consistently wrong.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
