from flask import Flask,  request ,render_template
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
        logtime=float(request.form.get('Lsw'))
        interactiontime=int(request.form.get('Ith'))
        leadvsquality=int(request.form.get('Ivsq'))

        
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

if __name__ == "__main__":
    app.run(debug=True)