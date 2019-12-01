from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import *
import urllib.parse
# Create your views here.

def index(request):

    list = []
    arrayForm = {
        "v_name": "",
        "e_name" : "",
        "director" : "",
        "tag" : "",
        "country" : "",
        "year" : "",
        "type" : 1,
    }
    number = 1
    if(request.POST):

        v_name = request.POST['v_name']
        e_name = request.POST['e_name']
        director = request.POST['director']
        country = request.POST['country']
        tag = request.POST['tag']
        year = request.POST['year']
        type = request.POST['type']
        if type == '1':
            c = " && "
        elif type == '2':
            c = " & "
        arrayForm = {
            "v_name" : v_name,
            "e_name" : e_name,
            "director" : director,
            "country" : country,
            "tag" : tag,
            "year" : year,
            "type" : int(type),
        }
        query = ""
        if v_name:
            query += "v_name:" + '\"' + v_name + '\"'
        if e_name:
            if query != "":
                query += c
            query += "e_name:" + '\"' + e_name + '\"'
        if director:
            if query != "":
                query += c
            query += "director:" + '\"' + director + '\"'
        if country:
            if query != "":
                query += c
            query += "country:" + '\"' + country + '\"'
        if tag:
            if query != "":
                query += c
            query += "tags:" + '\"' + tag + '\"'
        if year:
            if query != "":
                query += c
            query += "year:" + '\"' + year + '\"'
        print(query)
        solr_tuples = [
            ('q', query)
        ]
        conn = urlopen("http://localhost:8983/solr/core/select?" + urllib.parse.urlencode(solr_tuples))
        rsp = eval(conn.read())
        print(rsp)
        if rsp['response']['numFound'] != 0:
            count = 0
            list = []
            for doc in rsp['response']['docs']:
                if count < 20:
                    list.append(doc)
                    count += 1
                else:
                    break
        else:
            number = 0
    return render(request, "firstapp/index.html", {'list' : list, 'number': number, 'arrayForm': arrayForm})