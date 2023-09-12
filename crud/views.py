
'''
Código apenas para testar manualmente se há conexão entre Front, back e BD
'''

import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.db import models


# Isso aqui é a declaração de uma tabela do BD
class Nomes(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    

# Retornando o html da página inicial
def homepage(request):
    return render(request, 'crud.html')

# Retorna para o front os nomes registrados
def update(request):
    dbRes = Nomes.objects.all()
    nomes = []
    for nome in dbRes:
        nomes.append(str(nome))
    return JsonResponse({'names': nomes})

# Recebe um nome do front, e guarda no Banco de dados
def save(request):
    if request.method == 'POST':
        postData = request.body.decode('utf-8')
        try:
            json_data = json.loads(postData)
            nome = json_data.get('name', '')

            novoNome = Nomes(nome=nome)
            novoNome.save()

            return HttpResponse()
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'JSON PARSING ERROR'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
