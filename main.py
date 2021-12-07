# !pip install pandas
# !pip install fuzzywuzzy
# !pip install python-Levenshtein 

from fuzzywuzzy import process,fuzz
import pandas as pd

def create_list(file_path):
    new_file = open(file_path, "r")
    contents = new_file.read()
    new_list = contents.split("\n")
    new_file.close()
    return list(set(new_list))

live_list = create_list("live_urls.txt")
staging_list = create_list("staging_urls.txt")

# fixed_changes = {'/our-studios/':'/contact-us/'}

# for k,v in fixed_changes.items():
#     fix_list = [w.replace(k,v) for w in live_list]

output = []

for url in live_list:
    choice = process.extract(url, staging_list, limit=3)
    [url_1, score_1] = choice[0]
    [url_2,score_2] = choice[1]
    [url_3,score_3] = choice[2]
    data = [url,url_1, score_1, url_2, score_2,url_3,score_3]
    output.append(data)

df = pd.DataFrame(output, columns =['Original_URL',"Redirect_1","Score_1", "Redirect_2","Score_2","Redirect_3","Score_3"]) 
df.sort_values(by='Score_1', ascending=False, inplace=True)

print(df.head(20))

df.to_csv('output.csv', index=False)


