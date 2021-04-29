# sprint-4-tests
Automated testing script for Sprint 4. If you want to contribute, upload an .html file with the input and an associated .txt file for the expected output (just make it empty if it's supposed to be wrong). If there is a single file that is not .html or .txt committed, mods will ban the person responsible for committing those files from the discord server and remove them from the organization.

## Usage

Use `python3 test.py` for regular testing (requires `parse` from `pip3` to be installed)

To test with valgrind, run `python3 test.py -m` or `python3 test.py --memory` (only works on Linux)


## Test Breakdown
`cs24_test_1.html` through `cs24_test_4.html` and .txts: Tests to make sure only one pair of `<html></html>` and `<body></body>` exist in your file, and that no tags exist outside of the scope of html.
