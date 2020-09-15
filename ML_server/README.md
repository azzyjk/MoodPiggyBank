# TEAM 감성저금통 - AI 분야
#### [이관석](https://github.com/LuterGS)
#### [정준원](https://github.com/azzyjk)

##### 인공지능 서버는 Flask로 제작하였습니다.

## RESTful API 설명

#### Request gamsung data  
<strong>POST</strong> /gamsung  
<strong>REQUEST BODY SCHEMA :</strong> application/json  
##### Response samples  
`
{   
    "text" : "감정하고자 하는 문장"  
}
`

#### Responses  
<strong>Respose SCHEMA :</strong> application/json  
<strong>result :</strong> string - 감성분석 정보 결과 (-1 혹은 1)




## 인공지능

### 전처리 데이터
1. [Naver Sentimental Movie Corpus](https://github.com/e9t/nsmc) 에 있는 ratings_train.txt, ratings_test.txt 를 사용함
2. 개별 문장에서 한국어를 제외한 특수기호 혹은 다른 언어의 글자를 제거
3. 이후 문장을 음절 단위로 (글자 하나하나씩) 쪼갬
4. tf.Tokenizer를 사용해 글자를 토크나이징


### 신경망 : Customized Resnet structure
Resnet 구조를 응용함.

![image](https://user-images.githubusercontent.com/19836058/93164292-22b7b600-f754-11ea-9f40-f5852ac23834.png)

1. 토크나이징된 데이터를 Embedding Layer를 이용해 벡터화
2. 과적합을 막기 위해 Dropout 적용
3. Resnet의 block 단위 3개를 서로 이어붙임
    1. Convolutional Layer로 데이터 매핑
    2. Batch_normalization, Activation을 거친 Layer와, 그렇지 않은 Layer를 합침
    3. Activation을 다시 거침
4. 2차원 데이터를 1차원으로 변환 (Flatten)
5. 정답 출력

정답률 : ratings_test.txt 기준으로 85.3%의 정답률을 보임

 
