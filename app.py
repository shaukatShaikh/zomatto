from flask import Flask,render_template,request
import pickle
# import sklearn
import warnings
warnings.filterwarnings('ignore')
import os

with open('zomatto_model.pkl','rb') as my_file:
    unpickler=pickle.Unpickler(my_file)
    model=unpickler.load()
    print(model)

with open('encoder.pkl','rb') as my_file:
    unpickler=pickle.Unpickler(my_file)
    encoder=unpickler.load()


app=Flask(__name__)

@app.route("/",methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/text',methods=['POST'])
def predict_price():
    if request.method=="POST":
        book_table=int(request.form['book_table'])
        votes=int(request.form['votes'])
        cost=int(request.form['cost'])
        location=request.form['location']
        type_=request.form['type_']
        location ,type_= encoder.transform([[location,type_]])[0]
        location = int(location)
        type_ = int(type_)

        # return render_template('home.html')
        


        prediction=model.predict([[book_table,
                                votes,
                                cost,
                                location,
                                type_]])
        output=round(prediction[0],2)


    return render_template('home.html',prediction_text=f'The Ratings of the Restousrent will be {output}')



if  __name__ == "__main__":
    app.run(debug=True)


