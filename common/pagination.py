from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SettingsPageNumberPagination(PageNumberPagination):
    """
    Class for basic page pagination settings

    Attributes:
        page_query_param (str): The name of the page number parameter in the URL.
        page_size_query_param (str): The name of the page size parameter in the URL.
        max_page_size (int): The maximum number of items per page.
        page_size (int): The default number of items per page.
    """
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_size = 10

    def get_paginated_response(self, data):
        """
        Customized pagination response

        Args:
            data (list): The paginated data to be included in the response.

        Returns:
            Response: A customized pagination response containing the following keys:
                - 'results': The paginated data provided as an argument.
                - 'total_pages': The total number of pages in the paginated data.
                - 'count': The total number of items across all pages.
                - 'links': A dictionary containing 'next' and 'previous' links for navigation.
        """
        return Response({
            'results': data,
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            }
        })


def get_serializer_paginate(instance, queryset, serializer):
    """
    Paginate and serialize a queryset based on the provided serializer.

    This function is used to paginate a queryset and serialize the results using a specified serializer. It checks if
    pagination is needed and returns the appropriate response.

    Args:
        instance (object): The view instance where the method is called.
        queryset (QuerySet): The queryset containing the data to be serialized.
        serializer (Serializer): The serializer class used to serialize the data.

    Returns:
        Response: A response object containing the serialized data with pagination information if applicable.

    Example Usage:
    get_serializer_paginate(self, queryset, UserSerializer)
    """
    # check if pagination is required for the queryset
    page = instance.paginate_queryset(queryset=queryset)

    if page is not None:
        # if pagination is needed, serialized and paginated data
        serializer = serializer(page, many=True)
        return instance.get_paginated_response(data=serializer.data)

    # if pagination is not needed, serialized the entire queryset
    serializer = serializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
