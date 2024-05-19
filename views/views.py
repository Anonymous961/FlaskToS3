# views.py

from flask import (
    render_template,
    flash,
    request,
    redirect,
    url_for,
    Blueprint,
    send_file,
)
from utils.helpers import upload_file_to_s3, list_files_in_s3, download_file_from_s3
import os

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

views = Blueprint("views", __name__)


@views.route("/")
def home():
    files = list_files_in_s3()
    return render_template("home.html", files=files)


@views.route("/error")
def error():
    return render_template("notupload.html")


# function to check file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route("/upload", methods=["POST"])
def create():

    # check whether an input field with name 'user_file' exist
    if "user_file" not in request.files:
        flash("No user_file key in request.files")
        return redirect(url_for("views.home"))

    # after confirm 'user_file' exist, get the file from input
    file = request.files["user_file"]

    # check whether a file is selected
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("views.home"))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)

        # if upload success,will return file name of uploaded file
        if output:
            # write your code here
            # to save the file name in database

            flash("Success upload")
            return redirect(url_for("views.home"))

        # upload failed, redirect to upload page
        else:
            flash("Unable to upload, try again")
            return redirect(url_for("views.error"))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for("views.error"))


@views.route("/download/<filename>")
def download(filename):
    try:
        download_path = download_file_from_s3(filename)
        return send_file(download_path, as_attachment=True)
    except Exception as e:
        flash("Unable to download file: {}".format(e))
        return redirect(url_for("views.home"))
