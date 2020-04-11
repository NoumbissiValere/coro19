import time
from django.utils.html import format_html_join
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .estimator import estimator
from .models import ResponseTime

# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_json(request):
    t1 = int(round(time.time() * 1000.0))
    output = estimator(request.data)
    response = Response(output, status=status.HTTP_200_OK,
                        content_type='application/json')
    method = request.method
    path = request.path
    status_code = response.status_code
    t2 = int(round(time.time() * 1000.0))
    t = "{} ms".format(t2 - t1)
    ResponseTime.objects.create(
        method=method, path=path, status=status_code, time=t)
    return response


@api_view(['POST'])
@renderer_classes([XMLRenderer])
def get_xml(request):
    t1 = int(round(time.time() * 1000.0))
    output = estimator(request.data)
    response = Response(output, status=status.HTTP_200_OK,
                        content_type='application/xml')
    method = request.method
    path = request.path
    status_code = response.status_code
    t2 = int(round(time.time() * 1000.0))
    t = "{} ms".format(t2 - t1)
    ResponseTime.objects.create(
        method=method, path=path, status=status_code, time=t)
    return response


@api_view(['GET'])
def get_logs(request):
    output = []
    for obj in ResponseTime.objects.all():
        output.append("{0}    {1}    {2}    {3}".format(
            obj.method, obj.path, obj.status, obj.time))
    return Response("\n".join(output), status.HTTP_200_OK, content_type='text/plain')
