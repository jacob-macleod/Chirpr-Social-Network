from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import pymongo
import json
import ast

print ("Remember to start mongodb in the terminal, possibly using sudo systemctl start mongod!")

app = Flask(__name__)
global username
username = ""

#Initialise mongodb
client = pymongo.MongoClient()
database = client["social_app_db"]

#Add a posts collection
posts = database["posts"]
login_data = database["login_data"]

ENCRYPTION_KEY = 5
letters = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']


#Encrypt a sring
def encrypt(string) :
    encryption = ""
    global encrypted 
    encrypted = 0

    #Convert string to array
    string = [ch for ch in string]

    for i in range(0, len(string)):
        encrypted = 0
        for b in range(0, len(letters)) :
            if string[i] == letters[b] :
                if b+ENCRYPTION_KEY >= len(letters) :
                    encryption = encryption + letters[b-ENCRYPTION_KEY]
                else :
                    encryption = encryption + letters[b+ENCRYPTION_KEY]
                encrypted = 1
            b = b + 1

        if encrypted == 0:
            encryption = encryption + string[i]
        i = i + 1 
    return encryption


#Decrypt a string
def decrypt(string) :
    decryption = ""
    global decrypted 
    decrypted = 0

    #Convert string to array
    string = [ch for ch in string]

    for i in range(0, len(string)):
        decrypted = 0
        for b in range(0, len(letters)) :
            if string[i] == letters[b] :
                if b+ENCRYPTION_KEY > len(letters) :
                    decryption = decryption + letters[b-ENCRYPTION_KEY]
                elif b+ENCRYPTION_KEY*2 >= len(letters) :
                    decryption = decryption + letters[b+ENCRYPTION_KEY]
                else :
                    decryption = decryption + letters[b-ENCRYPTION_KEY]
                decrypted = 1
            b = b + 1

        if decrypted == 0:
            decryption = decryption + string[i]
        i = i + 1 
    return decryption


#Clumsily-named but self-explanitory
def find_whether_cookies_or_parameters_store_username () :
    global username

    if request.cookies.get("username") != None or request.cookies.get("username") != "":
        return "cookies"
    elif username != "" :
        return "variables"
    else :
        return None

def replace_single_with_double_quotes (string) :
    replaced_string = ""
    split_string = string.split("'")
    for i in range(0, len(split_string)) :
        if i != len(split_string)-1 :
            replaced_string = replaced_string + split_string[i] + '"'
        else :
            replaced_string = replaced_string + split_string[i]
    return replaced_string


#If you need to follow or unfollow someone, follow or unfollow them, or if mode=="view", only check if they are followed
def check_for_follow (user_name, profile_name, mode) :
    following = ""
    name = ""
    #Iterate through login_data and get value for username, then the following thing for username. If no no values in this value == the cookie
    #Followed, append the value of the cookie followed to login_data  following
    try :
        for x in login_data.find() :
            name = decrypt(login_data.find_one({encrypt("username"):{"$eq":encrypt(profile_name)}}).get(encrypt("username")))
            following = decrypt(login_data.find_one({encrypt("username"):{"$eq":encrypt(profile_name)}}).get(encrypt("following")))
            
            #Detect --%---/ symbol which means unfollow 
            if request.cookies.get("followed").split("/")[0] == "--%---" :
                #Unfollow user_name
                following = following.split("%")
                following_str = ""

                #Save following to a new str but don't count following[i] if the username == the username you want to unfollow 
                for i in range(0, len(following)) :
                    print (request.cookies.get("username"))
                    if following[i] != request.cookies.get("username") :
                        if following[i] != "" :
                            following_str = following_str + "%" + following[i]
                    i = i + 1

                #Update following_str (following minus the username you want to follow) to mongodb
                if mode == "edit" :
                    login_data.update_one({encrypt("username"):encrypt(profile_name)}, {"$set": {encrypt("following"):encrypt(following_str)}})
                return "False"

            else :
                #If the cookie followed is in the list of people followed of user_name
                if request.cookies.get("followed") not in following:
                    x = following + "%" + request.cookies.get("followed")

                    #Follow the username in cookies "followed" if the conditions are right
                    if mode == "edit" and request.cookies.get("followed") != "%NoneValue%":
                        login_data.update_one({encrypt("username"):encrypt(profile_name)}, {"$set": {encrypt("following"):encrypt(following + "%" + request.cookies.get("username"))}})

                #Detect if profile_name has been folowed
                following = following.split("%")
                for i in range(0, len(following)) :
                    if username == following[i] :
                        return "True"
                    i = i + 1

                #If a profile_name follow has not been detected
                return "False"
    except Exception as e:
        print (e)
        return "False"


