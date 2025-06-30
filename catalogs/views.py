from django.http import HttpResponse, FileResponse
from django.template import loader
from .models import Catalog
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CatalogSerializer
from openpyxl import Workbook

def catalogs(request):

  strFilter = str(request.GET.get("filter") or "")

  mycatalogs = Catalog.objects.filter(Q(name__contains=strFilter) | Q(title__contains=strFilter)).order_by('name') 

  paginator = Paginator(mycatalogs, 10)  
  page_number = request.GET.get("page") or 1
  page_mycatalogs = paginator.get_page(page_number)
  
  template = loader.get_template('all_catalog.html')
  context = {
    'page_mycatalogs': page_mycatalogs,
    'filter': strFilter 
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  myitem = Catalog.objects.get(id=id)
  template = loader.get_template('item_catalog.html')
  context = {
    'myitem': myitem,
  }
  return HttpResponse(template.render(context, request))

def SaveExcell(request):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Пословицы"
    catalog = mycatalogs = Catalog.objects.all()
    i = 1
    for elem in catalog:
        sheet['A'+str(i)] = elem.name
        sheet['B'+str(i)] = elem.title
        i = i + 1
    
    wb.save('Catalogs.xlsx')
    #return redirect("/catalogs")
    return FileResponse(open("Catalogs.xlsx", "rb"))


class CatalogAPI(APIView):
    def get(self, request, format=None):
        articles = Catalog.objects.all()
        serializer = CatalogSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            article = Catalog.objects.get(pk=pk)
        except Catalog.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CatalogSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            article = Catalog.objects.get(pk=pk)
        except Catalog.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())    
