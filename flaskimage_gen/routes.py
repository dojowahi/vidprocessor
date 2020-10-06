from flaskimage_gen.models import Vids
from flask import Flask, render_template, flash, redirect, url_for, Response, send_file
from flaskimage_gen.forms import YoutubeURLForm
from flaskimage_gen import app, db
from flaskimage_gen.video_transformer import Extractor
import time
from pathlib import Path

# @app.route("/", methods=['GET','POST'])
# @app.route("/login", methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'a@a.com' and form.password.data == 'a':
#             # flash('You have been logged in!', 'success')
#             return redirect(url_for('geturl'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/", methods=['GET','POST'])
@app.route('/geturl', methods = ['GET','POST'])
def geturl():
    form = YoutubeURLForm()

    if form.validate_on_submit():
        fe = Extractor(form.url.data, vid_type=int(form.radio_out.data))
        # flash(f'URL submitted for conversion', 'success')
        if int(form.radio_out.data) == 0:
            fe.extract_frames()
            img = [e.name for e in fe.img_path.iterdir() if e.match("*.jpg")]
            img_list = ['/static/image/'+fe.filename+'/'+file for file in img]
            print(img_list)
            url = Vids(youtube_url=form.url.data, video_title=fe.myVideo.title, process=form.radio_out.data)
            db.session.add(url)
            db.session.commit()
            return render_template('gallery.html', img_list=img_list)
        elif int(form.radio_out.data) == 1:
            fe.download()
            filename = fe.filename+'.mp4'
            print(str(fe.video_path),str(filename))
            url = Vids(youtube_url=form.url.data, video_title=fe.myVideo.title, process=form.radio_out.data)
            db.session.add(url)
            db.session.commit()
            # return send_from_directory(str(fe.video_path), filename , as_attachment=True)
            return redirect(url_for('downloadfile', filename=filename, file_type=form.radio_out.data))
        elif int(form.radio_out.data) == 2:
            fe.download()
            filename = fe.filename+'.mp4'
            print(str(fe.video_path),str(filename))
            url = Vids(youtube_url=form.url.data, video_title=fe.myVideo.title, process=form.radio_out.data)
            db.session.add(url)
            db.session.commit()
            # return send_from_directory(str(fe.video_path), filename , as_attachment=True)
            return redirect(url_for('downloadfile', filename=filename, file_type=form.radio_out.data))
        else:
            fe.download()
            filename = fe.filename + '.txt'
            url = Vids(youtube_url=form.url.data, video_title=fe.myVideo.title, process=form.radio_out.data)
            db.session.add(url)
            db.session.commit()
            return redirect(url_for('downloadfile', filename=filename, file_type=form.radio_out.data))
    else:
        return render_template('URLgetter.html', title='URL', form=form)


@app.route("/admin", methods = ["GET","POST"])
def admin():
    processed_vids = Vids.query.all()
    return render_template('admin.html', vids=processed_vids)


@app.route("/admin/delete/<id>")
def delete(id):
    delete_vids = Vids.query.all()
    delete_vids = Vids.query.get_or_404(id)
    db.session.delete(delete_vids)
    db.session.commit()
    return redirect('/admin')


@app.route("/downloadfile/<filename>/<file_type>", methods = ['GET'])
def downloadfile(filename,file_type):
    if file_type == "1":
        filename = '/static/audio/'+filename
    elif file_type == "2" :
        filename = '/static/aud_vid/'+filename
    elif file_type == "3" :
        filename = '/static/text/'+filename

    print(filename)
    return render_template('download.html', value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    return send_file(filename, as_attachment=True, attachment_filename='')


@app.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')