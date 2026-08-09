# =============================================
# ADVANCED SCIENTIFIC CALCULATOR - Python Mini Projects
# Features: Full expressions, Scientific, Memory, History
# =============================================

import math

history = []
memory = 0

def calculate(expression):
    """Safely calculate any math expression"""
    try:
        # Replace ^ with ** for power
        expression = expression.replace("^", "**")
        
        # Allowed functions for safety
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        allowed_names.update({"abs": abs, "round": round})
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        history.append(f"{expression} = {result}")
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Invalid expression"

def show_menu():
    print("\n" + "="*50)
    print(" ADVANCED SCIENTIFIC CALCULATOR")
    print("="*50)
    print("Type any expression: 2+3*4, (5+2)/3, 2^8")
    print("Scientific: sin(30), cos(60), tan(45), sqrt(16), log(100)")
    print("Commands: history, mem, mem+, mem-, clear, exit")
    print("="*50)

def handle_commands(cmd):
    global memory
    if cmd == "history":
        print("\n--- Calculation History ---")
        for i, h in enumerate(history[-5:], 1): # show last 5
            print(f"{i}. {h}")
    elif cmd == "mem":
        print(f"Memory: {memory}")
    elif cmd.startswith("mem+"):
        try:
            memory += float(cmd.split()[1])
            print(f"Added to memory. Memory = {memory}")
        except: print("Usage: mem+ 5")
    elif cmd.startswith("mem-"):
        try:
            memory -= float(cmd.split()[1])
            print(f"Subtracted from memory. Memory = {memory}")
        except: print("Usage: mem- 5")
    elif cmd == "clear":
        history.clear()
        print("History cleared")
    else:
        return False
    return True

def main():
    while True:
        show_menu()
        user_input = input("Enter expression or command: ").strip().lower()

        if user_input == "exit":
            print("Thank you for using Advanced Calculator!")
            break
        
        if handle_commands(user_input):
            continue
        
        result = calculate(user_input)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
