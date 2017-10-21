
def function1():
    print "function1"

def function2():
    print "function2"

def function3(fn_list):
    for function in fn_list:
        function()

def function4(*args):
    for function in args:
        function()

function_list = [function1, function2]

function4(function1, function2)