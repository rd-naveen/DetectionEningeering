import pandas as pd
import re

file_ =  r"E:\GitRepos\DetectionEningeering\FluentdConfigGenerator\Fluentd_Configuration.xlsx"
linux_user_name = "core_user"
linux_bash_script_name = "make_temp_file.sh"

pd_sources = pd.read_excel(file_, usecols=['type', 'path', 'pos_file', 'path_key', 'parser', 'tag',
       'emit_unmatched_lines', 'comment'], sheet_name="Sources")

pd_matches = pd.read_excel(file_, usecols=['match_pattern', 'type', 'host', 'port', 'user', 'password',
       'logstash_format', 'logstash_prefix',"comments"], sheet_name="Matches")

pd_filters = pd.read_excel(file_, usecols=['tag', 'type', 'old_field', 'new_field', 'custom_value', 'remove_old'],  sheet_name="Filters")


def check_match(tag):
    for matcher in set(pd_matches["match_pattern"].values.tolist()):
        if re.match(matcher, tag):
            return True
    return False

print("## Validation")
for tag_ in pd_sources["tag"].values.tolist():
    if not check_match(tag_):
       print(f" {tag_} not matching with any of the matchers: {set(pd_matches["match_pattern"].values.tolist())}")

print("## Stats")
print (f"No of log source configurations to create {len(set(pd_sources["path"].values.tolist()))}")
print (f"No of temp files to create {len(set(pd_sources["pos_file"].values.tolist()))}")
print (f"No of parsers to use {len(set(pd_sources["parser"].values.tolist()))}: {set(pd_sources["parser"].values.tolist())} ")

print(f"No of Matches: {set(pd_matches["match_pattern"].values.tolist())} ")

# create bash script to create temporary files
all_bash_script = "#/bin/bash\n\n"
for temp_file in pd_sources["pos_file"].values.tolist():
    temp_bash_string = f"sudo touch {temp_file}\n" +\
        f"sudo chown {linux_user_name} {temp_file}\n" +\
        f"sudo chmod o+w {temp_file}\n\n"
    all_bash_script += temp_bash_string
# print(all_bash_script)
with open(linux_bash_script_name,"w") as file: 
    file.write(all_bash_script) 



# create source input configurations
all_source = ""
for source_config in pd_sources.to_dict(orient='records'):
    source_config_string = f"# {source_config["comment"]}\n" +\
    f"<source>\n" + \
    f"     @type {source_config['type']}\n" + \
    f"     path {source_config['path']}\n" + \
    f"     pos_file {source_config['pos_file']}\n" + \
    f"     <parse>\n" + \
    f"        @type {source_config["parser"]}\n" + \
    f"     </parse>\n" + \
    f"     path_key {source_config['path_key']}\n" + \
    f"     tag {source_config['tag']}\n" + \
    f"     emit_unmatched_lines {str(source_config['emit_unmatched_lines']).lower()}\n" + \
    "</source>\n\n" 
    # print(source_config_string)
    all_source += source_config_string
with open ("fluentd.conf","w") as file: 
    file.write(all_source)
    file.write("\n\n\n")

# create filter configurations
all_fliter = ""
for tag_ in set(pd_filters["tag"].values.tolist()):
    remove_keys = set(pd_filters.loc[(pd_filters["tag"]==tag_) & (pd_filters["remove_old"] == True)]["old_field"].values.tolist())
    if len(remove_keys) == 0:
        remove_keys_str ="" 
    elif len(remove_keys) == 1:
        remove_keys_str = f"remove_key {",".join(remove_keys)}"
    elif len(remove_keys)>1:
        remove_keys_str = f"remove_keys {",".join(remove_keys)}"

    record_string = f"      <record>\n"
    for trans in pd_filters.loc[pd_filters["tag"] == tag_].to_dict(orient='records'):
        s_s = "{"
        s_e = "}"
        if str(trans["old_field"]) == "nan":
            record_string += f"         \"{trans['new_field']}\" {trans["custom_value"]}\n"
        else: 
            record_string += f"         \"{trans['new_field']}\" ${s_s}record[\"{trans["old_field"]}\"]{s_e}\n"

    record_string += f"     </record>\n"
    filter_string = f"#{tag_} filter\n" +\
    f"<filter {tag_}>\n"+\
    f"      @type {pd_filters.loc[pd_filters["tag"] == tag_]["type"].values.tolist()[0]}\n" +\
    f"{record_string}"
    if remove_keys_str:
        filter_string += f"       {remove_keys_str}\n"
    filter_string += f"</filter>"
    # print(filter_string)
    all_fliter += filter_string

with open("fluentd.conf","a") as file:
    file.write(all_fliter)
    file.write("\n\n\n")

# create output configurations
all_matcher = ""
for matcher in pd_matches.to_dict(orient='records'):
    matcher_string = f"# {matcher["comments"]}\n" +\
f"<match {matcher["match_pattern"]}>\n" +\
f"     @type {matcher["type"]}\n" +\
f"         host {matcher["host"]}\n" +\
f"         port {matcher["port"]}\n" +\
f"         user {matcher["user"]}\n"+\
f"         password {matcher["password"]}$\n"+\
f"         logstash_format {str(matcher["logstash_format"]).lower()}\n"+\
f"         logstash_prefix {matcher["logstash_prefix"]}\n"+\
f"</match>\n\n"
    # print(matcher_string)
    all_matcher += matcher_string 
with open("fluentd.conf","a") as file:
    file.write(all_matcher)
    file.write("\n\n\n")