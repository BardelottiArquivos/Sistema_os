from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .services import ViaCEPService

@login_required
@require_GET
def consultar_cep(request):
    cep = request.GET.get('cep', '')
    if not cep:
        return JsonResponse({'error': 'CEP não informado'}, status=400)
    
    dados = ViaCEPService.consultar_cep(cep)
    if dados:
        return JsonResponse(dados)
    return JsonResponse({'error': 'CEP não encontrado'}, status=404)
