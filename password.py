from bcrypt import hashpw, gensalt

print(hashpw(b"gymbk", gensalt()))
