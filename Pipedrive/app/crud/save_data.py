from ..core.config import API_TOKEN
from .get_data import GetData
import requests
import json

class SaveData:

    def __init__(self, cur, conn, table_m = 'activity_comercial'):
        self.api_token = API_TOKEN
        self.cur = cur
        self.conn = conn
        self.table_m = table_m

    def __add_columns(self, table, _dict, tipo) -> any:
        '''Adicionar colunas faltantes no banco de dados e retornar lista ou string com as colunas da tabela'''

        self.cur.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
        columns = self.cur.fetchall()
        table_columns = [x[0] for x in columns]

        list_columns = list(_dict.keys())
        str_columns = ','.join(map(str, list_columns))

        lista_final = list(set(list_columns) - set(table_columns))
        
        for coluna in lista_final:
            self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {coluna} INT;")
        self.conn.commit()
        res = str_columns if tipo == 'str' else list_columns # Retorna os nomes das colunas em str ou list, conforme é passado a variável 'tipo' como parâmetro da função
        return res

    def save_activity(self, request) -> None :
        '''Salvar atividades feitas em cada lead pelo analista comercial'''

        try:
            owner_name = request['current'].get('owner_name')
            user_id = request['meta'].get('user_id')
            deal_id = request['current'].get('deal_id')
            deal_title = request['current'].get('deal_title')
            activity = request['current'].get('type')
            type_name = request['current'].get('type_name')
            subject = request['current'].get('subject')
        except:
            deal_id = 'None'

        if deal_id != 'None':
            token = {
                'api_token': API_TOKEN
            }

            get_url = f'https://api.pipedrive.com/v1/deals/{deal_id}'

            get_response = requests.get(get_url, params=token)
            get_content = json.loads(get_response.content)

            stage = get_content['data'].get('stage_id')

            query_m = f"INSERT INTO {self.table_m} (owner_name, user_id, deal_id, deal_title, activity, type_name, subject, stage) VALUES ('{owner_name}','{str(user_id)}','{str(deal_id)}','{deal_title}','{activity}','{type_name}','{subject}','{stage}');"
            self.cur.execute(query_m)
            self.conn.commit()

    def save_data(self, request) -> None:
        '''Salvar/atualizar/deletar dados do banco de dados'''

        try:
            _id = request['current']['id']
        except:
            _id = 0
        
        if _id != 0:
            dict_metrics = GetData.get_data(request)

            query_count_lead = f"SELECT deal_id FROM pipedrive_metrics WHERE cpf = '{dict_metrics['cpf']}';"
            self.cur.execute(query_count_lead)
            count_lead = self.cur.fetchall()
            qtd_operacoes_lead = len(count_lead)
            lead_recorrente = 'novo' if qtd_operacoes_lead == 0 else 'recorrente'

            dict_metrics['lead_recorrente'] = lead_recorrente
            dict_metrics['qtd_operacoes'] = qtd_operacoes_lead

            query_count_client = f"SELECT deal_id FROM pipedrive_metrics WHERE cpf = '{dict_metrics['cpf']}' and status = 'won';"
            self.cur.execute(query_count_client)
            count_client = self.cur.fetchall()
            qtd_operacoes_client = len(count_client)
            cliente_recorrente = 'novo' if qtd_operacoes_client == 0 else 'recorrente'

            dict_metrics['cliente_recorrente'] = cliente_recorrente

            # Verificar se há duplicatas
            query_m = f"SELECT deal_id, stage_id, status FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}' and stage_id = '{dict_metrics['stage_id']}' and status = '{dict_metrics['status']}';"
            self.cur.execute(query_m)
            count_m = self.cur.fetchall()
            
            if (dict_metrics['status'] != 'open') and (len(count_m) == 0):
                lista = []
                for _ in range(len(dict_metrics)):
                    lista.append('%s')
                list_to_str = ','.join(map(str, lista))

                str_columns_m = self.__add_columns(self.table_m, dict_metrics, 'str')

                query_p = f"DELETE FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}';"
                self.cur.execute(query_p)
                self.conn.commit()

                try:
                    query_m = f"INSERT INTO {self.table_m} ({str_columns_m}) VALUES ({list_to_str});"
                    self.cur.execute(query_m, list(tuple(dict_metrics.values())))
                    self.conn.commit()
                except:
                    pass

            elif (dict_metrics['status'] == 'open') and (len(count_m) == 0):
                lista = []
                for _ in range(len(dict_metrics)):
                    lista.append('%s')
                list_to_str = ','.join(map(str, lista))

                str_columns = self.__add_columns(self.table_m, dict_metrics, 'str')

                query = f"SELECT deal_id, status FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}' and status != 'open';"
                self.cur.execute(query)
                content = self.cur.fetchall()

                if len(content) == 0:
                    query_p = f"DELETE FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}';"
                    self.cur.execute(query_p)
                    self.conn.commit()
                    try:
                        dict_metrics['valor_aprovado'] = None
                        query = f"INSERT INTO {self.table_m} ({str_columns}) VALUES ({list_to_str});"
                        self.cur.execute(query, list(tuple(dict_metrics.values())))
                        self.conn.commit()
                    except:
                        pass
        else:
            try:
                query_p = f"UPDATE {self.table_m} SET status = 'deleted' WHERE deal_id = '{request['previous']['id']}';"
                self.cur.execute(query_p)
                self.conn.commit()
            except:
                pass


                

