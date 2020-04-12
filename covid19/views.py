from django.http import HttpResponse
from silk.models import Response as Silk
from silk.profiling.profiler import silk_profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .estimator import estimator


# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@silk_profile(name="get_json")
def get_json(request):
    output = estimator(request.data)
    return Response(output, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
@renderer_classes([XMLRenderer])
@silk_profile(name="get_xml")
def get_xml(request):
    output = estimator(request.data)
    return Response(output, status=status.HTTP_200_OK, content_type='application/xml')


@api_view(['GET'])
def get_logs(request):
    output = ""
    valid_path = ['/api/v1/on-covid-19',
                  '/api/v1/on-covid-19/',
                  '/api/v1/on-covid-19/json',
                  '/api/v1/on-covid-19/xml',
                  '/api/v1/on-covid-19/logs']
    for obj in Silk.objects.all():
        method = obj.request.method
        path = obj.request.path
        if path not in valid_path:
            continue
        status_code = obj.status_code
        time_taken = round(obj.request.time_taken)
        output += "{0}\t\t{1}\t\t{2}\t\t{3} ms\n".format(method,
                                                         path,
                                                         status_code,
                                                         time_taken)
    return HttpResponse(output, status=status.HTTP_200_OK, content_type='text/plain')
