
    function Init(){
            document.location.reload();
    }
    
    
    function fetchPage(name,openPage){
        fetch(name).then(function(response){
            response.text().then(function(text){
                var data = JSON.parse(text);
                var article = "";
                var menu = "";
                var paction = "";

                console.log(name);
                console.log(openPage);
                $('.firstComment').html(data.login[0]);
                
                if(openPage == "login"){
                    $('.sub_title').html(data.login[0]);
                    $('.first_comment').html(data.login[1]);
                    $('.second_comment').html(data.login[2]);
                    $('.submit').html(data.login[3]);

                    menu += '\n<div class ="sign_up"><a href = "#!sign_up" onclick = "fetchPage("list.json","sign_up")">';
                    menu += data.login[4];
                    menu += '</div></a></div>';
                    menu += '\n<div class ="email_auth"><a href = "#!email_auth" onclick = "fetchPage("list.json","email_auth")">';
                    menu += data.login[5];
                    menu += '</div></a></div>';

                    login_box.action = "/sign_in";



                }

                else if(openPage == "sign_up"){
                     
                    $('.sub_title').html(data.sign_up[0]);
                    $('.first_comment').html(data.sign_up[1]);
                    $('.second_comment').html(data.sign_up[2]);
                    $('.submit').html(data.sign_up[5]);
                   
                    menu += '\n<div class ="email_auth"><a href = "#!email_auth" onclick = "fetchPage("list.json","email_auth")">';
                    menu += data.sign_up[6];
                    menu += '</div></a></div>';
                    
                    article += '\n<li><label>';
                    article += data.sign_up[3];
                    article += '</label></li><li><input type="text" class="text" name="third_post"></li>';
                    article += '\n<li><label>';
                    article += data.sign_up[4];
                    article += '</label></li><li><input type="text" class="text" name="forth_post"></li>';

                    paction += '<form name="login_box" action="/sign_up" method="POST">';

                    login_box.action = "/join";
                }
    
                else if(openPage == "email_auth"){
                                
                    $('.sub_title').html(data.email_auth[0]);
                    $('.first_comment').html(data.email_auth[1]);
                    $('.second_comment').html(data.email_auth[2]);
                    $('.submit').html(data.email_auth[3]);

                    menu += '\n<div class ="sign_up"><a href = "#!sign_up" onclick = "fetchPage("list.json","sign_up")">';
                    menu += data.email_auth[4];
                    menu += '</div></a></div>';

                    paction += '<form name="login_box" action="/email_auth" method="POST">';

                    login_box.action = "/email_auth";
                }

                else{
                
                }
                document.querySelector('article').innerHTML = article;
                document.querySelector('menu').innerHTML = menu;
            })
        });
    }

    
    if(location.hash){
        fetchPage('./js/list.json',location.hash.substr(2));
    }
    else{
        fetchPage('./js/list.json','login');
    }
    
