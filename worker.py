def parameter_extractor(param_dict):
    required_params = [
      "date_from",
      "date_to",
      "origin",
      "destination"
    ]

    final_params = {param: param_dict[param] for param in  required_params}
    if len(final_params) != 4:
        missing_params = list()
        for param in required_params:
            if param not in param_dict:
                missing_params.append(param)

        if not missing_params:
            return "", f"The query misses these required parameter(s) : {','.join(missing_params)}"
        
        return final_params, ""



def parameter_value_compiler(extracted_params):
    for key in extracted_params:
        if not extracted_params[key].strip():
            return "", "No data given for parameter {0}.".format(key)
        if len(extracted_params[key]) == 5:
            extracted_params[key] = extracted_params[key].upper()
        else:
            extracted_params[key] = extracted_params[key].lower()

    return extracted_params


def get_average_price(parameters):
    # find all the parent regions of the 
    # find all the ports for the regions for start and destination ports respectively
    # find average price using sql query 
    pass



