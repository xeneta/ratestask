from flask import Flask, request, jsonify
import logging
import worker
import Regions, Ports



app = Flask(__name__)
app.cache = {}

app.cache['Regions'] = Regions.RegionCollection() 
app.cache['Regions'].set_region_data()
app.cache['Ports'] = Ports.PortsCollection()
app.cache["Ports"].set_ports_cache()


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/rates', methods=['GET'])
def rates():
    args = request.args.to_dict()
    extracted_params, error = worker.parameter_extractor(args)
    if error != None:
        return error, 400

    final_params, error = worker.parameter_value_compiler(extracted_params)
    if error != None:
        return error, 400
    
    final_response, error = worker.get_average_price(final_params, app.cache['Regions'], app.cache["Ports"])
    if error != None:
        return error, 400

    return jsonify(final_response), 200


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug=False)