import json
import re
import os
import ast

# read file
with open('hashtag20231015.txt', 'r') as file:
    data = file.read()
data = data.split('b"')


def decode_utf8(item):
    if isinstance(item, str):  # If item is a string
        try:
            return item.encode('latin1').decode('utf-8')
        except:
            return item  # Return original if decoding fails
    elif isinstance(item, list):  # If item is a list
        return [decode_utf8(x) for x in item]
    elif isinstance(item, dict):  # If item is a dictionary
        return {key: decode_utf8(value) for key, value in item.items()}
    # If item is neither string, list nor dict (could be int, bool, etc.)
    else:
        return item


id_clean = {}
for i in range(len(data)):
    if i == 0:
        continue
    elif "TikTokApi.video(" in data[i]:
        continue
        # extract id from splited[i] ex. TikTokApi.video(id='7260080144771992838') i want 7260080144771992838
        match = re.search(r"id='(.+?)'", data[i]).group(1)

        # add to id_clean
        id_clean[i] = {"id": match}
        print(i, match)

    else:
        try:
            # id = id_clean[i-1].get("id")

            # remove " to prevent data error
            if '"' in data[i]:
                body = data[i].replace('"', '')

            # clean & decode UTF-8
            content = body.replace("'", '"')
            str_data = ast.literal_eval(content)
            decoded_data = str(decode_utf8(str_data)).replace(
                "'", '"').replace("True", "true").replace("False", "false")

            # turn string into object
            json_data = json.loads(decoded_data)
            id = json_data["id"]

            print(id, json_data)

            # export to check json data
            file_path = f"./json-decoded-auto/{id}.json"
            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
        except:
            print('error')
