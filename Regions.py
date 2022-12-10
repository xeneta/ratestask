import db_handler
import constant

class RegionCollection:
    def __init__(self):
        self.region = set()
        self.parents = dict()

    def set_region_data(self):
        query = '''
        SELECT * FROM public.regions
        '''
        handle = db_handler.DbHandle(constant.HOST, constant.PORT, constant.DATABASE, constant.USER, constant.PASSWD)
        handle.connect_db()
        query_result = handle.execute_query(query)
        handle.close_db_connection()

        for p, k, c in query_result:
            self.parents.setdefault(p, []).append(c)
        self.region = set(self.parents)

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

regions = RegionCollection()
regions.set_region_data()
print(regions.get_parents('baltic'))

