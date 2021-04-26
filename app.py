from flask import Flask, render_template, request
from course_listings import parse_html, generate_url, download_page, student_course_list
app = Flask(__name__)
global babson_url
babson_url = 'https://fusionmx.babson.edu/CourseListing/?blnShowHeader=true'



@app.route("/")
def home_page():
    return render_template('homepage.html')



@app.route("/coursefinder", methods=["GET", "POST"])
def course_list():
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
                return render_template('result.html', 
                                        program=program,
                                        term=term,
                                        year=year,
                                        concentration=concentration,
                                        concentration_courses=concentration_courses)
            else:
                return render_template('course_finder.html', error=True)
        except:
            return render_template('error.html', babson_url=babson_url)
    return render_template('course_finder.html', error=None)



if __name__ == "__main__":
    app.run(debug=True)