from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import pymongo
import json

app = Flask(__name__)
global username
username = ""

#Initialise mongodb
client = pymongo.MongoClient()
database = client["social_app_db"]

#Add a posts collection
posts = database["posts"]
login_data = database["login_data"]


#Clumsily-named but self-explanitory
def find_whether_cookies_or_parameters_store_username () :
    global username

    if request.cookies.get("username") != None or request.cookies.get("username") != "":
        return "cookies"
    elif username != "" :
        return "variables"
    else :
        return None

@app.route("/")
def index():
    global username
    if username == "" and request.cookies.get("username") != None or request.cookies.get("username") != "":
        username = request.cookies.get("username")


    post_contents = request.cookies.get("post")
    
    #print (posts.find_one({"username":{"$eq":request.cookies.get("username")}}).get("username"))
    print (find_whether_cookies_or_parameters_store_username())

    #Save all the posts a user has made to an array and if needed, saves new posts to an array
    user_posts = []
    if find_whether_cookies_or_parameters_store_username() == "cookies" :
        if post_contents != "%NoneValue%" :
            post_data = {"username":request.cookies.get("username"), "post":post_contents}
            posts.insert_one(post_data)

    elif find_whether_cookies_or_parameters_store_username() == "variables" :
        if post_contents != "%NoneValue%" :
            post_data = {"username":username, "post":post_contents}
            posts.insert_one(post_data)


    #Save all posts user has made to an array
    #Check for null values before actually defining user_posts
    try :
        for x in posts.find({"username":{"$eq":username}}, {"_id":0}) :
            user_posts.append(x.get("post"))
    except :
        user_posts = ["Please enter a post to view them!"]


    
    #If the user is not logged in
    if request.cookies.get("username") == None or request.cookies.get("username") == "" and username == "":
        return render_template("login.html", username=username)
    else :
        return render_template("index.html", username=username, user_posts=user_posts)
    return render_template("index.html", username=username, user_posts=user_posts)



@app.route("/sign_up", methods=["POST", "GET"])
def sign_up () :
    global username
    if request.method == "POST":
        username = request.form.get("uname") 
        password = request.form.get("pword") 
        password_confirm = request.form.get("pword_confirm") 

        #Check username already exists
        try :
            if login_data.find_one({"username":{"$eq":username}}).get("username") != "" :
                user_exists = True
        except:
            user_exists = False

        #Check if password and confirmed passwords match and if user already exists, and if they do, direct to an error page
        if password != password_confirm or user_exists == True:
            username = ""
            return render_template("login_failed.html")
        else :
            login = {"username":username, "password":password}
            login_data.insert_one(login)
            return render_template("redirect_to_index.html")
    return render_template("sign_up.html", username=username)


@app.route("/sign_in", methods=["POST", "GET"])
def sign_in () :
    global username

    #If user clicked sign in
    if request.method == "POST" and request.form.get("uname") != None:
        username = request.form.get("uname") 
        password = request.form.get("pword") 

        #See if the username and password match the one in the database and display an error page or redirect to the main page accordingly
        try :
            if login_data.find_one({"username":{"$eq":username}}).get("username") != "" and login_data.find_one({"password":{"$eq":password}}).get("username") != "" :
                username = username
                return render_template("redirect_to_index.html")
        except :
            username = ""
            return render_template("signin_failed.html")
    return render_template("sign_in.html")


if __name__ == "__main__":
    app.run(port=5001)