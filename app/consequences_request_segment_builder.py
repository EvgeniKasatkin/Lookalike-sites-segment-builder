import os
import pandas as pd
import requests
from tqdm import tqdm
import json
import time
import random
from dotenv import load_dotenv, find_dotenv
import ast

load_dotenv(find_dotenv())


class ChatGPTRequests:
    def __init__(self, rapidapi_headers):
        self.rapidapi_headers = rapidapi_headers

    def chat_GPT_function(self):
        url = os.getenv('rapidapi_chatgpt_url') #Url like https://chatgpt-api6.p.rapidapi.com/standard-gpt
        headers = self.rapidapi_headers
        no_parse_sites_df = pd.read_csv(os.getenv('file_of_sites')) #virtual env txt file of sorted and no requested sites
        list_of_site = list(no_parses_site_df['site'])

        query_to_chatGPT = 'Give me the top-10 of most similar sites like ' + str(list_of_site[0]) + 'in' + str(os.getenv('segment_of_markets')) + ' and for ' +  str('language_jurisdiction') + 'language persons with link'

        payload = { "conversation": [
    			    {
    				    "role": "user",
    				    "content": query_to_chatGPT
    			    }
    		                         ]
                  }
        response = requests.post(url, json=payload, headers=headers)
        try:
            suc_flg = response.json()['success']
            len_flg = len(str(response.json()['answer']['content']))
            if suc_flg == True and len_flg > 0:
                with open(str(os.getenv('url_of_files_of_consequences_requests')), 'a+') as f: #File of results of consequences requests
                    f.write(query_to_chatGPT + '\t' +  str(response.json()) + '\n')
                return 'FILE from chatGPT downloaded sucsessfully'
            else:
                time.sleep(5)
                return 'FILE from chatGPT no download (unsucsessfully)'
        except:
            try:
                if response.json()['success'] == False:
                    time.sleep(10)
            except:
                if response.status_code == 504:
                    time.sleep(60)

class ParsersAndFormerNewLists:

    def shape_of_all_files(self, cons_requests_file_path, outputs_data_sites):
        input_query_site, output_query_site, rank_list, site_name_list, link_site_list = [], [], [], [], []
        df_responses = pd.read_csv(cons_requests_file_path, delimiter='\t')
        query_site = str(list(df_responses.tail(1)['Query'])[0])[
				        str(list(df_responses.tail(1)['Query'])[0]).find('sites like') + 11: str(
					    list(df_responses.tail(1)['Query'])[0]).find(' for' + str(os.getenv('language_jurisdiction')) +  'language')]

        res = ast.literal_eval(list(df_responses.tail(1)['Response'])[0])
        http_flg = 0
        for ind_ in range(len(str(res['answer']['content']).split('\n'))):
            if 'http' in str(res['answer']['content']).split('\n')[ind_]:
                try:
                    rank = str(res['answer']['content']).split('\n')[ind_][
	    				   0:str(res['answer']['content']).split('\n')[ind_].find('. ')]
                except:
                    rank = 'undefined'
                try:
                    site_name = str(res['answer']['content']).split('\n')[ind_][
	    						str(res['answer']['content']).split('\n')[ind_].find('. ') + 2:
	    						str(res['answer']['content']).split('\n')[ind_].find(' -')]
                except:
                    site_name = 'undefined'
                try:
                    link = str(res['answer']['content']).split('\n')[ind_][
			    		   str(res['answer']['content']).split('\n')[ind_].find(' -') + 3:]
                except:
                    link = 'undefined'

                input_query_site.append(query_site)
                output_query_site.append(str(res['answer']['content']).split('\n')[ind_])
                rank_list.append(rank)
                site_name_list.append(site_name)
                link_site_list.append(link)
                http_flg = 1

	    if http_flg == 1:
		    df = pd.DataFrame({
			    'Input site': input_query_site,
			    'Output site': output_query_site,
			    'Rank': rank_list,
			    'Site_name': site_name_list,
			    'Link': link_site_list
		    })
		    df['Name_plus_Link'] = df['Site_name'] + ' ' + df['Link']
		    df_old_data = pd.read_csv(outputs_data_sites)
		    df_all = pd.concat([df_old_data, df])
		    df_all.to_csv(outputs_data_sites, index = False)
		    return 'Main data sites updated'
	    return 'Main data sites NO updated'

    def form_no_parse_list(self, url_of_files_of_outputs_data_sites, file_of_sites):
	    df = pd.read_csv(url_of_files_of_outputs_data_sites)
	    exists_sites = list(df['Input site'].drop_duplicates())
	    potential_sites = list(df['Name_plus_Link'].drop_duplicates())
	    no_parse_sites_list = []
	    for p_site in potential_sites:
		    exists_flg = 0
		    for e_site in exists_sites:
			    if p_site == e_site:
				    exists_flg = 1
				    break
		    if exists_flg == 0:
			    no_parse_sites_list.append(p_site)
	    no_parse_sites_df = pd.DataFrame({'site': no_parse_sites_list}).to_csv(file_of_sites, index=False)
	    return 'Parser reserv list updated', len(no_parse_sites_list)


if __name__ == "__main__":
    parse_and_form = ParsersAndFormerNewLists()
    status, total = parse_and_form.form_no_parse_list(str(os.getenv('url_of_files_of_outputs_data_sites')), str(os.getenv('file_of_sites')))
    while total > 0 and status == 'Parser reserv list updated':
        status_GPT = ChatGPTRequests.chat_GPT_function(os.getenv('rapidapiheaders'))
        if status_GPT == 'FILE from chatGPT downloaded sucsessfully':
            Status_update_main_data = parse_and_form.shape_of_all_files(str(os.getenv('url_of_files_of_consequences_requests')), str(os.getenv('url_of_files_of_outputs_data_sites')))
        else:
            time.sleep(10)
        status, total = parse_and_form.form_no_parse_list(str(os.getenv('url_of_files_of_outputs_data_sites')), str(os.getenv('file_of_sites')))



