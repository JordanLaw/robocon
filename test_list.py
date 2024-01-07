def myFunc(e):
  return e['x']

x1 = 300
y1 = 200

x2 = 200
y2 = 200

list = [{'x': str(x1), 'y': str(y1)},
        {'x': str(x2), 'y': str(y2)}]

list.sort(key=myFunc)

print(list)
print(list[0]['x'])