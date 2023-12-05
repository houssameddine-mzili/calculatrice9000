import tkinter as tk
from collections import deque

def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    if operator == '+':
        values.append(left + right)
    elif operator == '-':
        values.append(left - right)
    elif operator == '*':
        values.append(left * right)
    elif operator == '/':
        values.append(left / right if right != 0 else "Error: Division by zero")

def greater_precedence(op1, op2):
    precedences = {'+' : 1, '-' : 1, '*' : 2, '/' : 2}
    return precedences[op1] > precedences[op2]

def evaluate_expression(expression):
    values = deque()
    operators = deque()
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] == '(':
            operators.append(expression[i])
        elif expression[i].isdigit() or expression[i] == '.':
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            values.append(float(expression[i:j]))
            i = j-1
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()  # Pop the '('
        else:  # Operator
            while (operators and operators[-1] in "+-*/" and
                   greater_precedence(operators[-1], expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        i += 1
    while operators:
        apply_operator(operators, values)
    return values.pop()


def on_click(char):
    global expression
    expression += str(char)
    input_text.set(expression)

def on_clear():
    global expression
    expression = ""
    input_text.set("")

def on_equals():
    global expression
    try:
        result = evaluate_expression(expression)
        input_text.set(str(result))
        expression = str(result)
    except Exception as e:
        input_text.set("Error")
        expression = ""


expression = ""
root = tk.Tk()
root.title("Calculator")


input_text = tk.StringVar()
input_frame = tk.Frame(root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2)
input_frame.pack(side=tk.TOP)
input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10)


buttons_frame = tk.Frame(root, width=312, height=272.5, bg="grey")
buttons_frame.pack()


button_texts = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2),
    ('C', 0, 0), ('/', 0, 1), ('*', 0, 2), ('-', 0, 3), ('+', 1, 3)
]

for text, row, col in button_texts:
    if text == '=':
        btn = tk.Button(buttons_frame, text=text, fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=on_equals)
    elif text == 'C':
        btn = tk.Button(buttons_frame, text=text, fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=on_clear)
    else:
        btn = tk.Button(buttons_frame, text=text, fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2", command=lambda txt=text: on_click(txt))
    btn.grid(row=row, column=col)


root.mainloop()
