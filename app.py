from flask import Flask, render_template, request
import course_listings
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def course_list():
    if request.method == "POST":
        program = str(request.form['program'])
        term = str(request.form['term'])
        year = int(request.form['year'])
        concentration = str(request.form['concentration'])
        url = generate_url(program, term, year)
        if course_list:
            return render_template('result.html', 
                course_list=course_list)
    else:
        return render_template('index.html')
    return render_template('index_html')


if __name__ == "__main__":
    app.run(debug=True)