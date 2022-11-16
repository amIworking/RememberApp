$("#words button[name=\"delete_0\"]").click(function(){
        $("#words p")[0].remove();
    })

    $("#add").click(function() {
        let lenght = $("#words p").length;
        $("#words").append("<div>\n" +
            "                <input class=\"m_input\" type=\"text\" placeholder=\"your word\" name=\"word_" + lenght +"\" value=\"\">\n" +
            "                <input class=\"m_input\" type=\"text\" placeholder =\"translation\"name=\"trans_" + lenght +"\" value=\"\">\n" +
            "                <button class='m_btn m_delete' type=\"button\" name=\"delete_" + lenght + "\"><span class='material-symbols-outlined'>remove</span></button>\n" +
            "            </div>" );
        $("#words button[ name=\"delete_" + lenght +"\"]").click(function(){
            $("#words div")[lenght].remove();
        })
    });

    $("#delete").click(function() {
        $("#words div:last-child").remove();
    });