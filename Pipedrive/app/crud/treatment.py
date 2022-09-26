import re
from datetime import datetime, timedelta

def treatment(_type, value) -> any:
    '''Tratar os dados e retornar seu valor'''
    if value == None:
        pass
    elif value == '':
        value = None
    elif _type == 'utm_source':
        if value in ['facebook','Facebook_Desktop_Feed','Facebook_Instant_Articles','Facebook_Instream_Video','Facebook_Marketplace','Facebook_Mobile_Feed','Facebook_Stories','fb','fbclid','Messenger_Inbox','Messenger_Stories','msg','Others']:
            value = 'facebook'
        elif value == 'cs':
            value = 'atendimento'
        elif value in ['gclid','google']:
            value = 'google'
        elif value in ['ig','Instagram_Explore','Instagram_Feed','Instagram_Stories']:
            value = 'instagram'
        elif value == 'RD Station':
            value = 'email'
        elif value == 'recuperacao':
            value = 'recuperação'
        elif value == 'indicacao':
            value = 'indicação'
    elif _type == 'fonte_lead':
        if value in ['Indicação de Cliente - Time Comercial','Indicação de Cliente - Time CS']:
            value = 'indicação'
        elif value in ['Prospecção Ativa','Recuperação','Recuperação - Black Friday']:
            value = 'recuperação'
        elif value == 'Pré-pagamento':
            value = 'pré-pagamento'
        elif value == 'Renovação':
            value = 'renovação'
    elif _type == 'subdominio_conversao':
        if value in ['advertorial','capitalgiro','creditosafra']:
            value = 'facebook'
        elif value in ['ciadoleitecredprodutor','ciadoleitegiro','engenhodoce','nobresolu','piffer','rochainvestimentosgiro']:
            value = 'parcerias'
        elif value == 'credito':
            value = 'atendimento'
        elif value == 'gg':
            value = 'google'
        elif value in ['giroinstitucional','institucional']:
            value = 'institucional'
        elif value == 'indicacao':
            value = 'indicação'
        elif value == 'simulador':
            value = 'email'
        elif value == 'yt':
            value = 'youtube'
    elif _type == 'valor_pretendido':
        if value != None:
            value = value.replace('.','')
            value = value.replace(',','.')
            value = value[3:]
            value = float(value)
    elif _type == 'installments':
        value = re.sub('[^0-9]', '', value)
    elif _type in ['add_time','update_time','won_time']:
        temp_value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S') if value != None else None
        value = temp_value - timedelta(hours = 3)
    elif _type == 'cpf':
        value = re.sub('[.\-/]','',value)

    return value
