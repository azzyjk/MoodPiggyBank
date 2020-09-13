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
        var goal = data.goal;
        var outputs = [];
        var text_good = "기분 좋은 일이 있으셨군요! ";
        var text_bad = "앞으로는 좋은 일이 찾아오기를 기원합니다.";
        var text_bank = "작은 금액씩 저축을 하다보면, 큰 돈이 모이는 기쁨이 찾아올거에요!";
        var text_nobank = "저금할 계좌를 등록해 주시면, 안 좋은 일이 있으실 떄마다 소액을 저금할 수 있는 서비스를 이용하실 수 있습니다.";
        var text_goal = "";
        var send_img_form = {};
        var send_report_form = {};

        if (emotion == -1) {
            var bad_img_url = "https://diary-chatbot.us-south.cf.appdomain.cloud/img/" + String(user_text.length % 18) + ".jpg";
            send_img_form = {
                "simpleImage": {
                    "imageUrl": bad_img_url,
                    "altText": "힘들때 힘이 되는 이미지"
                }
            };
        }

        if (emotion == 1) {
            outputs = [
                {
                    simpleText: {
                        text: text_good + text_goal
                    }
                }
            ];
        }
        else if (emotion == -1) {
            url = data.sendUrl;
            if (url == -1) {
                outputs = [
                    send_img_form,
                    {
                        simpleText: {
                            text: text_bad + text_nobank + text_goal
                        }
                    }
                ];
            }
            else {
                outputs = [
                    send_img_form,
                    {
                        "basicCard": {
                            "title": text_bad + text_goal,
                            "description": text_bank,
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

        if (img != -1) {
            send_report_form =
            {
                "basicCard":
                {
                    "title": "주간 분석 그래프가 도착했어요.",
                    "description": "일주일간의 감정 변화를 표시한 그래프입니다.",
                    "thumbnail": {
                        "imageUrl": img
                    }
                }
            };
            outputs.push(send_report_form);
        }

        if (goal != -1) {
            var goal_amount = goal.amount;
            var goal_reason = goal.reason;
            text_goal = goal_reason + "을(를) 하기 위한 목표금액 " + goal_amount + "원 달성을 축하드립니다. 목표 금액 초기화를 진행하면, 현재 모은 금액과 목표 금액이 모두 초기화되며, 다시 목표 금액 설정을 통해 새로운 목표를 설정하실 수 있습니다.";
            send_goal_form = {
                simpleText: {
                    text: text_goal
                }
            }
            outputs.push(send_goal_form);
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

app.post("/goal_acheive", function (req, res) {
    var user_id = req.body.userRequest.user.id;
    axios.post('http://218.144.108.84/goal_acheive', {
        id: user_id
    })
    res.send({
        version: "2.0",
        template: {
            outputs: [
                {
                    simpleText: {
                        text: "목표 금액 초기화"
                    }
                }
            ]
        }
    });
})


app.listen(port, function () {
    console.log("server start");
});


app.get('/', (req, res) => {
    res.send('감성일기 카카오톡 챗봇 API 서버');
})

app.use(express.static('public'));