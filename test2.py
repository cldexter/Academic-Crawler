
def function1(a):
    print "function1"
    print a

def function2(b):
    print "function2"
    print b

def function3(fn_list):
    for function in fn_list:
        function()

def function4(a, *args):
    for function in args:
        function(a)

function_list = [function1, function2]

function4("fuck", function1, function2)