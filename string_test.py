f = open('person.txt', 'r')
content = f.read()
f.close()
print(content.split())

f = open('answer.txt', 'r')
content = f.read()
print(content.split())