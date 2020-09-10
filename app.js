var express = require('express');
var app = express();
var mysql = require('./db/mysql.js');
var session = require('express-session');
var fs = require('fs');
var bodyParser = require('body-parser');
var path = require('path');
var http = require('http').createServer(app);
var axios = require('axios');
var {
    PythonShell
} = require('python-shell');
var pythonOptions = {
    mode: 'text',
    scriptPath: './',
    args: ['value1', 'value2', 'value3']
};
require('dotenv').config();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(express.static(path.join(__dirname, '/public')));
app.use(express.static(path.join(__dirname, '/graph')));
mysql.connect();

app.post('/goal', function(req, res) {

    var id = req.body.id;
    var goal_amount = '';
    var goal_reason = req.body.goal_reason;
    var sendResult;

    for (var i in req.body.goal_amount) {
        if (i > 10) {
            if (req.body.goal_amount[i] == ',') break;
            else goal_amount = goal_amount + req.body.goal_amount[i];
        }
    }


    mysql.query('select * from member_info where id = ?', id, function(err, result) {
        if (err) console.log(err);
        else {
            //new member
            if (result[0] == undefined) {
                mysql.query('insert into member_info (id,goal_amount,goal_reason) values (?,?,?)', [id, goal_amount, goal_reason], function(err, result) {
                    if (err) console.log(err);
                });
                mysql.query('insert into feeling (id) values (?)', id, function(err, result) {
                    if (err) console.log(err);
                });
            }
            //exist member
            else {
                mysql.query('update member_info set goal_amount = ?, goal_reason = ? where id = ?', [goal_amount, goal_reason, id], function(err, result) {
                    if (err) console.log(err);
                    else {
                        sendResult = {
                            aa: 1,
                            bb: 2
                        }

                        console.log(sendResult);
                    }
                })
            }
        }
    });

    res.send('ok');
});
//get bank address
app.post('/bankAddress', function(req, res) {

    var id = req.body.id;
    var bank = req.body.bank;
    var account = req.body.account;
    var amount = req.body.amount;
    var bank_encoded;
    var send;

    if (bank == '카카오뱅크') bank_encoded = process.env.kakao;
    else if (bank == 'NH농협') bank_encoded = process.env.nh;
    else if (bank == 'KB국민') bank_encoded = process.env.kb;
    else if (bank == '신한') bank_encoded = process.env.sinhan;
    else if (bank == '우리') bank_encoded = process.env.woori;
    else if (bank == '하나') bank_encoded = process.env.hana;
    else if (bank == 'IBK기업') bank_encoded = process.env.ibk;
    else if (bank == 'SC제일') bank_encoded = process.env.sc;
    else if (bank == '씨티') bank_encoded = process.env.city;
    else if (bank == '케이뱅크') bank_encoded = process.env.kbank;
    else {
        bank_encoded = bank;
    }
    mysql.query('select * from member_info where id = ?', id, function(err, result) {
        if (err) console.log(err);
        else {

            send = 'supertoss://send?amount=' + amount + '&bank=' + bank_encoded + '&accountNo=' + account + '&origin=qr';
            //new member
            if (result[0] == undefined) {
                mysql.query('insert into member_info (id,bank,account,amount,bank_active,send) values (?,?,?,?,1,?)', [id, bank_encoded, account, amount, send], function(err, result) {
                    if (err) console.log(err);
                });

                mysql.query('insert into feeling (id) values (?)', id, function(err, result) {
                    if (err) console.log(err);
                });
            }
            //exist member
            else {

                send = 'supertoss://send?amount=' + amount + '&bank=' + bank_encoded + '&accountNo=' + account + '&origin=qr';
                mysql.query('update member_info set bank = ?, account = ?, amount = ?, bank_active = 1, send = ?  where id = ?', [bank_encoded, account, amount, send, id], function(err, result) {
                    if (err) console.log(err);
                })
            }
        }

    })

    res.send('ok');
});
//get dairy 
app.post('/getDairy', function(req, res) {

    var id = req.body.id;
    var text = req.body.text;
    var feeling;
    var option;
    var date = new Date();
    var kakaoData;
    option = {
        url: 'http://193.122.122.61/gamsung',
        method: 'POST',
        data: {
            'text': text
        }
    }

    mysql.query('select * from member_info where id = ?', id, function(err, result) {
        if (err) console.log(err);
        else {

            //new member
            if (result[0] == undefined) {
                mysql.query('insert into member_info (id) values (?)', id, function(err, result) {
                    if (err) console.log(err);
                    else {

                        mysql.query('insert into feeling (id,last_dairy) values (?,?)', [id, text], function(err, result) {
                            if (err) console.log(err);
                            else {

                                axios(option).then(
                                    (response) => {
                                        //console.log(response.data);

                                        kakaoData = {
                                            emotion: response.data.result,
                                            sendUrl: '-1',
                                            imgUrl: '-1'
                                        
                                        }
                                        var sql;
                                        var tmp;
                                        var day = date.getDay();
                                        day = '7';
                                        if (day == '1') {
                                            sql = 'update feeling set mon = ? where id =?'
                                        } else if (day == '2') {
                                            sql = 'update feeling set tue = ? where id =?'
                                        } else if (day == '3') {
                                            sql = 'update feeling set wed = ? where id =?'

                                        } else if (day == '4') {
                                            sql = 'update feeling set thr = ? where id =?'
                                        } else if (day == '5') {
                                            sql = 'update feeling set fri = ? where id =?'
                                        } else if (day == '6') {
                                            sql = 'update feeling set sat = ? where id =?'
                                        } else if (day == '7') {
                                            sql = 'update feeling set sun = ?  where id =?'
                                        } else {}

                                        mysql.query(sql, [Number(kakaoData.emotion), id], function(err, result) {
                                            if (err) console.log(err);
                                        });
                                        res.send(kakaoData);
                                    }
                                )
                            }
                        });
                    }
                });

            }
            //exist member
            else {

                mysql.query('update feeling set last_dairy =  ? where id = ?', [text, id], function(err, result) {
                    if (err) console.log(err);
                    else {
                        mysql.query('select * from member_info where id = ?', id, function(err, result) {
                            if (err) console.log(err);
                            else {



                                axios(option).then(
                                    (response) => {
                                        //console.log(response.data);

                                        kakaoData = {
                                            emotion: response.data.result,
                                            sendUrl: result[0].send,
                                            imgUrl: '-1'
                                            
                                        }
                                        mysql.query('select * from feeling where id = ?', id,
                                            function(err, result) {
                                                if (err) console.log(err);
                                                else {
                                                    var sql;
                                                    var tmp;
                                                    //var day = date.getDay();
                                                    var day = '7';
                                                    if (day == '1') {
                                                        tmp = result[0].mon;
                                                        sql = 'update feeling set mon = ?, print = 0 where id =?'
                                                    } else if (day == '2') {
                                                        tmp = result[0].tue;
                                                        sql = 'update feeling set tue = ? , print = 0where id =?'
                                                    } else if (day == '3') {
                                                        tmp = result[0].wed;
                                                        sql = 'update feeling set wed = ? , print = 0where id =?'

                                                    } else if (day == '4') {
                                                        tmp = result[0].thr;
                                                        sql = 'update feeling set thr = ? , print = 0where id =?'
                                                    } else if (day == '5') {
                                                        tmp = result[0].fri;
                                                        sql = 'update feeling set fri = ? , print = 0where id =?'
                                                    } else if (day == '6') {
                                                        tmp = result[0].sat;
                                                        sql = 'update feeling set sat = ? , print = 0where id =?'
                                                    } else if (day == '7') {
                                                        tmp = result[0].sun;
                                                        sql = 'update feeling set sun = ? where id =?'

                                                    } else {}

                                                    if (day == '7') {
                                                        mysql.query('select * from feeling where id = ?'
                                                        ,id
                                                        ,function(err,result){
                                                        
                                                                if(result[0].print == '0'){
                                                                mysql.query('update feeling set print = 1 where id = ?', id, function(err, result) {
                                                                if (err) console.log(err);
                                                                else {
                                                                    PythonShell.run('graph.py', pythonOptions, function(err, pythonResult) {
                                                                        if (err) console.log(err);
                                                                        else {
                                                                            mysql.query(sql, [ Number(kakaoData.emotion), id], function(err, result) {
                                                                                if (err) console.log(err);
                                                                                else {
                                                                                    kakaoData = {

                                                                                        emotion: kakaoData.emotion,
                                                                                        sendUrl: kakaoData.sendUrl,

                                                                                        imgUrl: 'http://218.144.108.84/' + pythonResult[0]
                                                                                    }
                                                                                    console.log(kakaoData.imgUrl);

                                                                                    res.send(kakaoData);
                                                                                    }

                                                                                })

                                                                            }
                                                                        })
                                                                    }
                                                                })
                                                            }
                                                            else{
                                                                mysql.query(sql, [Number(tmp) + Number(kakaoData.emotion), id], function(err, result) {
                                                                                if (err) console.log(err);
                                                                                else {
                                                                                    res.send(kakaoData);
                                                                                    }

                                                                      })
                                                            }
                                                        })
                                                        
                                                    } else {
                                                        mysql.query(sql, [Number(tmp) + Number(kakaoData.emotion), id], function(err, result) {
                                                            if (err) console.log(err);
                                                            else {
                                                                res.send(kakaoData);
                                                            }

                                                        })
                                                    }
                                                   
                                                }
                                            });
                                      
                                    }
                                )

                            }
                        })
                    }
                })


            }
        }

    })

});
///open server
app.get('/', function(req, res) {
    res.writeHead(200, {
        'Content-Type': 'text/html'
    });
    res.end(data);
});
app.listen(80, function() {
    console.log('NLP server on');
});
