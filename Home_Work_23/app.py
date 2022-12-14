import os
import re
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__)

def construct_query(cmd: str, value: str, data: list[str]) -> list:
	if cmd == "filter":
		result = list(filter(lambda x: value in x, data))
	if cmd == "map":
		col_um = int(value)
		if col_um == 0:
			result = list(map(lambda x: x.split()[col_um], data))
		elif col_um == 1:
			result = list(map(lambda x: x.split()[3] + x.split()[4], data))
		elif col_um == 2:
			result = list(map(lambda x: " ".join(x.split()[5:]), data))
		return result
	elif cmd == "unique":
		result = list(set(data))
	elif cmd == "sort":
		reverse = (value == 'desc')
		result = sorted(data, reverse=reverse)
	elif cmd == "limit":
		result = data[: int(value)]
	elif cmd == "regex":
		regex = re.compile(value)
		return list(filter(lambda v: re.search(regex, v), data))
	else:
		raise BadRequest
	return result


def do_query(params: dict) -> list:
	with open(os.path.join(DATA_DIR, params["file_name"])) as f:
		file_data = f.readlines()
	res = file_data
	if "cmd1" in params.keys():
		res = construct_query(params['cmd1'], params['value1'], res)
	if "cmd2" in params.keys():
		res = construct_query(params['cmd2'], params['value2'], res)
	if "cmd3" in params.keys():
		res = construct_query(params['cmd3'], params['value3'], res)
	return res
@app.route("/perform_query", methods=["POST"])
def perform_query():
	data: dict = request.json
	file_name: str = data["file_name"]
	if not os.path.exists(os.path.join(DATA_DIR, file_name)):
		raise BadRequest
	return jsonify(do_query(data))


if __name__ == '__main__':
	app.run()
