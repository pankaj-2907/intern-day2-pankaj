# Problem 4: Exception Handling
def divide_numbers(a, b):
    try:
        # Converting both inputs to float and then divide.
        result = float(a) / float(b)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        return None
    except (ValueError, TypeError):
        print("Error: Invalid input. Please provide numbers.")
        return None
    else:
        # If no error occurs, this will print
        print(f"Successful division: {a} / {b} = {result}")
        return result

# Test input
if __name__ == "__main__":
    print("--- Testing Division ---")
    divide_numbers(10, 2)   # Successful division
    divide_numbers(10, 0)   # Division by zero error
    divide_numbers(10, "a") # Invalid input error