import math
from pprint import pprint

import hubspot
import pandas as pd
from hubspot.crm.companies import (ApiException,
                                   BatchInputSimplePublicObjectId,
                                   BatchReadInputSimplePublicObjectId)
from numpy import array_split


def setup_client():
    api_client = hubspot.Client.create()
    api_client.access_token = "pat-na1-a9496a1d-02e4-48d7-aebb-bc5abe0ddee7"
    # api_client.access_token = "" ## Prod
    return api_client


def batch_read_companies(api_client, company_ids):
    properties = None
    default_properties = ["vamp_team_id", "team_type", "name", "id"]
    properties = default_properties if properties is None else properties

    company_ids = [{'id': str(i)} for i in company_ids]
    pprint(company_ids)
    batch_read = BatchReadInputSimplePublicObjectId(properties=properties, id_property="vamp_team_id", inputs=company_ids)
    try:
        api_response = api_client.crm.companies.batch_api.read(batch_read_input_simple_public_object_id=batch_read, archived=False)
        pprint(api_response)
        return None
    except ApiException as e:
        print("Exception when calling batch_api->read: %s\n" % e)
        return e



def batch_archive_companies(api_client, company_ids):
    company_ids = [{'id': str(i)} for i in company_ids]
    pprint(company_ids)
    batch_input = BatchInputSimplePublicObjectId(inputs=company_ids)
    try:
        api_response = api_client.crm.companies.batch_api.archive(batch_input_simple_public_object_id=batch_input)
        pprint(api_response)
        return api_response
    except ApiException as e:
        print("Exception when calling batch_api->archive: %s\n" % e)
        return e


def read_file(file_path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    if(df.empty):
        print ('CSV file is empty')
    else:
        pprint("CSV Loaded and below are the data types.")
        pprint(df.dtypes)

    return df


def main():
    batch_size = 1
    api_client = setup_client()
    id_field_name = "id"
    data = read_file("companies_to_archive_error.csv")
    # data = data.head(batch_size)
    # data =  ['10317769397', '10317752119']
    if len(data) == 0:
        pprint(f"No data found")
    else:
        # data = data.replace({nan: None})
        # pprint(data[id_field_name].to_string())
        for create_batch in array_split(data[id_field_name], math.ceil(len(data[id_field_name])/batch_size)):
            response = batch_archive_companies(api_client, create_batch.to_numpy())
            if response != None:
                pprint("Something happened " + response)
                break
            else:
                data.tail(data.shape[0] - batch_size)
                continue


if __name__ == "__main__":
    main()