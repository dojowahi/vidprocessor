from flaskimage_gen import db
from datetime import datetime


class Vids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_url = db.Column(db.String(500), nullable=False)
    video_title = db.Column(db.String(500), nullable=False)
    process = db.Column(db.String(100), nullable=False)
    date_processed = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __repr__(self):
        return f"URL ('{self.youtube_url}')"
