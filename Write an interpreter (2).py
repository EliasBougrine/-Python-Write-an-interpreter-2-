import numpy as np



# Here are different possible inputs:

# The code should return just a value
Input0 = '(+,5,2)'
Input1 = '(-,7,4)'
Input2 = '(x,18,3)'

# The code returns a value and assigns it to a variable
Input3 = 'a0:=(+,10,12)'
Input4 = 'a0:=(-,45,12)'
Input5 = 'a0:=(x,1,6)'

# Error: undefinned variable
Input6 = '(+,a0,2)'
Input7 = '(-,5,a0)'
Input8 = '(x,a0,7)'

# The code should return a boolean
Input9 = '(or,true,true)'
Input10 = '(or,false,true)'
Input11 = '(or,false,false)'

Input12 = '(and,true,true)'
Input13 = '(and,false,true)'
Input14 = '(and,false,false)'

Input15 = '(<,4,9)'
Input16 = '(=,56,56)'
Input17 = '(<,52,1)'
Input18 = '(=,21,12)'

# The code returns a boolean and assigns it to a variable
Input19 = 'b0:=(or,false,true)'
Input20 = 'b0:=(and,false,true)'
Input21 = 'b0:=(<,52,1)'
Input22 = 'b0:=(=,48,48)'

# If/While loop
Input23 = 'if{(=,4,15)}else{b0:=false}then{b0:=true}'



# We define the first calculation function. It permits to do the computation of a while/if loop

def Calculation1(dico,Input):
    inp = len(Input)
    # Test if we have to do an 'if' loop
    if ('if' in Input):
        cond = ''   # Condition of the if loop
        cond_true = ''   # If the condition is true
        cond_false = ''   # If the condition is false
        u = 0   # Position of '{'
        v = 0   # Position of '}'
        a = 0   # Number of '{'
        # Find the condition and the actions of the if loop
        for i in range(0,inp):
            if Input[i] == '{':
                u = i
                a = a + 1
            elif Input[i] == '}':
                v = i
                if a == 1:
                    cond = Input[u+1:v]
                elif a == 2:
                    cond_false = Input[u+1:v]
                elif a == 3:
                    cond_true = Input[u+1:v]
        # Test if the condition is true
        if Calculation2(dico,cond)[0]=='true':
            return Calculation2(dico,cond_true)
        # If the condition is not true
        elif Calculation2(dico,cond)[0]=='false':
            return Calculation2(dico,cond_false)
        # If the condition is not a boolean
        else:
            return 'The condition is not a boolean'
    # Test if we have to do an 'while' loop
    elif ('while' in Input):
        u = 0   # Position  of the first '}'
        v = 0   # Position of the second '{'
        # Take the condition of the loop
        for i in range(6,inp-1):
            if Input[i] == '}':
                u = i
            elif Input[i] == '{':
                v = i
        cond = Input[6:u]   # Condition of the while loop
        do = Input[v+1:inp-1]   # Action to do if the condition is true
        while Calculation2(dico,cond)[0]=='true':
            a = Calculation2(dico,do)
            if Calculation2(dico,do)[0]=='false':
                return a
    # If we don't have to do either a while or if loop, we just have to compute a basic result
    else:
        return Calculation2(dico,Input)



# We define the second calculation function. It permits to assign variables to the dico

def Calculation2(dico,Input):
    inp = len(Input)
    # Test if we need to assign the calculation into a variable
    if ':' in Input:
        for i in range(0,inp):
            if Input[i] == ':':
                a = Calculation3(dico,Input[i+2:inp])
                # If the result is false
                if a[0] == 'false':
                    dico[Input[0:i]] = False
                # If the result is true
                elif a[0] == 'true':
                    dico[Input[0:i]] = True
                # If the result isn't defined
                elif a[0] == 'variable not defined or grammar not respected':
                    dico[Input[0:i]] = 'error'
                # If the result is an integer
                else:
                    dico[Input[0:i]] = int(a[0]) 
                return a
    # If we don't need to assign the calculation, just do it
    else:
        return Calculation3(dico,Input)



# Define the third calculation function. It permits to compute basic sequences

def Calculation3(dico,Input):
    inp = len(Input)
    u = 0   # position of the first ( 
    v = 0   # position of the first )
    if '(' not in Input and (('b' in Input) or ('a' in Input)) and ('false' not in Input) and (Input in dico):
        return dico[Input],dico
    elif '(' not in Input:
        return Input,dico
    while '(' in Input:
        i = 0
        while Input[i] != ')':
            if Input[i] == '(':
                u = i
            i=i+1
        v = i
        Input = Replace(Input,Compute(dico,Input,u,v)[0],u,v)
    return Input,dico



# Define a function that compute the result of an operation between 2 values

