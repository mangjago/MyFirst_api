from flask import Flask, jsonify
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

data = {
  "App_name": "",
  "Package_name": "",
  "Version": "",
  "Developer": "",
  "Size_app": "",
  "Url_download": ""
}

def search_app(app_name):
  base_url = f"https://apkpure.com/id/search?q={app_name}&t=app"
  headers = {"User-Agent": UserAgent().random}
  response = requests.get(base_url, headers=headers)
  #print(response.text)
  soup = bs(response.text, "html.parser")
  find_url = soup.find("a", attrs={"class": "first-info"})
  
  data_url = find_url.get("href")
  find_app_name = soup.find("p", class_="p1").text.replace("\n", "")
  find_dev_name = soup.find("p", class_="p2").text
  get_package_name = data_url.split("/")[5]
  
  data["App_name"] = find_app_name
  data["Package_name"] = get_package_name
  data["Developer"] = find_dev_name
 
  return data_url
  
def get_download_url(app_name):
  apps = search_app(app_name)
  headers = {"User-Agent": UserAgent().random}
  response = requests.get(apps, headers=headers)
  #print(response.text)
  soup = bs(response.text, "html.parser")
  try:
    find_url = soup.find("a", attrs={"class":"download_apk_news da"})
    data_size = find_url.get("data-dt-file_size")
    data_version = find_url.get("data-dt-version")
    data["Version"] = data_version
    data["Size_app"] = data_size
    return find_url.get("href")
  except AttributeError:
    find_other = soup.find("a", attrs={"class": "download_apk_news da no-right-radius"})
    data_size = find_other.get("data-dt-file_size")
    data_version = find_other.get("data-dt-version")
    data["Version"] = data_version
    data["Size_app"] = data_size
    #print(find_other)
    return find_other.get("href")

@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
    
@app.route('/api/v1/download/<app_name>', methods=['GET'])
def main_download_url(app_name):
  app_url = get_download_url(app_name)
  headers = {"User-Agent": UserAgent().random}
  response = requests.get(app_url, headers=headers)
  soup = bs(response.text, "html.parser")
  find_main_download = soup.find("a", class_="btn jump-downloading-btn")
  download_url = find_main_download.get("href")
  
  data["Url_download"] = download_url
  
  return jsonify(data)
  #return jsonify(main_download_url)
# @app.route('/main_download_url/<app_name>', methods=['GET'])
# def main_download_url_endpoint(app_name):
#     app_info = main_download_url(app_name)
#     return jsonify(app_info)

if __name__ == '__main__':
    app.run(debug=True, port=8001)
