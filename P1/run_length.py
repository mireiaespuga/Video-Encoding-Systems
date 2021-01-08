def RL_encode(message):
    # initialize empty variables
    count = 0
    bit = ''
    result = []  

    split_sequence = message.split(" ")  # split incoming message
    
    # run lenght algorithm
    previous_bit = split_sequence[0]
    for B in split_sequence:
        bit = B

        if previous_bit == bit:
            count = count + 1
        else:
            result.append(str(count) + previous_bit)
            count = 1
        previous_bit = bit

    result.append(str(count) + previous_bit)
    return result


# input parameters from terminal
seq = str(raw_input("Enter a binary sequence: "))

# get encoded sequence
encoded_message = RL_encode(seq) 

# format output
message = ''
for i in encoded_message:
    message = message + i + ' '

print('Encoded sequence: ' + message)