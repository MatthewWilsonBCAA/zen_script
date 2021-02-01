# Zen Script
## Inspiration
The language Cobol inspired the sentence-like structure of Zen's syntax with spaces being significant. However, there is still the "pseudo-code" style following things
like Python, along with the loose-type system. 
## Features
### Built-In statements
"assign" is the built-in statement for initializing variables. It's syntax is assign <variable-name> <optional:str,list,math> <value(s)>. The optional parameter 'str' allows you
to store a string with spaces in it. 'list' allows you to store a collection of data. 'math' allows you to perform operations and use pre-existing variables in the
definition of your value. To reference variables, prefix it's name with a $ sign.

"display" acts as a print statement, allowing you to send information to the screen. Whatever is said behind it will be sent out.

"get" acts as an input statement. It only takes one arguement, in which is the variable you wish to send the keyboard input to.

"if...else...end" is the basic branching set up. You can compare values with =, !=, >, <, >=, and <= to see when the code under the if statement should execute. If the case
given in the if statement fails, the optional else block is executed instead. 'end' denotes where the if and else blocks stop.

"repeat" can be put at the end of an if's block to let it act as a while loop, where the loop stops only when the condition becomes false.
