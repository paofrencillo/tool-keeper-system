var year_course = document.getElementById("id_year_course");
year_course.setAttribute("pattern", "[a-zA-Z1-9-]+");

var email = document.getElementById("id_email");
email.setAttribute("pattern", "[a-zA-Z0-9._]+@gsfe.tupcavite.edu.ph");

$('#id_year_course').on('change', ()=> {
    let year_course = $('#id_year_course').val();
    let year_course_upper = year_course.toUpperCase();

    $('#id_year_course').val(year_course_upper);
});
