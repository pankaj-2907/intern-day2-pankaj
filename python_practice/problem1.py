# Problem 1: Word Frequency
## Write a function that accepts a sentence and returns the frequency of each word.

def count_word_freq(sentence):

    # Convert the input into lower case and splt the words.
    words = sentence.lower().split()

    # Creating empty dictionary.
    freq = {}

    # Loop through every word in sentence and count them.
    for word in words:
        if word in freq:
            freq[word] += 1   # Add by 1 if word is already in frequency.
        else:
            freq[word] = 1    # If word occurs only once.

    return freq

## Testing the output
input_text = "AI is useful and AI is growing"
print(count_word_freq(input_text)) 