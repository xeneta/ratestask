import config
import datetime
import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest


def get_db_conn(db_config):
    """ Create a database connection. """
    return psycopg2.connect(
        "dbname='{}' user='{}' host='{}'".format(
            db_config['name'],
            db_config['user'],
            db_config['host']
        )
    )

def create_app():
    """ Creat the server application """
    app = Flask(__name__)
    conn = get_db_conn(config.DB)


    def get_cursor():
        """ Get database dict cursor. """
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return cur


    def get_rows(query, params=None):
        """ Get all rows from a database query """
        cur = get_cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows


    def aggregate_to_dto(row):
        """ Transform a database dict row into a json serializable dict. """
        dto = {
            'price': float(row['price']) if row['price'] is not None else None,
            'day': row['day'].isoformat(),
            'count': row['count'],
        }
        return dto


    def parse_iso_date(value):
        """ Try to parse a value into a datetime """
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return value
        except:
            return None

    @app.route('/')
    def hello_world():
        return jsonify({
            'message': 'Hello world!'
        })


    @app.route('/rates', methods=['GET'])
    def get_rates():
        """
            Get average price per day in a timespan using portcode or region
            slugs.
        """
        orig_code = request.args.get('orig_code')
        dest_code = request.args.get('dest_code')
        orig_slug = request.args.get('orig_slug')
        dest_slug = request.args.get('dest_slug')
        date_from = parse_iso_date(request.args.get('date_from'))
        date_to = parse_iso_date(request.args.get('date_to'))

        if not date_from or not date_to:
            raise BadRequest('Invalid date arguments')
        if orig_code and dest_code:
            return get_rates_using_codes(
                date_from, date_to, orig_code, dest_code
            )
        if orig_slug and dest_slug:
            return get_rates_using_slugs(
                date_from, date_to, orig_slug, dest_slug
            )
        raise BadRequest('Invalid location arguments')


    def get_rates_using_codes(date_from, date_to, orig_code, dest_code):
        rows = get_rows('''
            SELECT
                CASE WHEN a.count < 3 THEN null ELSE a.price END AS price,
                d.day,
                a.count
            FROM
            (
                SELECT (generate_series(%(date_from)s, %(date_to)s, '1 day'::interval))::date as day
            ) d
            LEFT OUTER JOIN (
                SELECT AVG(price) AS price, day, COUNT(*) AS count
                FROM prices
                WHERE
                    orig_code = %(orig_code)s AND
                    dest_code = %(dest_code)s AND
                    day >= %(date_from)s AND
                    day <= %(date_to)s
                GROUP BY day, orig_code, dest_code
            ) AS a ON d.day = a.day
            ORDER BY day DESC ''',
            {
                'date_from': date_from,
                'date_to': date_to,
                'orig_code': orig_code,
                'dest_code': dest_code
            })

        rates = [aggregate_to_dto(row) for row in rows]
        return jsonify({ "rates": rates})


    def get_rates_using_slugs(date_from, date_to, orig_slug, dest_slug):
        rows = get_rows('''
            SELECT
                CASE WHEN a.count < 3 THEN null ELSE a.price END AS price,
                d.day,
                a.count
            FROM
            (
                SELECT (generate_series(%(date_from)s, %(date_to)s, '1 day'::interval))::date as day
            ) d
            LEFT OUTER JOIN (
                SELECT AVG(pr.price) AS price, pr.day, COUNT(*) as count
                FROM prices pr
                WHERE
                    orig_code IN (
                        SELECT p.code FROM ports p JOIN (
                            WITH RECURSIVE tree AS (
                                SELECT slug, ARRAY[]::text[] AS ancestors
                                FROM regions WHERE parent_slug IS NULL

                                UNION ALL

                                SELECT regions.slug, (tree.ancestors || regions.parent_slug) as ancestors
                                FROM regions, tree
                                WHERE regions.parent_slug = tree.slug
                            ) SELECT slug FROM tree where %(orig_slug)s = ANY(tree.ancestors) or tree.slug = %(orig_slug)s
                        ) s ON s.slug = p.parent_slug
                    ) AND
                    dest_code IN (
                        SELECT p.code FROM ports p JOIN (
                            WITH RECURSIVE tree AS (
                                SELECT slug, ARRAY[]::text[] AS ancestors
                                FROM regions WHERE parent_slug IS NULL

                                UNION ALL

                                SELECT regions.slug, (tree.ancestors || regions.parent_slug) as ancestors
                                FROM regions, tree
                                WHERE regions.parent_slug = tree.slug
                            ) SELECT slug FROM tree where %(dest_slug)s = ANY(tree.ancestors) or tree.slug = %(dest_slug)s
                        ) s ON s.slug = p.parent_slug
                    ) AND
                    day >= %(date_from)s AND
                    day <= %(date_to)s
                GROUP BY day
            ) AS a ON d.day = a.day
            ORDER BY day DESC ''',
            {
                'date_from': date_from,
                'date_to': date_to,
                'orig_slug': orig_slug,
                'dest_slug': dest_slug
            })

        rates = [aggregate_to_dto(row) for row in rows]
        return jsonify({ "rates": rates})

    return app
