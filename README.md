# SetLang
Based on the concept of an eso-lang where you have access to a fully-fletched proramming language but where the only form of 
output is "yes" or "no" to the question if a supplied particular solution is correct. The result is a very shallow library
and an interpreter that converts basic syntax into python.

## Running the SetLang interpreter
Running the "setlang_interpreter.py" program will launch a prompt. The interpreter comes with help-documentation that can be 
accessed by typing "help" at the prompt.

## The SetLang class
A simple class that implements some "double-underscore" methods of containers. It does not save any elements but instead
saves an anonymous function that returns a boolean (or a type which can be implicitly converted to a boolean) type. The
way to check for inclusion is running the function with a supplied element and returning the result. Thats about it.

## The SetLang interpreter
Basically converts from
```python
var_name = { e1 : condition }
``` 
into
```python
var_name = setlang(lambda e1 : condition)
```
and evaluates the last using the `eval()` function. It also keeps track of all variables in a dictionary
and therefore replaces all variable-names in a "SetLang" statement with dict accesses. I try catch
most syntax errors before they reach evaluation, but I'm quite far from proficient in using regular expressions. 
A big point I was trying to achieve was not being able to print the result of an evaluation. I therefore don't
allow print statements but when it actually became feasable to work with some sort of "SetLang-libraries" I hade to allow
saving to- and reading from files.
