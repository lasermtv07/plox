def error(line, message):
    report(line,"",message)

def report(line, where,message):
    global hadError
    print(f"[Error] line {line}: {where}: {message}")
    hadError=True