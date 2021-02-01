global_variables = dict()


def convert_variable(var):
    var = var.replace("$", "")
    if var in global_variables.keys():
        return global_variables[var]
    else:
        return var


class Node:
    def __init__(self, line, index, tree):
        self.words = line.split()
        self.index = index
        self.parent = None
        self.else_statement = None
        self.tree = tree

    def __str__(self):
        return " ".join(self.words)

    def run_block(self):
        i = self.index + 1
        lent = len(self.tree.children)
        while i < lent:
            if self.tree.children[i].parent == self:
                self.tree.children[i].interp()
            i += 1

    def interp(self):
        # print(self, ":", self.parent)
        start = self.words[0]
        if start == "assign":
            if self.words[2] == "str":
                self.words.pop(0)
                name = self.words.pop(0)
                self.words.pop(0)
                global_variables[name] = " ".join(self.words)
            elif self.words[2] == "math":
                self.words.pop(0)
                name = self.words.pop(0)
                self.words.pop(0)
                result = self.words.pop(0)
                if "$" in result:
                    result = convert_variable(result)
                result = float(result)
                while self.words:
                    if "$" in self.words[0]:
                        self.words[0] = convert_variable(self.words[0])
                    op = self.words.pop(0)
                    number = float(self.words.pop(0))
                    if op == "+":
                        result += number
                    elif op == "-":
                        result -= number
                    elif op == "*":
                        result *= number
                    elif op == "/":
                        result /= number
                    elif op == "**":
                        result = result ** number
                if round(result) == result:
                    result = round(result)
                global_variables[name] = str(result)
            else:
                global_variables[self.words[1]] = self.words[2]
        elif start == "display":
            i = 0
            string = list(self.words)
            string.pop(0)
            lent = len(string)
            while i < lent:
                if "$" in string[i]:
                    string[i] = convert_variable(self.words[i + 1])
                i += 1
            print(" ".join(string))
        elif start == "get":
            global_variables[self.words[1]] = input(">")
        elif start == "else":
            self.run_block()
        elif start == "repeat":
            self.tree.i = self.parent.index - 1
        elif start == "if":
            i = self.index + 1
            c = 1
            self.found_else = False
            while True:
                if (
                    self.tree.children[i].words[0] == "if"
                    or self.tree.children[i].words[0] == "while"
                ):
                    c += 1
                elif (
                    self.tree.children[i].words[0] == "else"
                    and self.found_else == False
                    and c == 1
                ):
                    self.else_statement = self.tree.children[i]
                    self.found_else = True
                elif self.tree.children[i].words[0] == "end":
                    c -= 1
                    if c == 0:
                        break
                # print(self.tree.children[i])
                if not self.found_else:
                    self.tree.children[i].parent = self
                else:
                    self.tree.children[i].parent = self.else_statement
                i += 1
            left = self.words[1]
            right = self.words[3]
            if "$" in self.words[1]:
                left = convert_variable(self.words[1])
            if "$" in self.words[3]:
                right = convert_variable(self.words[3])
            if self.words[2] == "=":
                if left == right:
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
            if self.words[2] == "!=":
                if left != right:
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
            if self.words[2] == ">":
                if float(left) > float(right):
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
            if self.words[2] == "<":
                if float(left) < float(right):
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
            if self.words[2] == ">=":
                if float(left) >= float(right):
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
            if self.words[2] == "<=":
                if float(left) <= float(right):
                    self.run_block()
                else:
                    if self.else_statement:
                        self.else_statement.run_block()
        elif start == "com":
            pass


class Tree:
    def __init__(self, lines):
        self.children = []
        j = 0
        for i in lines:
            self.children.append(Node(i, j, self))
            j += 1

    def run_program(self):
        self.i = 0
        lent = len(self.children)
        while self.i < lent:
            if self.children[self.i].parent == None:
                self.children[self.i].interp()
            self.i += 1


my_file = open("program.txt", "r")
code = []
while True:
    cur_line = my_file.readline()
    if not cur_line:
        break
    code.append(cur_line)

new_tree = Tree(code)
new_tree.run_program()
