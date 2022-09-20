from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class myCursorPagination(PageNumberPagination):
    page_size = 7
    def get_paginated_response(self, data):
        try:
            return Response({
                'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'results': data
            })
        except:
    # return here any message you want
            return Response({
                "code": 400,
                "error": "Page out of range"
            })