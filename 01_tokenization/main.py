import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = " Hey, there my name is vishal"

tokens = enc.encode(text)
print('\033[38;2;4;73;28m'+'tokens: ' + '\033[38;2;164;205;63m', tokens, '\033[0m')
# tokens:  [41877, 11, 1354, 922, 1308, 382, 323, 1109, 280] 

decoded = enc.decode([41877, 11, 1354, 922, 1308, 382, 323, 1109, 280] )
print('\033[38;2;78;201;59m'+'decoded: ' + '\033[38;2;53;210;22m', decoded, '\033[0m')
