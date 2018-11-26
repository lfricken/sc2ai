import os

index_start = 4

def gen_investment(indexer: int) -> str:
	prop = str()
	prop += "\n"
	prop += "\tdef __init__(self):\n"
	prop += "\t\tself.investments = np.full({}, 0)\n".format(indexer)
	return prop

def gen_prop(prop_name, indexer) -> str:
	prop = str()
	prop += "\n"
	prop += "\t@property\n"
	prop += "\tdef {}(self) -> int:\n".format(prop_name)
	prop += "\t\treturn self.investments[{}]\n".format(indexer)
	prop += "\n"
	prop += "\t@{}.setter\n".format(prop_name)
	prop += "\tdef {}(self, value):\n".format(prop_name)
	prop += "\t\tself.investments[{}] = value\n".format(indexer)
	return prop


def gen_props(race: str):
	file_name = race + "_unit_types.txt"
	file_name = os.path.join(dir_path, file_name)
	try:
		with open(file_name, "r") as f:
			content = f.readlines()
	except Exception:
		return

	content = [x.strip() for x in content]

	file_name = os.path.join(dir_path, race + "_props.txt")
	with open(file_name, "w+") as f:
		indexer = index_start
		props = str()
		for prop_name in content:
			props += gen_prop(prop_name, indexer)
			indexer += 1

		props = gen_investment(indexer) + props
		f.write(props)

dir_path = os.path.dirname(os.path.realpath(__file__))

for race in "terran", "zerg", "protoss":
	gen_props(race)
