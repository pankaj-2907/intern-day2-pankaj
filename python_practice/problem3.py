## Problem 3: File Handling
# Create a program that:
#  1.	Reads a .txt file.
#  2.	Counts the total number of words.
#  3.	Counts the total number of lines.
#  4.	Prints both counts.

import re

def file_analyze(filepath: str):
    try:
        # Opening file in read mode.
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # Count total lines
            line_count = len(lines)
            
            # Count total words using regex
            word_count = sum(len(re.findall(r'\b\w+\b', line)) for line in lines)

            # Print both counts
            print(f"Total Lines: {line_count}")
            print(f"Total Words: {word_count}")
            
        return word_count, line_count

    except FileNotFoundError:
        print(f"Error: '{filepath}' File Not Found!")
    except Exception as e:
        print(f" Something went wrong {e}")

# Test karne ke liye
if __name__ == "__main__":
    file_analyze("python_practice/sample.txt")