import re
import json

file=open('sample_stored_procedure.sql')
sql_file=file.read()

queries=sql_file.split(';')

out_json={}
q_length=len(queries)

queries.pop(67)
#Dropped last query since it was blank query
q_length=len(queries)

info=[]

for i in range(q_length):
    present_information={}
    source_information=[]
    sub_info={}
    main=re.findall(r"INSERT INTO.+|CREATE.+|DELETE.+|UPDATE.+|USE.+|SELECT COUNT.+",queries[i])[0].split(' ')
    present_information["statement_id"]=i+1
    if 'OR' in main:
        present_information["statement_type"]=' '.join(main[0:3])
    elif 'USE' in main:
        present_information["statement_type"]=' '.join(main[0:2])
    else:
        present_information["statement_type"]=main[0]
    if(main[-2]=="AS"):
        present_information["target_table"]=main[-3]
    elif 'USE' in main:
        present_information["target_table"]=' '.join(main[1:])
    else:
        present_information["target_table"]=main[-1]
    sub=re.findall(r"JOIN.+|FROM.+",queries[i])
    for j in range(len(sub)):
        sub_table=sub[j].split(' ')
        sub_info['type']="JOIN or FROM"
        sub_info['source_table']=sub_table[1]
        source_information.append(sub_info)
    present_information["source"]=source_information
    info.append(present_information)

json_file=open('sample_stored_procedure.json', 'w')

json_file.write(json.dumps(info,indent='\t'))

json_file.close()

print("\nExtracted information from SQL query is stored in sample_stored_procedure.json.")
