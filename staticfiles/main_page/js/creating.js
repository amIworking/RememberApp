$("#words button[name=\"delete_0\"]").click(function(){
        $("#words p")[0].remove();
    })
    console.log('chenged');

    $("#add").click(function() {
        let lenght = $("#words p").length;
        $("#words").append("<p>\n" +
            "                <input class=\"m_input\" type=\"text\" placeholder=\"your word\" name=\"word_" + lenght +"\" value=\"\">\n" +
            "                <input class=\"m_input\" type=\"text\" placeholder =\"translation\"name=\"trans_" + lenght +"\" value=\"\">\n" +
            "                <button class='m_delete material-symbols-outlined' type=\"button\" name=\"delete_" + lenght + "\"></button>\n" +
            "            </p>" );
        $("#words button[ name=\"delete_" + lenght +"\"]").click(function(){
            $("#words p")[lenght].remove();
        })
    });

    $("#delete").click(function() {
        $("#words p:last-child").remove();
    });