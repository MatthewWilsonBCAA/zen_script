global_variables = dict()


def static_display(obj, item_list):
    i = 0
    for item in item_list:
        item_list[i] = convert_variable(obj, item)
        if type(item_list[i]) == list:
            try:
                ind = int(item_list[i + 1].replace("i/", ""))
                item_list[i] = item_list[i][ind]
                item_list[i + 1] = "\b"
            except:
                raise TypeError(
                    f"Line {obj.index+1}, attempt to print a list without referencing an index"
                )
        i += 1
    print(" ".join(item_list))


static_functions = dict()  # function calls will look like this:
# ( function_name $args ... )
static_functions["display"] = static_display
zen_functions = dict()  # functions written in Zen by the end user!
# definitions will look like this:
# define ( function_name  *args ... )
# ... code ...
# end


def assign_variable(obj, var, value):
    scope = obj
    if scope.parent:
        scope.parent.local_variables[var] = value
    else:
        global_variables[var] = value
    # reached_top = False
    # looped_top = False
    # while not looped_top:
    #     if var in scope.local_variables.keys():
    #         return scope.local_variables[var]
    #     if reached_top:
    #         looped_top = True
    #     if scope.parent:
    #         scope = scope.parent
    #     else:
    #         reached_top = True


def convert_variable(obj, var):
    if not "$" in var:
        return var
    scope = obj
    var = var.replace("$", "")
    reached_top = False
    looped_top = False
    while not looped_top:
        if var in scope.local_variables.keys():
            return scope.local_variables[var]
        if reached_top:
            looped_top = True
        if scope.parent:
            scope = scope.parent
        else:
            reached_top = True

    if var in global_variables.keys():
        return global_variables[var]
    else:
        raise NameError(f"Line {obj.index+1}, {var} not defined in any scope")


class Node:
    def __init__(self, line, index, tree):
        self.words = line.split()
        self.index = index
        self.parent = None
        self.else_statement = None
        self.has_children = False
        self.tree = tree
        self.local_variables = dict()
        self.return_value = None

    def __str__(self):
        return " ".join(self.words)

    def run_block(self):
        i = self.index + 1
        lent = len(self.tree.children)
        while i < lent:
            if self.tree.children[i].parent == self:
                self.tree.children[i].interp()
            i += 1

    def define_block(self):
        i = self.index + 1
        c = 1
        while self.has_children == False:
            if not self.tree.children[i].words or self.tree.children[i] == self:
                i += 1
                continue
            if self.tree.children[i].words[0] == "if":
                c += 1
            elif self.tree.children[i].words[0] == "end":
                c -= 1
                if c == 0:
                    self.has_children = True
            self.tree.children[i].parent = self
            i += 1
        zen_functions[self.words[2]] = self

    def if_block(self):
        i = self.index + 1
        c = 1
        self.found_else = False
        while self.has_children == False:
            if not self.tree.children[i].words or self.tree.children[i] == self:
                i += 1
                continue
            if self.tree.children[i].words[0] == "if":
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
                    self.has_children = True
            if not self.found_else:
                self.tree.children[i].parent = self
            else:
                self.tree.children[i].parent = self.else_statement
            i += 1
        left = self.words[1]
        right = self.words[3]
        if "$" in self.words[1]:
            left = convert_variable(self, self.words[1])
        if "$" in self.words[3]:
            right = convert_variable(self, self.words[3])
        if self.words[2] == "==":
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

    def exec_function(self, item_list):
        func = item_list.pop(0)
        if func in static_functions.keys():
            static_functions[func](self, item_list)
        else:
            i = 3
            for item in item_list:
                args = zen_functions[func].words
                j = convert_variable(self, item)
                zen_functions[func].local_variables[args[i]] = j
                i += 1
            zen_functions[func].run_block()
            return zen_functions[func].return_value

    def interp(self):
        if self.words:
            start = self.words[0]
        else:
            start = ""
        if start == "assign":
            if self.words[2] == "str":
                string = list(self.words)
                string.pop(0)
                name = string.pop(0)
                string.pop(0)
                assign_variable(self, name, " ".join(string))
            elif self.words[2] == "(":
                item_list = list(self.words)
                item_list.pop(0)
                item_list.pop()
                name = item_list.pop(0)
                item_list.pop(0)
                # print("ITEM LIST", item_list)
                assign_variable(self, name, self.exec_function(item_list))
            elif self.words[2] == "math":
                q_line = list(self.words)
                q_line.pop(0)
                name = q_line.pop(0)
                q_line.pop(0)
                result = q_line.pop(0)
                if "$" in result:
                    result = convert_variable(self, result)
                    if type(result) == list:
                        if q_line[0] and "i/" in q_line[0]:
                            j = q_line[0].replace("i/", "")
                            result = result[int(j)]
                            q_line.pop(0)
                result = float(result)
                while q_line:
                    if "$" in q_line[0]:
                        q_line[0] = convert_variable(self, q_line[0])
                        if type(q_line[0]) == list:
                            if q_line[1] and "i/" in q_line[1]:
                                j = q_line[1].replace("i/", "")
                                q_line[1] = q_line[1][int(j)]
                    op = q_line.pop(0)
                    if not q_line:
                        break
                    number = float(q_line.pop(0))
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
                assign_variable(self, name, str(result))
            elif self.words[2] == "list":
                q_line = list(self.words)
                q_line.pop(0)
                name = q_line.pop(0)
                q_line.pop(0)
                result = []
                for i in q_line:
                    result.append(convert_variable(self, i))
                assign_variable(self, name, result)
            else:
                assign_variable(self, self.words[1], self.words[2])

        # elif start == "display":
        #     i = 0
        #     string = list(self.words)
        #     string.pop(0)
        #     lent = len(string)
        #     while i < lent:
        #         if "$" in string[i]:
        #             string[i] = convert_variable(self, self.words[i + 1])
        #             if type(string[i]) == list:
        #                 if string[i + 1] and "i/" in string[i + 1]:
        #                     j = string[i + 1].replace("i/", "")
        #                     string[i] = string[i][int(j)]
        #                     string[i + 1] = "\b"
        #                 else:
        #                     string[i] = " ".join(string[i])
        #         i += 1
        #     print(" ".join(string))
        elif start == "get":
            global_variables[self.words[1]] = input()
        elif start == "else":
            self.run_block()
        elif start == "repeat":
            self.tree.i = self.parent.index
            self.parent.interp()
        elif start == "if":
            self.if_block()
        elif start == "(":
            item_list = list(self.words)
            item_list.pop()
            item_list.pop(0)
            self.exec_function(item_list)
        elif start == "define":
            self.define_block()
        elif start == "return":
            self.parent.return_value = convert_variable(self, self.words[1])
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

    def show_tree(self):
        for child in self.children:
            print(f"{child} <with parent> {child.parent}")


my_file = open("program_4.txt", "r")
code = []
while True:
    cur_line = my_file.readline()
    if not cur_line:
        break
    cur_line = cur_line.strip()
    code.append(cur_line)
new_tree = Tree(code)
new_tree.run_program()
