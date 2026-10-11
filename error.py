import lexer

def error(line, message):
    if type(line)==int:
        report(line,"",message)
    else:
        token=line
        report(token.line," at '"+token.lexeme+"'",message)

def report(line, where,message):
    global hadError
    print(f"[Error] line {line}: {where}: {message}")
    hadError=True