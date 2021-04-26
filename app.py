from flask import Flask, render_template, request
from course_listings import parse_html, generate_url, download_page, concentration_course_list, course_type_list, sort_by_course_level_num, course_level_list
app = Flask(__name__)
global babson_url
babson_url = 'https://fusionmx.babson.edu/CourseListing/?blnShowHeader=true'



@app.route("/")
def home_page():
    return render_template('homepage.html')


@app.route("/concentrationcoursefinder", methods=["GET", "POST"])
def conc_course_list():
    if request.method == "POST":
        try:
            program = str(request.form['program'])
            term = str(request.form['term'])
            year = int(request.form['year'])
            concentration = str(request.form['concentration'])
            url = generate_url(program, term, year)
            course_list = parse_html(download_page(url).read())
            concentration_courses = concentration_course_list(concentration, course_list)
            if concentration_courses:
                return render_template('conc_result.html', 
                                        program=program,
                                        term=term,
                                        year=year,
                                        concentration=concentration,
                                        concentration_courses=concentration_courses)
            else:
                return render_template('conc_course_finder.html', error=True)
        except:
            return render_template('error.html', babson_url=babson_url)
    return render_template('conc_course_finder.html', error=None)


@app.route("/coursetypefinder", methods=["GET", "POST"])
def ct_course_list():
    if request.method == "POST":
        try:
            program = str(request.form['program'])
            term = str(request.form['term'])
            year = int(request.form['year'])
            course_type = str(request.form['course_type'])
            url = generate_url(program, term, year)
            course_list = parse_html(download_page(url).read())
            available_courses = course_type_list(course_type, course_list)
            if available_courses:
                return render_template('coursetype_result.html', 
                                        program=program,
                                        term=term,
                                        year=year,
                                        course_type=course_type,
                                        available_courses=available_courses)
            else:
                return render_template('ct_course_finder.html', error=True)
        except:
            return render_template('error.html', babson_url=babson_url)
    return render_template('ct_course_finder.html', error=None)


@app.route("/courselevelfinder", methods=["GET", "POST"])
def cl_course_list():
    if request.method == "POST":
        try:
            program = str(request.form['program'])
            term = str(request.form['term'])
            year = int(request.form['year'])
            course_level = str(request.form['course_level'])
            url = generate_url(program, term, year)
            course_list = parse_html(download_page(url).read())
            electives_available = course_level_list(course_level, course_list)
            if electives_available:
                return render_template('courselevel_result.html', 
                                        program=program,
                                        term=term,
                                        year=year,
                                        course_level=course_level,
                                        electives_available=electives_available)
            else:
                return render_template('cl_course_finder.html', error=True)
        except:
            return render_template('error.html', babson_url=babson_url)
    return render_template('cl_course_finder.html', error=None)


if __name__ == "__main__":
    app.run(debug=True)