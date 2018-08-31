import requests
import pandas as pd

df = pd.read_excel("C:\\Users\\User\Downloads\세지포_이벤트.xlsx")
# print(df.shape)
# print(df.columns)

dedu_df = df.drop_duplicates(['연락처'], keep='first')
dedu_df.columns = ['contact', 'link']

# print(dedu_df.shape)
# print(dedu_df.columns)

def download_image(file_name, url):
    #filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)

if __name__ == '__main__':
    cnt = 1
    for file_name, url in zip(dedu_df['contact'], dedu_df['link']):
        cnt += 1
        file_name = str(cnt) + "_" + file_name
        download_image(file_name, url)
