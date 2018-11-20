"""
Copyright 2018 ShipChain, Inc.

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

from channels.db import database_sync_to_async
from enumfields import Enum
from rest_framework.renderers import JSONRenderer

from apps.authentication import AsyncJsonAuthConsumer
from .models import AsyncJob
from .serializers import AsyncJobSerializer


class EventTypes(Enum):
    error = 0
    asyncjob_update = 1


class JobsConsumer(AsyncJsonAuthConsumer):
    async def jobs_update(self, event):
        job_json = await database_sync_to_async(self.render_async_job)(event['async_job_id'])
        await self.send(job_json)

    def render_async_job(self, job_id):
        job = AsyncJob.objects.get(id=job_id)
        return JSONRenderer().render({'event': EventTypes.asyncjob_update.name,
                                      'data': AsyncJobSerializer(job).data}).decode()

    async def receive_json(self, content, **kwargs):
        await self.send_json({
            "event": EventTypes.error.name,
            "data": "This websocket endpoint is read-only",
        })