from flask import Flask, request, jsonify, current_app
import logging
import worker


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/rates', methods=['GET'])
def rates():
    extracted_params, error = worker.parameter_extractor(request.args.to_dict())
    if error != "" or error != None:
        return error, 400

    final_params, error = worker.parameter_value_compiler(extracted_params)
    if error != "" or error != None:
        return error, 400
    

    return final_params, 200


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)