import json
from pathlib import Path

def concat_jsons(result_json, next_json):
    for query_result_1, query_result_2 in zip(result_json, next_json):
        query_1 = query_result_1["query"]
        query_2 = query_result_2["query"]
        assert query_1 == query_2
        query_result_1["results"].extend(query_result_2["results"])

all_intermediate_jsons_filepaths = snakemake.input.all_intermediate_jsons
result_json_filepath = snakemake.output.result_json

with open(all_intermediate_jsons_filepaths[0]) as file_handler:
    result_json = json.load(file_handler)

for intermediate_json_filepath in all_intermediate_jsons_filepaths[1:]:
    with open(intermediate_json_filepath) as file_handler:
        next_json = json.load(file_handler)
    concat_jsons(result_json, next_json)

result_json_path = Path(result_json_filepath)
result_json_path.write_text(json.dumps(result_json, indent=4))