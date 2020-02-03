"""
Copyright 2019 ShipChain, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from django.conf import settings
from influxdb_metrics.loader import log_metric
from rest_framework import permissions, status, renderers

from rest_framework.response import Response
from rest_framework.views import APIView
from shipchain_common.exceptions import RPCError
from shipchain_common.pagination import CustomResponsePagination


from apps.permissions import get_owner_id

from ..iot_client import DeviceAWSIoTClient
from ..serializers import DevicesQueryParamsSerializer

LOG = logging.getLogger('transmission')


class ListDevicesStatus(APIView):
    http_method_names = ['get', ]
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = CustomResponsePagination
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        owner_id = get_owner_id(request)

        LOG.debug(f'Listing devices for owner with id: {owner_id}.')
        log_metric('transmission.info', tags={'method': 'devices.list', 'module': __name__})

        if not settings.IOT_THING_INTEGRATION:
            raise RPCError('IoT Integration is not set up in this environment.',
                           status_code=status.HTTP_501_NOT_IMPLEMENTED)

        iot_client = DeviceAWSIoTClient()

        serializer = DevicesQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        devices = iot_client.get_list_owner_devices(owner_id, serializer.validated_data)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(devices, request, view=self)
        if page is not None:
            return paginator.get_paginated_response(page)
        return Response(devices, status=status.HTTP_200_OK)