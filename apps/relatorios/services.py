import os
from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class RelatorioService:
    @staticmethod
    def gerar_pdf(template_src, context_dict, filename='relatorio.pdf'):
        try:
            template = get_template(template_src)
            html = template.render(context_dict)
            result = BytesIO()
            
            from xhtml2pdf import pisa
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8')
            
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                logger.error(f"Erro ao gerar PDF: {pdf.err}")
                return None
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return None


class RelatorioOSService:
    @classmethod
    def gerar_relatorio_os(cls, ordem_servico):
        context = {
            'os': ordem_servico,
            'cliente': ordem_servico.cliente,
            'computador': ordem_servico.computador,
            'itens': ordem_servico.itens.all(),
            'data_emissao': datetime.now(),
            'tecnico': ordem_servico.tecnico_responsavel,
        }
        filename = f"OS_{ordem_servico.numero_os.replace('/', '_')}.pdf"
        return RelatorioService.gerar_pdf('relatorios/os_detalhada.html', context, filename)
    
    @classmethod
    def gerar_relatorio_periodo(cls, data_inicio, data_fim, status=None):
        # Importar dentro do método para evitar circularidade
        from apps.ordens_servico.models import OrdemServico
        
        ordens = OrdemServico.objects.filter(
            data_abertura__date__gte=data_inicio,
            data_abertura__date__lte=data_fim
        )
        
        if status:
            ordens = ordens.filter(status=status)
        
        total_os = ordens.count()
        total_valor = sum(os.valor_total for os in ordens)
        media_valor = total_valor / total_os if total_os > 0 else 0
        
        context = {
            'ordens': ordens,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_os': total_os,
            'total_valor': total_valor,
            'media_valor': media_valor,
            'data_emissao': datetime.now(),
        }
        
        filename = f"relatorio_periodo_{data_inicio}_{data_fim}.pdf"
        
        return RelatorioService.gerar_pdf('relatorios/os_periodo.html', context, filename)