import db_handler
import constant

class PortsCollection:
    def __init__(self):
        self.ports = list()
        self.ports_cache = list()

    def set_ports_cache(self):
        query = '''
        SELECT code FROM public.ports
        '''

        handle = db_handler.DbHandle(constant.HOST, constant.PORT, constant.DATABASE, constant.USER, constant.PASSWD)
        handle.connect_db()
        query_result = handle.execute_query(query)
        handle.close_db_connection()

        self.ports_cache = [code[0] for code in query_result]

    def set_port_data(self, regions):
        query = '''
        SELECT code FROM public.ports
        WHERE parent_slug in ({0})
        '''.format(", ".join("'" + slug + "'" for slug in regions))

        handle = db_handler.DbHandle(constant.HOST, constant.PORT, constant.DATABASE, constant.USER, constant.PASSWD)
        handle.connect_db()
        query_result = handle.execute_query(query)
        handle.close_db_connection()

        self.ports = [code[0] for code in query_result]

        

    def all_parents(self, p):
        if p not in self.parents:
            return set()
        return set(self.parents[p] + [b for a in self.parents[p] for b in self.all_parents(a)])

    def get_parents(self, child_name):
        relation = {p: self.all_parents(p) for p in self.region}
        if child_name not in relation:
            return []
        final_parents = list(relation[child_name])
        final_parents = [parent for parent in final_parents if parent != None]
        return final_parents