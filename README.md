# Iscom B&B Project

## 采葳景點推薦所需的爬蟲:  
Get all tripadvisor data:

`scrapy crawl tripadvisor -t json -o filename.json`

## INSTALL

1. Install Docker:
    * use this [script](https://get.docker.com/) to install docker
2. Pull & RUN Container:
    * Download MongoDb container which has Tourist attraction recommendation model
        1. `docker pull davidtnfsh/iscommongo`
        2. `docker run -itd --name ASYOUWISH_DB davidtnfsh/iscommongo`
        3. `docker exec -it ASYOUWISH_DB bash`
        4. `mongorestore -d nlp --drop /dump/nlp/kcm.bson`
        5. `ifconfig`
            * Look up IP in  eth0 -> inet addr
            * Remember this IP, we'll need this later.
    * Install api server, written in Django(python web framework):
      1. `docker pull davidtnfsh/iscom`
      2. `docker run -itd --name ASYOUWISH -ip PORT:8000 davidtnfsh/iscom`
      3. `docker exec -it ASYOUWISH bash`
      4. `cd /ISAPI`
      5. `vim /ISAPI/settings.py` ASSIGNE container ip to VARIABLE IP at the second-last line of settings.py 
      6. `nohup python3 manage.py runserver 0.0.0.0:8000 &`

## API Usage and Results

API使用方式（下面所寫的是api的URL pattern）  
(Usage of API (pattern written below is URL pattern))：

#### parameter

* `query`：The tourist attraction user will have been through in his/her trip.
* `number`：Amount of tourist attractions api returns.
* `type`：Keywords matching or related to one of seven tourism category which is defined by ISCOM.
* `city`：The city user would like to go to.

#### url pattern

1. *`http://ip:8000/api?query=<>&number=<>`*  
return tourist attractions system would recommend user to go to.  
* 範例 (Example)：`api/?query=逢甲夜市&number=10`

  ```
  [
    [
      "宮原眼科",
      [
        "小吃/特產類",
        "古蹟類"
      ]
    ],
    [
      "中友百貨",
      [
        "其他"
      ]
    ],
    [
      "台中公園",
      [
        "生態類",
        "體育健身類",
        "遊憩類"
      ]
    ],
    [
      "中正公園",
      [
        "國家公園類",
        "文化類",
        "廟宇類",
        "遊憩類",
        "都會公園類"
      ]
    ...
    ...
    ...
  ]
  ```

2. *`http://ip:8000/api/findroot?type=<>&city=<>`*  
Use this api to find Root of each tourism category.  
* 範例 (Example)：`api/findroot?type=美食&city=台中`

  ```
  [
    [
      "逢甲夜市",
      35
    ],
    [
      "高美濕地",
      31
    ],
    [
      "新社花海",
      21
    ],
    [
      "東海大學",
      9
    ],
    [
      "武陵農場",
      9
    ],
    [
      "谷關溫泉",
      8
    ],
    [
      "麗寶樂園",
      8
    ],
    [
      "新社莊園",
      7
    ]
  ]
  ```