def Compute(dico,Input,u,v): 
    # If the operator is +, x or -
    if ('x' in Input) or ('+' in Input) or ('-' in Input):
        operator = Input[u+1]
        n1 = ''
        n2 = ''
        a = v
        # Get n1 and n2
        for i in range(u+3,v):
            if Input[i]==',':
                a = i
            elif i > a:
                n2 = n2 + Input[i]
            else:
                n1 = n1 + Input[i]
        n1 = variable(dico,n1)
        n2 = variable(dico,n2)
        # If n1 and n2 are two integers
        if n1 != 'error' and n2 != 'error' and n1 != 'false' and n2 != 'false'and n1 != 'true' and n2 != 'true':
            n1 = int(n1)
            n2 = int(n2)
            # Compute the appropriate operation between n1 and n2
            if operator == '+':
                r = n1 + n2
            elif operator == '-':
                r = n1 - n2
            elif operator == 'x':
                r = n1 * n2
            return str(r),dico
        # If n1 and n2 are not integers, return the false message
        else:
            return 'False_Message',dico
    # If the operator is 'or'
    elif 'or' in Input:
        n1 = ''
        n2 = ''
        a = v
        # Get n1 and n2
        for i in range(u+4,v):
            if Input[i] == ',':
                a = i
            elif i > a:
                n2 = n2 + Input[i]
            else:
                n1 = n1 + Input[i]
        n1 = variable(dico,n1)
        n2 = variable(dico,n2)
        # If n1 and n2 are not integers and not errors
        if n1 != 'error' and n2 != 'error':
            if (n1 or n2) == True:
                return 'true',dico
            else:
                return 'false',dico
        # Else, return the false message
        else:
            return 'False_Message',dico
    # If the operator is 'and'
    elif ('and' in Input):
        n1 = ''
        n2 = ''
        a = v
        # Get n1 and n2
        for i in range(u+5,v):
            if Input[i] == ',':
                a = i
            elif i > a:
                n2 = n2 + Input[i]
            else:
                n1 = n1 + Input[i]
        n1 = variable(dico,n1)
        n2 = variable(dico,n2)
        # If n1 and n2 are not an error
        if n1 != 'error' and n2 != 'error':
            if (n1 and n2) == True:
                return 'true',dico
            else:
                return 'false',dico
        # Else, return the false message
        else:
            return 'False_Message',dico
    # If the operator is '=' or '<'
    elif ('=' in Input) or ('<' in Input):
        operator = Input[u+1]
        n1 = ''
        n2 = ''
        a = v
        # Get n1 and n2
        for i in range(u+3,v):
            if Input[i] == ',':
                a = i
            elif i > a:
                n2 = n2 + Input[i]
            else:
                n1 = n1 + Input[i]
        n1 = variable(dico,n1)
        n2 = variable(dico,n2)
        # If n1 and n2 are not integers nor errors
        if n1 != 'error' and n2 != 'error' and n1 != 'false' and n2 != 'false'and n1 != 'true' and n2 != 'true':
            n1 = int(n1)
            n2 = int(n2)
            # Do the appropriate test according to the operator
            if operator == '=':
                if n1 == n2:
                    r = 'true'
                else:
                    r = 'false'
            else:
                if n1 <= n2:
                    r = 'true'
                else:
                    r = 'false'
            return r,dico
        # Else, return the false message
        else:
            return 'False_Message',dico
    else:
        return 'False_Message',d



# Define a function that replace the list of operation by the result

def Replace(Input,r,u,v): 
    inp = len(Input)
    # If the result is the false message
    if r == 'False_Message':
        return 'There is a problem. Be careful with the grammar of the input. Is your variable defined?'
    ch = ''
    for i in range(0,inp):
        if i < u or i > v:
            ch = ch + Input[i]
        elif i == u:
            ch = ch + r
    return ch



# Def a variable function that try if the variable is in the dictionnary

def variable(dico,n):
    if 'true' in n:
        return True
    if 'false' in n:
        return False
    elif ('a' in n) or ('b' in n):
        if n in dico:
            return dico[n]
        else:
            return 'error'
    else:
        return n



# We define the interpreter

def Interpreter(Input):
    inp = len(Input)
    # Create a dictionnary we will implement with the new variables
    dico = {}
    seq = ''   # Different possible sequences within the input
    a = 0   # Position of the possible ';'
    # Test if there are more than one sequence within the input
    if ';' in Input:
        for i in range(0,inp):
            if Input[i]==';':
                a = i
                if 'skip' in seq:
                    seq=''
                else:
                    Calculation1(dico,seq)
                    seq = ''
            else:
                seq = seq + Input[i]
        return(Calculation1(dico,Input[a+1:inp]))
    else:
        return(Calculation1(dico,Input))

