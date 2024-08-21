from datetime import date, datetime, timedelta

from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Port, Price, Region
from .serializers import PortSerializer, PriceSerializer, RegionSerializer


class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    @action(detail=False, methods=['get'])
    def average_prices(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')

        if not all([date_from, date_to, origin, destination]):
            return Response({"error": "Missing parameters"}, status=400)

        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Check if date_to is greater than the current date
        if date_to > date.today():
            return Response({"error": "The 'date_to' parameter cannot be greater than the current date."}, status=400)

        with connection.cursor() as cursor:
            sql = '''
            SELECT day, ROUND(AVG(price),2) as average_price
            FROM prices
            WHERE day BETWEEN %s AND %s
            AND orig_code IN (
                SELECT code FROM ports WHERE code = %s OR parent_slug IN (
                    SELECT slug FROM regions WHERE slug = %s
                )
            )
            AND dest_code IN (
                SELECT code FROM ports WHERE code = %s OR parent_slug IN (
                    SELECT slug FROM regions WHERE slug = %s
                )
            )
            GROUP BY day
            HAVING COUNT(*) >= 3;
            '''
            params = [date_from, date_to, origin, origin, destination, destination]
            cursor.execute(sql, params)
            result = cursor.fetchall()

        response = [{'day': row[0].strftime('%Y-%m-%d'), 'average_price': row[1] if row[1] is not None else None} for row in result]

        day_range = [date_from + timedelta(days=x) for x in range((date_to - date_from).days + 1)]
        response_dict = {day.strftime('%Y-%m-%d'): None for day in day_range}

        for entry in response:
            response_dict[entry['day']] = entry['average_price']

        final_response = [{'day': k, 'average_price': v} for k, v in response_dict.items()]

        return Response(final_response)
