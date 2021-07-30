from flask import Flask, request, jsonify
from psycopg2 import connect

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route('/rates', methods=['GET'])
def rates():
  raw_args = request.args.to_dict()

  return jsonify(raw_args)


if __name__ == '__main__':
  app.run()