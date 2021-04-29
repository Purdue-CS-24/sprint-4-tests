# sprint-4-tests
Automated testing script for Sprint 4. If you want to contribute, upload an .html file with the input and an 
associated .txt file for the expected output (just make it empty if it's supposed to be wrong). If there is a single 
file that is not .html or .txt committed, mods will ban the person responsible for committing those files from the 
Discord server and remove them from the organization.

## Usage

Use `python3 test.py` for regular testing (requires `parse` from `pip3` to be installed)

To test with valgrind, run `python3 test.py -m` or `python3 test.py --memory` (only works on Linux)

Note that you need to manually review valgrind output for memory testing. The script will not automatically check 
if the program does not leak memory.

## Test Breakdown

### `cs24_test_x`

Tests to make sure only one pair of `<html></html>` and `<body></body>` exist in your file, and that no tags exist 
outside of the scope of html.

### `cw_test_x`

Various tests collected from Campuswire posts.

 - `cw_test_1`: tests missing recognized tag
 - `cw_test_2`: tests unrecognized entity replacement
 - `cw_test_3`: tests unrecognized tags and text inside \<body\> tags


### `cw_min_test_x`

Tests from [this Campuswire post by Min Lu](https://campuswire.com/c/G3A7E1182/feed/1971) (thanks!)

See the linked post for details. Files 1-9 should be valid examples, while files 10-17 are invalid examples.

### `discord_test_x`

Various tests collected from Discord.

 - `discord_test_1`: test case from Sprint 3 (should be blank under Sprint 4 requirements since it is invalid)
 - `discord_test_2`: test case from Sprint 3 (also should be blank as it has an invalid tag level)
 - `discord_test_3`: tests missing closing recognized tag

### `handout_test_x`

Test cases from the handout.

 - `handout_test_1`: test case from Sprint 3
 - `handout_test_2`: test case from Sprint 3
 - `handout_test_3`: test case from Sprint 4
 - `handout_test_4`: tests missing closing recognized tag
 - `handout_test_5`: tests file with invalid level nesting

### `self_test_x`

Miscellaneous test cases

 - `self_test_1`: tests all entity replacements
 - `self_test_2`: tests invalid file with multiple \<html\> tags
 - `self_test_3`: tests entity replacements in title attributes
 - `self_test_4`: tests invalid file with an unrecognized, mismatched closing tag
 - `self_test_5`: tests invalid file with missing \<html\> tag
 - `self_test_6`: tests invalid file with missing \<body\> tag