def count_followers() :
    profile_name = request.cookies.get("profile_clicked")
    followers = decrypt(login_data.find_one({encrypt("username"):{"$eq":encrypt(profile_name)}}).get(encrypt("following"))).split("%")
    i = 0
    follower_count = 0


    for i in range(0, len(followers)) :
        if followers[i] != "" :
            follower_count = follower_count + 1
        i = i + 1

    return follower_count


#Finds all posts from the users the currently logged in user has followed
def find_follower_posts () :
    username = request.cookies.get("username")
    
    if username != None :
        for x in login_data.find() :
            x = x.get(encrypt("following")).split("%")
            for i in range(0, len(x)) :
                s = decrypt(x[i])
                if username == decrypt(x[i]) :
                    print ("Match found! - x is " + decrypt(x[i]))
                i = i + 1

    #If the user is not logged in
    else :
        return ["You aren't logged in!"]





@app.route("/")
def index():
    global username
    if username == "":
        if request.cookies.get("username") != None or request.cookies.get("username") != "":
            username = request.cookies.get("username")


    post_contents = request.cookies.get("post")
    

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
        bio = request.form.get("bio")
        username = request.form.get("uname") 
        password = request.form.get("pword") 
        password_confirm = request.form.get("pword_confirm") 

        #Check username already exists
        try :
            tempory_username = login_data.find_one({encrypt("username"):{"$eq":encrypt(username)}}).get(encrypt("username"))
            user_exists = True
        except:
            user_exists = False

        #Check if password and confirmed passwords match and if user already exists, and if they do, direct to an error page
        if password != password_confirm or user_exists == True:
            username = ""
            return render_template("login_failed.html")
        else :
            login = {encrypt("username"):encrypt(username), encrypt("password"):encrypt(password), encrypt("bio"):encrypt(bio), encrypt("following"):encrypt("%" + username)}
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
            if decrypt(login_data.find_one({encrypt("username"):{"$eq":encrypt(username)}}).get(encrypt("username"))) != "" and login_data.find_one({encrypt("password"):{"$eq":encrypt(password)}}).get(encrypt("password")) != "" :
                username = username
                return render_template("redirect_to_index.html")
        except :
            username = ""
            return render_template("signin_failed.html")
    return render_template("sign_in.html")

@app.route("/profile")
def profile () :
    user_posts = []
    profile = request.cookies.get("profile_clicked")
    #Follow users if you need to
    check_for_follow(request.cookies.get("username"), profile, "edit")


    try :
        bio = decrypt(login_data.find_one({encrypt("username"):{"$eq":encrypt(profile)}}).get(encrypt("bio")))
    except :
        return "<h1>Sorry, here's been an intenal server error</h1><p>The server either doesn't know who's profile you want to see or the person's profile that you want to see doesn't exist</p>"
    
    #Save all posts user has made to an array
    #Check for null values before actually defining user_posts
    try :
        for x in posts.find({"username":{"$eq":profile}}, {"_id":0}) :
            user_posts.append(x.get("post"))
    except :
        user_posts = ["Please enter a post to view them!"]
    
    #Returns check_follow AFTER relevant changes have been made
    return render_template("profile.html", username=profile, bio=bio, posts=user_posts, check_follow=check_for_follow(request.cookies.get("username"), profile, "view"), followers=count_followers())


@app.route("/search", methods=["POST", "GET"])
def search () :
    search_results = []

    #If the user searches for something
    if request.method == "POST":
        search_term = request.form.get("search") 
        #Save usernames with search_term in and save them to an array 
        for x in login_data.find() :
            if search_term in decrypt(x.get(encrypt("username"))) :
                search_results.append(decrypt(x.get(encrypt("username"))))
        return render_template("profile_search.html", results=search_results)

    #If the user doesn't search
    return render_template("profile_search.html", results="None")

@app.route("/following", methods=["POST", "GET"])
def following () :
    find_follower_posts()
    return render_template("following.html")


if __name__ == "__main__":
    app.run(port=5001)