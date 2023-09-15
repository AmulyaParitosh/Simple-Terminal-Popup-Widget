
import contextlib
with open('/home/encryptedbee/.zsh_history', 'rb') as file:
	history = []
	for line in file:
		with contextlib.suppress(Exception):
			history.append(line.decode('utf-8').rsplit(';',1)[-1].strip())
	print(history)
