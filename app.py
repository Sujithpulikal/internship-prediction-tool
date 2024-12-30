from flask import Flask,  request ,render_template
import math
import pickle
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
app = Flask(__name__)

model = pickle.load(open('model1.pkl', 'rb'))
encoders = pickle.load(open('encoder.pkl', 'rb'))

model1 = pickle.load(open('model2.pkl', 'rb'))
encoders1 = pickle.load(open('label_encoders1.pkl', 'rb'))

model2 = pickle.load(open('attrition.pkl', 'rb'))
encoders2 = pickle.load(open('encoderatt.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/lead")
def lead():
    return render_template("lead.html")
@app.route("/attrition")
def attrition():
    return render_template("attrition.html")
@app.route("/placement")
def placement():
    return render_template("placement.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/confirm', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        age = int(request.form.get('age'))
        course = request.form.get('course')

        leadsource=request.form.get('ls')
        totalvisit=int(request.form.get('TotalVisits'))
        timespentonwebsite=int(request.form.get('Tws'))
        lastactivity=request.form.get('Las')
        country=request.form.get('Country')
        city=request.form.get('City')
        occupation=request.form.get('Op')
        tags = request.form.get('Tags')
        leadquality=request.form.get('LQ')
        pageviewpervisit=float(request.form.get('Pvpv'))
        perferdcontactmethod=request.form.get('Pcm')
        engagementscore=int(request.form.get('Es'))
        Qualification=request.form.get('Qualification')
        leadinterstlevel=int(request.form.get('Lil'))
        contactedhour=int(request.form.get('Ch'))
        daysincepastinteraction=int(request.form.get('Dsli'))
        coursefee=float(request.form.get('Cfo'))
        potentialscore=int(request.form.get('Ps'))
        logtime=round(math.log(timespentonwebsite),6)
        interactiontime=timespentonwebsite*contactedhour
        

        
        fields = {
            "Course": course,
            "LeadSource": leadsource,
            "LastActivity": lastactivity,
            "Occupation": occupation,
            "Tags": tags,
            "LeadQuality": leadquality,
            "PreferredContactMethod": perferdcontactmethod,
            "Qualification": Qualification,
            "co": country,
            "co1": city
        }

        encoded_values = {}
        for field, value in fields.items():
            encoded_values[field] = int(encoders[field].transform([value]))
        
        course_encoded = encoded_values["Course"]
        leadsource_encoded = encoded_values["LeadSource"]
        lastactivity_encoded = encoded_values["LastActivity"]
        occupation_encoded = encoded_values["Occupation"]
        tags_encoded = encoded_values["Tags"]
        leadquality_encoded = encoded_values["LeadQuality"]
        preferedcontactmethod_encoded = encoded_values["PreferredContactMethod"]
        qualification_encoded = encoded_values["Qualification"]
        country_encoded = encoded_values["co"]
        city_encoded = encoded_values["co1"]
        if leadquality_encoded==0:
            leadvsquality=3*leadinterstlevel
        elif leadquality_encoded==1:
            leadvsquality=1*leadinterstlevel
        else:
            leadvsquality=2*leadinterstlevel

        predict_list=[age,course_encoded,leadsource_encoded,totalvisit,timespentonwebsite,lastactivity_encoded,
                      country_encoded,city_encoded,occupation_encoded,tags_encoded,leadquality_encoded,
                      pageviewpervisit,preferedcontactmethod_encoded,engagementscore,qualification_encoded,leadinterstlevel,
                      contactedhour,daysincepastinteraction,coursefee,potentialscore,interactiontime,leadvsquality]
        prediction = model.predict([predict_list])
        y=int(prediction)
        return render_template('confirm.html', a=name,b=age,c=course,d=leadsource,e=totalvisit,f=timespentonwebsite,g=lastactivity,
                               h=country,i=city,j=occupation,k=tags,l=leadquality,m=pageviewpervisit,
                               n=perferdcontactmethod,o=engagementscore,p=Qualification,q=leadinterstlevel,
                               r=contactedhour,s=daysincepastinteraction,t=coursefee,
                               u=potentialscore,v=logtime,w=interactiontime,x=leadvsquality,y=y)
    return render_template('lead.html')

@app.route('/confirm1', methods=['POST', 'GET'])
def register1():
    if request.method == "POST":
        name = request.form.get('name')
        age = int(request.form.get('age'))
        department = request.form.get('department')
        duration = int(request.form.get('duration'))
        performance_score = float(request.form.get('performance_score'))
        attendance_rate = float(request.form.get('attendance_rate'))
        socio_status = request.form.get('socio_status')
        projects = request.form.get('projects')
        hours_worked = int(request.form.get('hours_worked'))
        mentorship = request.form.get('mentorship')
        distance = float(request.form.get('distance'))
        job_satisfaction = request.form.get('job_satisfaction')
        worklife_index = float(request.form.get('worklife_index'))
        performance_adjusted = float(request.form.get('performance_adjusted'))
        engagement = float(request.form.get('engagement'))
        socio_perf = float(request.form.get('socio_perf'))

        fields2 = {
        'Department':department,
        'Socioeconomic Status':socio_status,
        'Mentorship Level':mentorship,
        'Participation in Projects':projects,
        'Job Satisfaction':job_satisfaction
        }


        encoded_values2 = {}
        for field, value in fields2.items():
            encoded_values2[field] = int(encoders2[field].transform([value]))

        department_encoded=encoded_values2['Department']
        socio_status_encoded=encoded_values2['Socioeconomic Status']
        mentorship_encoded=encoded_values2['Mentorship Level']
        projects_encoded=encoded_values2['Participation in Projects']
        job_satisfaction_encoded=encoded_values2['Job Satisfaction']

        predict_list2=[age,department_encoded,duration,performance_score,attendance_rate,socio_status_encoded,projects_encoded
                      ,hours_worked,mentorship_encoded,distance,job_satisfaction_encoded,worklife_index,engagement]

        prediction = model2.predict([predict_list2])
        y=int(prediction)
        


        return render_template('confirm1.html', a=name,b=age,c=department,d=duration,e=performance_score,
                               f=attendance_rate,g=socio_status,
                               h=projects,i=hours_worked,j=mentorship,k=distance,l=job_satisfaction,m=worklife_index,
                               n=performance_adjusted,o=engagement,p=socio_perf,q=y)
        
        



    return render_template('attrition.html')

@app.route('/confirm2', methods=['POST', 'GET'])
def register2():
    if request.method == "POST":
        name1 = request.form.get('name1')
        age1 = int(request.form.get('age1'))
        department1 = request.form.get('department1')
        duration1= int(request.form.get('duration1'))
        performance_score1 = float(request.form.get('performance_score1'))
        attendance_rate1 = float(request.form.get('attendance_rate1'))
        socio_status1 = request.form.get('socio_status1')
        projects1 = int(request.form.get('projects1'))
        tech = float(request.form.get('tech_skill'))
        soft = float(request.form.get('soft_skill'))
        hours_worked1 = int(request.form.get('hours_worked1'))
        mentorship1 = request.form.get('mentorship1')
        distance1 = float(request.form.get('distance1'))
        recommendscore = int(request.form.get('recommendation_score'))
        skillcomposite = float(request.form.get('skill_composite'))
        performpjt = float(request.form.get('performance_project'))
        placementindex = float(request.form.get('placement_likelihood'))
        socioengmnt = float(request.form.get('socio_engagement'))

        fields1 = {
            "Department": department1,
            "Socioeconomic Status": socio_status1,
            "Mentorship Level": mentorship1
        }

        encoded_values1 = {}
        for field, value in fields1.items():
            encoded_values1[field] = int(encoders1[field].transform([value]))

        dept_encoded = encoded_values1["Department"]
        socio_status1_encoded = encoded_values1["Socioeconomic Status"]
        mentorship1_encoded = encoded_values1["Mentorship Level"]

        predict_list1=[age1,dept_encoded,duration1,performance_score1,attendance_rate1,socio_status1_encoded,
                      projects1,tech,soft,hours_worked1,mentorship1_encoded,distance1,recommendscore,performpjt,placementindex,socioengmnt
                      ]
        prediction1 = model1.predict([predict_list1])

        return render_template('confirm2.html', a=name1,b=age1,c=department1,d=duration1,e=performance_score1,
                               f=attendance_rate1,g=socio_status1,
                               h=projects1,i=tech,j=soft,k=hours_worked1,l=mentorship1,m=distance1,
                               n=recommendscore,o=skillcomposite,p=performpjt,q=placementindex,r=socioengmnt,s=int(prediction1))

if __name__ == "__main__":
    app.run(debug=True)