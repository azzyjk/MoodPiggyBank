const express = require('express');
const axios = require('axios');

var app = express();
app.use(express.json());

const port = 8080;

function send_kakaotalk(res, outputs_data){
    res.send({
        version: "2.0",
        template: {
            outputs: outputs_data
        }
    });
}

function axios_diary(user_id, user_text, res) {
    axios.post('http://218.144.108.84/getDairy', {
        id: user_id,
        text: user_text
    }).then(function (response) {
        var data = response.data;
        var emotion = data.emotion;
        var img = data.imgUrl;
        var outputs = [];

        if(img == -1){
            if(emotion == 1){
                outputs = [
                    {
                        simpleText: {
                            text: "긍정"
                        }
                    }
                ];
            }
            else if(emotion == -1){
                url = data.sendUrl;
                if(url == -1){
                    outputs = [
                        {
                            simpleText: {
                                text: "부정, 계좌X"
                            }
                        }
                    ];
                }
                else{
                    outputs = [
                        {
                          "basicCard": {
                            "title": "부정",
                            "description": "계좌O",
                            "buttons": [
                              {
                                "action": "webLink",
                                "label": "송금 링크",
                                "webLinkUrl": url
                              }
                            ]
                          }
                        }
                    ];
                }
            }else{
                if(emotion == 1){
                    outputs = [
                        {
                          "basicCard": {
                            "title": "주간 분석 그래프가 도착했어요",
                            "description": "긍정",
                            "thumbnail": {
                                "imageUrl": img
                              },
                              "profile": {
                                "imageUrl": img,
                                "nickname": "주간 분석 그래프"
                              }
                          }
                        }
                    ];
                }
                else if(emotion == -1){
                    url = data.sendUrl;
                    if(url == -1){
                        outputs = [
                            {
                                "basicCard": {
                                "title": "주간 분석 그래프가 도착했어요",
                                "description": "부정, 계좌X",
                                "thumbnail": {
                                    "imageUrl": img
                                    },
                                    "profile": {
                                    "imageUrl": img,
                                    "nickname": "주간 분석 그래프"
                                    }
                                }
                            }
                        ];
                    }
                    else{
                        outputs = [
                            {
                                "basicCard": {
                                "title": "주간 분석 그래프가 도착했어요",
                                "description": "부정, 계좌O",
                                "thumbnail": {
                                    "imageUrl": img
                                    },
                                    "profile": {
                                    "imageUrl": img,
                                    "nickname": "주간 분석 그래프"
                                    },
                                    "buttons": [
                                        {
                                        "action": "webLink",
                                        "label": "송금 링크",
                                        "webLinkUrl": url
                                        }
                                    ]
                                }
                            }
                        ];
                    }
                }
            }
        }
        
        send_kakaotalk(res, outputs);
    }).catch(function (error) {
        console.log(error);
    })
}

function axios_bank(user_id, user_bank, user_account, user_amount, res) {
    axios.post('http://218.144.108.84/bankAddress', {
        id: user_id,
        bank: user_bank,
        account: user_account,
        amount: user_amount
    }).then(function (response) {
        res.send({
            version: "2.0",
            template: {
                outputs: [
                    {
                        simpleText: {
                            text: "계좌 등록이 완료되었습니다. 목표 금액도 한번 설정해 보세요. (목표 금액 설정 또는 목표 금액 00원 등의 명령으로 설정 가능합니다.)"
                        }
                    }
                ]
            }
        });
    }).catch(function (error) {
        console.log(error);
    })
}

function axios_goal(user_id, user_goal_amount, user_goal_reason, res) {
    axios.post('http://218.144.108.84/goal', {
        id: user_id,
        goal_amount: user_goal_amount,
        goal_reason: user_goal_reason
    }).then(function (response) {
        res.send({
            version: "2.0",
            template: {
                outputs: [
                    {
                        simpleText: {
                            text: user_goal_reason + "을(를) 하기 위한 목표금액이 설정되었습니다."
                        }
                    }
                ]
            }
        });
    }).catch(function (error) {
        console.log(error);
    })
}

app.post("/diary", function (req, res) {
    var id = req.body.userRequest.user.id;
    var text = req.body.action.params.text;
    axios_diary(id, text, res);
})

app.post("/bankAddress", function (req, res) {
    var id = req.body.userRequest.user.id;
    var bank = req.body.action.params.bank;
    var account = req.body.action.params.account;
    var amount = req.body.action.params.amount;
    axios_bank(id, bank, account, amount, res);
})

app.post("/goal", function (req, res) {
    var id = req.body.userRequest.user.id;
    var goal_amount = req.body.action.params.goal_amount;
    var goal_reason = req.body.action.params.goal_reason;
    axios_goal(id, goal_amount, goal_reason, res);
})


app.listen(port, function () {
    console.log("server start");
});


app.get('/', (req, res) => {
    res.send('감성일기 카카오톡 챗봇 API 서버');
})
