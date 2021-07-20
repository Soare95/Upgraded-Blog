from flask import Flask, render_template, request
import requests
from datetime import datetime
import smtplib


MY_EMAIL = "YOUR_EMAIL"
MY_PASSWORD = "YOUR_PASSWORD"
TO_EMAIL = "HIS_PASSWORD"

app = Flask(__name__)
date = datetime.today().strftime("%B %d, %Y")

all_posts = requests.get("https://api.npoint.io/6a8be5a3249d676750a1").json()


@app.route("/")
def home():
    return render_template("index.html", all_posts=all_posts, date=date)


@app.route("/about")
def about_me():
    return render_template("about.html")


@app.route("/post/<int:number>")
def show_post(number):
    requested_post = None
    for post in all_posts:
        if post["id"] == number:
            requested_post = post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["POST", "GET"])
def contact_me():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=120)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=f"Subject:Form Received\n\nYou received a form:\n"
                                                                    f"From: {name}\n"
                                                                    f"Email: {email}\n"
                                                                    f"Phone: {phone}\n"
                                                                    f"Message: {message}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)