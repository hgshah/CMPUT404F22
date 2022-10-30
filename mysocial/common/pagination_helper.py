from typing import Any
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnDict
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage


class PaginationHelper:
    NO_PAGINATION_REQUEST = "NO_PAGINATION_REQUEST"

    @staticmethod
    def paginate_serialized_data(request: Request, data: ReturnDict) -> (Any, str):
        """
        Paginates serialized data.

        :param request: HTTPRequest from Django. We are expecting the query_parameters to contain:
            - page: an integer greater than zero telling which page to return
            - size: an integer greater than zero telling what size pages are
        :param data: ReturnDict in serializer.data from Django Serializers
        :return new_data: returns :new_data: which is either:
            - a list of object for successful paginations based on :data:, or
            - the original :data: if there were no pagination parameters in :request:
            - returns None is there was an error
        :return err: returns None if successful but returns a string error message if validation
            failed or an error occurred

        Example how to use::

            data, err = PaginationHelper.paginate_serialized_data(request, data)
            if err is None:
                # do successful logic
            else:
                # should do unsuccessful logic

        """
        should_paginate = 'page' in request.query_params or 'size' in request.query_params

        if not should_paginate:
            return data, None

        # failing query param validation should return 404 since this is user-facing
        # note: validation here also means that if either of the query params are missing, we fail
        page = 1
        size = 1

        try:
            page = int(request.query_params['page'])
            if page < 1:
                return "page should be greater than or equal to 1"

            size = int(request.query_params['size'])
            if size < 1:
                return "size should be greater than or equal to 1"
        except Exception as err:
            return None, str(err)

        paginator = Paginator(data, size)
        try:
            return paginator.page(page).object_list, None
        except EmptyPage:
            return (), 'Page is empty'
        except PageNotAnInteger:
            return (), 'Page is not an integer'
        except InvalidPage:
            return (), 'Invalid page'
        except Exception as err:
            return (), str(err)
