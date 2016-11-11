def custom_dict_filter(d, conditions):
	for key, value in conditions.items():
		if d[key] != value:
			return False
	return True

####tests####
first = {"host": "192.168.1.104",
		 "port": 5432}
second = {"host": "192.168.1.104"}

print(custom_dict_filter(first, second))