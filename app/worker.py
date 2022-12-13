import Ports
import db_handler
import constant

def parameter_extractor(param_dict):
    '''Extracts the required parameters from the parameters passed and checks if they exist'''
    required_params = [
      "date_from",
      "date_to",
      "origin",
      "destination"
    ]
    # Required parameter extraction
    final_params = {param: param_dict[param] for param in required_params}
    if len(final_params) != 4:
        missing_params = list()
        for param in required_params:
            if param not in param_dict:
                missing_params.append(param)
        if len(missing_params) > 0:
            return None, f"The query misses these required parameter(s) : {','.join(missing_params)}"
        
    return final_params, None



def parameter_value_compiler(extracted_params):
    '''Function that checks whether the parameter data is valid and also sanitize it for further data processing'''
    for key in extracted_params: 
        if not extracted_params[key].strip():
            return None, "No data given for parameter {0}.".format(key)
        if len(extracted_params[key]) == 5:
            extracted_params[key] = extracted_params[key].upper()
        else:
            extracted_params[key] = extracted_params[key].lower()

    return extracted_params, None


def get_average_price(parameters, region_data_object, ports_data_object): 
    '''Function to find the average price'''
    # find all the parent regions of the region
    # and find all the ports for the regions for start and destination ports respectively

    # Getting all origin regions
    origins, is_port = get_parents(parameters['origin'], region_data_object)
    if len(origins) == 0:
        return None, "No origin data found"
    if is_port == False:
        port_object = Ports.PortsCollection()
        # origins.append(parameters['origin'])
        port_object.set_port_data(origins)
        # getting all origin ports
        origins = port_object.ports
    elif origins[0] not in ports_data_object.ports_cache:
        return None, "Origin is invalid"


    destinations, is_port = get_parents(parameters['destination'], region_data_object) 
    if len(destinations) == 0:
        return None, "No destination data found"
    if is_port == False:
        port_object = Ports.PortsCollection()
        # destinations.append(parameters['destination'])
        port_object.set_port_data(destinations)
        destinations = port_object.ports
    elif destinations[0] not in ports_data_object.ports_cache:
        return None, "Destination is invalid"
    # find average price using sql query 

    # converting the ports list to string
    origins_as_string = ", ".join(["'" + origin + "'" for origin in origins])
    destinations_as_string = ", ".join(["'" + destination + "'" for destination in destinations])
    average_price_query_result = average_price_query(origins_as_string, destinations_as_string, parameters['date_from'],parameters['date_to'] , 3)
    return [i[0] for i in average_price_query_result], None

def get_parents(name, region_data_object):
    # check if its a port code
    code = list()
    is_port = False
    if len(name) == 5:
        code.append(name)
        is_port = True
    else:
        code = region_data_object.get_childrens(name)
        code.append(name)

    return code, is_port


def average_price_query(origins_as_string, destinations_as_string, from_date, to_date, minimum_days):
    price_per_day_query = '''
    WITH AVGPRICE as 
    (SELECT day,
    CASE
        WHEN COUNT(price) >= {0} THEN ROUND(AVG(price), 0)
        WHEN COUNT(price) < {0} THEN null
    END AS average_price
    FROM prices
    WHERE orig_code in ({1})
    AND dest_code in ({2})
    AND day >= '{3}'
    AND day <= '{4}'
    GROUP BY day
    ORDER BY day)
    SELECT TO_JSON(AVGPRICE)
    FROM AVGPRICE;
    '''.format(
        minimum_days,
        origins_as_string,
        destinations_as_string,
        from_date,
        to_date
    )

    handle = db_handler.DbHandle(constant.HOST, constant.PORT, constant.DATABASE, constant.USER, constant.PASSWD)
    handle.connect_db()
    query_result = handle.execute_query(price_per_day_query)
    handle.close_db_connection()
    return query_result



    





