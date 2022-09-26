from typing import Dict
import requests
import json
from ..models import dbmodel
from .treatment import treatment
from ..core.config import API_TOKEN

class GetData:

    def __api_data(deal) -> any:
        '''Obter dados provenientes da API e retorná-los'''

        token = {
            'api_token': API_TOKEN
        }
        get_url = f'https://nagro.pipedrive.com/api/v1/deals/{deal}'

        get_response = requests.get(get_url, params=token)

        get_content = json.loads(get_response.content)
        
        return get_content

    @classmethod
    def get_data(self, request) -> Dict:
        '''Obter dados provenientes do Webhook e retornar um dicionário'''

        deal_id =                  request['current'].get('id')
        deal_name =                request['current'].get('title')                                     
        age =                      request['current'].get('6810577fad4b85906d2d5143aa81d4c7c21a0b0f')  
        status =                   request['current'].get('status')                                    
        stage_id =                 request['current'].get('stage_id')                                  
        action =                   request['current'].get('action')                                    
        installments =             request['current'].get('997113147c4a51d84eef10b9f947b85be79eef8b')
        owner =                    request['current'].get('owner_name')                                
        pipeline_id =              request['current'].get('pipeline_id')                               
        update_time =              request['current'].get('update_time')                               
        add_time =                 request['current'].get('add_time')                                 
        utm_term =                 request['current'].get('adf3c645b694d779817bd8184f407c39055c9838')
        utm_source =               request['current'].get('521eaa686910d2b8b126298d32299fe6753a48c8')  
        utm_medium =               request['current'].get('45cbdaf0c572df1f8473d34efe86d56863d42022')  
        utm_campaign =             request['current'].get('7569772c5d6840ecb5fd5adbbb45eef70f18c370')  
        utm_content =              request['current'].get('b3256627eac0b4660f4b3cd322fb335030cda5a3')  
        fonte_lead =               request['current'].get('c2ab9cb7bc249fb9d38165fd2459ca53d2a7cb46')   
        subdominio_conversao =     request['current'].get('4dde5c9a449d6be4ddadb4158a0460bf11cb5cc1')  
        valor_pretendido =         request['current'].get('12ec4a94ffff9ca57294a279ee37dcf0959b8ada')  
        valor_aprovado =           request['current'].get('value')
        valor_liq_liberado =       request['current'].get('4345ea4f120dd4920d535ebde31d875d33910a28')  
        carencia_mensal =          request['current'].get('07c9b8ac63a8592fbcbf4d04c4fc70fee4f1fe6c')  
        garantia =                 request['current'].get('d6a0929d3d1da72acbbb398703b7f2af090c717a')  
        renda_mensal =             request['current'].get('2c93a0839708a41dde44b94194ee9b70ddd4ddde')  
        divida_scr_prejuizo =      request['current'].get('9cbda042a7173818997a4a3bdab6592d7685ab3e')  
        divida_scr_atrasada =      request['current'].get('1780fc5896dd07430431df88bab33a9237a21708')  
        divida_rural_scr =         request['current'].get('f898b00371d589905773a0d955426a55b253f25a')  
        divida_total_scr =         request['current'].get('99749581870a68eb1f954a8342c01305bb478c86')  
        cultura =                  request['current'].get('a41155dac32cee97f69c473d30fb3756b72cbae3')  
        atividade_rural =          request['current'].get('48fbf0ba6afda8967ca5d6b2c278c5b0190be6b9')  
        motivo_perda =             request['current'].get('lost_reason')                               
        score_bvs =                request['current'].get('e642adbbcbf0ba8617964dd75c8137dd002dae72')  
        aprovacao_scr =            request['current'].get('2007196288170325416b1881ab7ec9f3209a869a')  
        inscricao_produtor_ativa = request['current'].get('957522c0f6c528ec0de2104004536de049c2c3d3')  
        area_propria =             request['current'].get('6b43be2acca486154c3910d7c970efa604f768bb')  
        imoveis_proprios =         request['current'].get('e8393f57687788a1b8ebe397079ab681cefa97de') 
        autorizacao_scr =          request['current'].get('1d47b5db5538f298b3d3dd470f93abc70d79dab0')  
        op_credito_ativo =         request['current'].get('a2a89eae0b340143f857f30a6db1bd244cc4935b')  
        tempo_experiencia =        request['current'].get('d8136896f5dc14ffaedb06c63bbd3ea01ea987f8')  
        segmento =                 request['current'].get('65cb6fe62b8d4ef1df4afb78f05bf7b7ad3bf2db')   
        restricao_credito =        request['current'].get('c5fdcac211a155fe87388207c689f9c162827098')  
        juros =                    request['current'].get('eb755970dea5fd0c7976d854348880fa755ab95b')  
        uf =                       request['current'].get('dfe31eb818bbd0f146feaf909a45c9a0d88097bf')
        genero =                   request['current'].get('c0d400587de98966d4a5776ea5ac24ffe9342bb0')
        estado_solicitacao =       request['current'].get('f5730fd773dee64040204b00160c9b6cb4f9719e')
        won_time =                 request['current'].get('won_time')
        criador =                  request['current'].get('creator_user_id')
        op_endividamento_rural =   request['current'].get('1feb0315231800eb870f59599cd78f7dff3531f2')
        nr_contato =               request['current'].get('21a9d50748dda56a6c87f7b4432fa10dc0fe2b35')
        email =                    request['current'].get('c79ef1cfeb9a6c3ff0d9d38694e7d9449f3d75c2')
        cpf =                      request['current'].get('c88631d6bdeeaf470038008742ef1a0aa104fc9e')
        cidade_solicitacao =       request['current'].get('a8f47a5db3aefcb78d0cd31cb132fa376626aec7')

        utm_source = treatment('utm_source',utm_source)
        fonte_lead = treatment('fonte_lead',fonte_lead)
        subdominio_conversao = treatment('subdominio_conversao',subdominio_conversao)
        valor_pretendido = treatment('valor_pretendido',valor_pretendido)
        installments = treatment('installments',installments)
        add_time = treatment('add_time',add_time)
        update_time = treatment('update_time',update_time)
        won_time = treatment('won_time',won_time)
        cpf = treatment('cpf',cpf)

        modelo = dbmodel.DbModelMetrics(deal_id=deal_id,deal_name=deal_name,age=age,status=status,stage_id=stage_id,action=action, \
            installments=installments,owner=owner,pipeline_id=pipeline_id,add_time=add_time,update_time=update_time,utm_term=utm_term, \
            utm_source=utm_source,utm_medium=utm_medium,utm_campaign=utm_campaign,utm_content=utm_content,fonte_lead=fonte_lead, \
            subdominio_conversao=subdominio_conversao,valor_pretendido=valor_pretendido,valor_aprovado=valor_aprovado,valor_liq_liberado=valor_liq_liberado, \
            carencia_mensal=carencia_mensal,garantia=garantia,renda_mensal=renda_mensal,divida_scr_prejuizo=divida_scr_prejuizo, \
            divida_scr_atrasada=divida_scr_atrasada,divida_rural_scr=divida_rural_scr,divida_total_scr=divida_total_scr,cultura=cultura, \
            atividade_rural=atividade_rural,motivo_perda=motivo_perda,score_bvs=score_bvs,aprovacao_scr=aprovacao_scr,inscricao_produtor_ativa=inscricao_produtor_ativa, \
            area_propria=area_propria,imoveis_proprios=imoveis_proprios,autorizacao_scr=autorizacao_scr,op_credito_ativo=op_credito_ativo, \
            tempo_experiencia=tempo_experiencia,segmento=segmento,restricao_credito=restricao_credito,juros=juros,uf=uf,genero=genero, \
            estado_solicitacao=estado_solicitacao,won_time=won_time,criador=criador,op_endividamento_rural=op_endividamento_rural,nr_contato=nr_contato, \
            email=email,cpf=cpf,cidade_solicitacao=cidade_solicitacao)

        dict_metrics = modelo.dict()

        if status != 'open':
            get_content = self.__api_data(deal_id)
            stages = get_content['data']['stay_in_pipeline_stages']['times_in_stages']
            time_stages = {}
            for i in stages:
                time_stages[f'stage_{i}'] = stages[i]
            dict_metrics.update(time_stages)

        return dict_metrics
