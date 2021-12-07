# SPOC backend:

## Code good practices

The idea of having best practices when coding is something that you need to define with your team and stick to those practices, but we can generalize some thigs for the backend.

Plase stick to follow [pep8](https://www.python.org/dev/peps/pep-0008/) when coding in python, this will help us to follow good standards when writing code.

### How to test

Let's follow the [test driven development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development). Please make sure your tests are mocked up correctly and all the dependencies are managed automatically.

Each module should have their own tests, this will allow us to just worry about the part of the code we are changing.
Let's start working with the actual configuration:
```
mypkg/
    __init__.py
    code.py
    test/
        __init__.py
        test_code.py
        run_tests.py
        ...
```
