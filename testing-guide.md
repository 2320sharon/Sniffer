# Testing Guide for Sniffer

## How to Run Automatic Testing with PyTest

---

- Automatic testing runs all the tests in the `Sniffer\Sniffer\tests` folder and prints the output in the console.

- If any of the tests fail due to changes you made in the code `Pytest` will tell you exactly what failed.
### WARNING
NOTE: Do NOT change any of the data within the `test_data` folder within `Sniffer\Sniffer\tests\test_data` it will cause tests to fail. That directory is only to be used for testing.
### How to Run Pytest
---
```bash
conda activate sniffer
# Pytest should already be installed by default with Sniffer but if it isn't somehow uncomment the next line
# pip install pytest
cd <location where you installed sniffer>
# You should be at a location something like this  C:\Myprograms\Sniffer\
pytest
```

To see all the output of each test use the `-s` flag to `switch on` the printed output to the console.

- `-v` is the `verbose` flag which gives more information about each test

```bash
pytest -v -s
```

To see all the coverage of the testing suite. This coverage report will display the percentage of the code that has been tested and which lines of codes are not run by tests.

```bash
pytest --cov-report term-missing --cov
```



## How to Run Automatic Linting

---

Automatic linting is the linter fixing all the formatting errors in your code. Basically it adds spaces where they are missing,
removed excess whitespace and makes your code adhere to Python style standards.

```bash
conda activate sniffer
# If you don't have autopep8 install it
# pip install autopep8
cd <location where you installed sniffer>
cd Sniffer
# You should be at a location something like this  C:\Myprograms\Sniffer\Sniffer
autopep8 -i  --max-line-length 120 -a -a sniffer.py
```

- This will format all your code `--in-place` because of the `-i` flag.
- The `-a` stands for `--aggressive` and its how much you want the linter to modify your code. [Read about it here](https://pypi.org/project/autopep8/)
- The `--max-line-length 120` means that the linter will not let any lines of code be long than 120 characters
- If you don't want your sniffer.py file modified and want to see a preview of the changes run the same command,but
  with the `-d` flag which stands for `--diff`. This shows you which lines will be changing without actually changing them.
  Here is a quickly example:

```bash
autopep8 -d  --max-line-length 120 -a -a sniffer.py
```
