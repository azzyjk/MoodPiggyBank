# Team 감정저금통 - AI 분야

##### 인공지능 서버는 Flask로 제작하였습니다.

## RESTful API 설명

#### Request gamsung data  
<strong>POST</strong> http://193.122.122.61/gamsung  
<strong>REQUEST BODY SCHEMA :</strong> application/json  
##### Response samples  
`
{   
    "text" : "감정하고자 하는 문장"  
}
`

#### Responses  
<strong>Respose SCHEMA :</strong> application/json  
<strong>result :</strong> string - 감정분석 정보 결과 (-1 혹은 1)




## 인공지능

### 전처리 데이터
1. [Naver Sentimental Movie Corpus](https://github.com/e9t/nsmc) 에 있는 ratings_train.txt, ratings_test.txt 를 사용함
2. 개별 문장에서 한국어를 제외한 특수기호 혹은 다른 언어의 글자를 제거
3. 이후 문장을 음절 단위로 (글자 하나하나씩) 쪼갬
4. tf.Tokenizer를 사용해 글자를 토크나이징

### 출력 결과
* 하단의 신경망 2개는 각각 0과 1 사이의 실수값을 출력하며, 0.5 미만이면 부정, 이상이면 긍정을 의미한다.
* 이 신경망 두 개의 평균값이 인공지능의 출력이다.

### 신경망1: ELMo 구조와 Resnet 구조 응용
![model](https://user-images.githubusercontent.com/19836058/93204660-6c72c180-f791-11ea-914f-8e07fbe4d9aa.png)

1. 들어온 문장을 Embedding Layer 를 통해 벡터화 시킨 후 Convolution Layer 로 특징을 잡아줍니다.
2. 이후 batch normalization Layer 를 통해 값을 regularization 시켜줍니다.
3. skip connection 을 이용해 Bi-LSTM Layer 를 통해 문장의 앞뒤 문맥을 학습합니다.
4. 이후 해당 layer 를 거친 데이터와 거치지 않은 데이터를 합치고 LSTM Layer 를 한번 더 거칩니다.
5. Max pooling 을 통해 다시 한번 해당 데이터들의 특징을 추출한 뒤 Full connection layer 를 통해 학습해줍니다.

<strong>정답률 : ratings_test.txt 기준으로 86% 의 정답률을 보임</strong>


### 신경망2 : CNN 방식과 Resnet 구조 응용
![test](https://user-images.githubusercontent.com/19836058/93205039-19e5d500-f792-11ea-9364-3af1fc5659cb.png)

1. 토크나이징된 데이터를 Embedding Layer를 이용해 벡터화해 줍니다.
2. 과적합을 막기 위해 Dropout 적용합니다.
3. Resnet의 block 단위 3개를 서로 이어붙입니다.
    1. Convolutional Layer로 데이터를 매핑합니다.
    2. Batch_normalization, Activation을 거친 Layer와, 그렇지 않은 Layer를 서로 합칩니다.
    3. Activation을 다시 거칩니다.
4. 2차원 데이터를 1차원으로 변환 (Flatten) 합니다.
5. 정답을 출력합니다.

<strong>정답률 : ratings_test.txt 기준으로 85.3%의 정답률을 보임</strong>

 
