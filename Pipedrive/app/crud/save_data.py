from ..core.config import API_TOKEN
from .get_data import GetData
import requests
import json

class SaveData:

    def __init__(self, cur, conn, table_m = 'activity_comercial'):
        '''Initializing the object's attributes'''
        self.api_token = API_TOKEN # To connect with Pipedrive
        self.conn = conn # To connect with Postgres
        self.cur = cur # The cursor from Postgres
        self.table_m = table_m # The table used to save the data

    def __add_columns(self, table, _dict, tipo) -> any:
        '''Add missing columns to database and return list or string with table columns'''
        
        # Getting all the columns in the table
        self.cur.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
        columns = self.cur.fetchall()
        table_columns = [x[0] for x in columns]
        
        # Converting in string or list
        list_columns = list(_dict.keys())
        str_columns = ','.join(map(str, list_columns))
        
        # Finding the missing columns
        lista_final = list(set(list_columns) - set(table_columns))
        
        # Adding new columns to the table
        for coluna in lista_final:
            self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {coluna} INT;")
        self.conn.commit()
        res = str_columns if tipo == 'str' else list_columns # Returns the column names in str or list, depending on the 'type' variable being passed as a function parameter
        return res

    def save_activity(self, request) -> None :
        '''Save activities performed on each lead by the business analyst'''
        
        valid = True
        
        # Getting data from webhook
        try:
            owner_name = request['current'].get('owner_name')
            user_id = request['meta'].get('user_id')
            deal_id = request['current'].get('deal_id')
            deal_title = request['current'].get('deal_title')
            activity = request['current'].get('type')
            type_name = request['current'].get('type_name')
            subject = request['current'].get('subject')
        except:
            valid = False

        if valid:
            # Connecting with Pipedrive to get the currently stage of the lead and saving in Database
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
        '''Save/update/delete database data'''
        
        valid = True
        
        # Verifying if there is an ID in the data from webhook, who doesn't have one it's because they have been deleted
        try:
            _id = request['current']['id']
        except:
            valid = False
        
        if valid:
            dict_metrics = GetData.get_data(request)
            
            # Finding out if the lead is new or recurring
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

            # Checking for duplicates
            query_m = f"SELECT deal_id, stage_id, status FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}' and stage_id = '{dict_metrics['stage_id']}' and status = '{dict_metrics['status']}';"
            self.cur.execute(query_m)
            count_m = self.cur.fetchall()
            
            # Inserting lead data according to their status

            if (dict_metrics['status'] != 'open') and (len(count_m) == 0):
                lista = []
                for _ in range(len(dict_metrics)):
                    lista.append('%s')
                list_to_str = ','.join(map(str, lista))

                str_columns_m = self.__add_columns(self.table_m, dict_metrics, 'str')

                query_p = f"DELETE FROM {self.table_m} WHERE deal_id = '{dict_metrics['deal_id']}';"
                self.cur.execute(query_p)
                self.conn.commit()
                   
                # Sometimes Pipedrive gives us repeated data, so the 'try' is used for avoiding the error
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
            # Setting 'deleted' status for leads who doesn't have an ID
            try:
                query_p = f"UPDATE {self.table_m} SET status = 'deleted' WHERE deal_id = '{request['previous']['id']}';"
                self.cur.execute(query_p)
                self.conn.commit()
            except:
                pass


                

