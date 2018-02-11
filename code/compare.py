with open('drivebook.txt', 'r') as of:
	allbook = [line.strip() for line in of]
with open('books.txt', 'r') as nf:
	drivebook = [line.strip() for line in nf]
missingbook = []

print('comparing...')
for item in allbook:
	print(item)
	if item not in drivebook:
		missingbook.append(item)
print(missingbook)
with open('notfound.txt', 'w') as nfd:
	for item in missingbook:
		nfd.write('%s\n' % item)
