import os

index_start = 0
dir_path = os.path.dirname(os.path.realpath(__file__))


def gen_investment(race: str, indexer: int) -> str:
	prop = str()
	prop += "\n"
	prop += "class {}Investments(Investments):".format(race)
	prop += "\n"
	prop += "\tinvestments: np.ndarray = None\n"
	prop += "\n"
	prop += "\tdef num_values(self) -> int:\n"
	prop += "\t\treturn {}\n".format(indexer)
	prop += "\n"
	prop += "\tdef __init__(self):\n"
	prop += "\t\tself.investments = np.full(self.num_values(), 0)\n"
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


def gen_props() -> str:
	all_props = ""
	for race in "Terran", "Zerg", "Protoss":
		file_name = race.lower() + "_unit_types.txt"
		file_name = os.path.join(dir_path, file_name)
		try:
			with open(file_name, "r") as f:
				content = f.readlines()
		except Exception:
			break

		content = [x.strip() for x in content]

		indexer = index_start
		props = ""
		for prop_name in content:
			props += gen_prop(prop_name, indexer)
			indexer += 1
		all_props += gen_investment(race, indexer) + props

	return all_props


file_name = os.path.join(dir_path, "race_props.txt")
with open(file_name, "w+") as f:
	data = gen_props()
	f.write(data)
