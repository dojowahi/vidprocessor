import math
import datetime
import pytube
import cv2
import uuid
import pathlib
import moviepy.editor as mp
from youtube_transcript_api import YouTubeTranscriptApi


class Extractor():
    '''
    Class used for downloading and transforming video file.
    '''

    def __init__(self, url="https://www.youtube.com/watch?v=668nUCeBHyY", vid_type=0):

        self.base_path = pathlib.Path('C:/Users/682528/pythonproj/youtube_video_processor/vidprocessor/flaskimage_gen/static')
        self.url = url
        self.vid_type = vid_type
        if self.vid_type == 0:
            self.video_path = self.base_path/'video'
        elif self.vid_type == 1:
            self.video_path = self.base_path/'audio'
        elif self.vid_type == 2:
            self.video_path = self.base_path/'aud_vid'
        else:
            self.video_path = self.base_path /'text'

        if not self.video_path.is_dir():
            pathlib.Path.mkdir(self.video_path)

        self.img_path = None
        self.vid_cap = None
        self.n_frames = None
        self.fps = None
        self.filename = str(uuid.uuid4())
        self.abs_path_suffix = None
        self.myVideo = None

    def download(self):
        try:
            self.myVideo = pytube.YouTube(str(self.url))
            print("Title: " + self.myVideo.title)
            # print("Duration: " + str(myVideo.length))
            print("Video Id: " + str(self.myVideo.video_id))
            if self.vid_type == 0:
                success = self.only_video_download()
            elif self.vid_type == 1:
                success = self.audio_download()
            elif self.vid_type == 2:
                success = self.audio_video_download()
            else:
                print(f'Download transcript')
                success = self.text_download()

            return success

        except KeyError as e:
            print('KeyError - reason "%s"' % str(e))
            print('Skipping Video - : ' + self.url)
            exit(1)

    def only_video_download(self):
        print(self.video_path, self.vid_type)
        stream = self.myVideo.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path=self.video_path, filename=self.filename)
        print(f'Video of {self.url} has been downloaded')
        abs_path = self.video_path / self.filename
        self.abs_path_suffix = abs_path.with_suffix('.mp4')
        self.vid_cap = cv2.VideoCapture(str(self.abs_path_suffix))
        self.n_frames = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.vid_cap.get(cv2.CAP_PROP_FPS))
        duration = self.n_frames / self.fps
        print(f'Duration: {datetime.timedelta(seconds=duration)}')
        return True

    def audio_download(self):
        print(self.video_path, self.vid_type)
        stream = self.myVideo.streams.filter(file_extension='mp4').filter(only_audio=True).first()
        # Download audio and video
        # stream = self.myVideo.streams.first()
        stream.download(output_path=self.video_path, filename=self.filename)
        print(f'Audio of {self.url} has been downloaded')
        # abs_path = self.video_path / self.filename
        # self.abs_path_suffix = abs_path.with_suffix('.mp4')
        # tgt_path_wav = abs_path.with_suffix('.wav')
        #
        # clip = mp.AudioFileClip(str(self.abs_path_suffix))
        # clip.write_audiofile(str(tgt_path_wav))

        return True

    def audio_video_download(self):
        print(self.video_path, self.vid_type)
        # Download audio and video
        stream = self.myVideo.streams.first()
        stream.download(output_path=self.video_path, filename=self.filename)
        print(f'Audio and Video of {self.url} has been downloaded')
        return True

    def text_download(self):
        captions = self.myVideo.captions.get_by_language_code('en')
        abs_path = self.video_path / self.filename
        self.abs_path_suffix = abs_path.with_suffix('.txt')
        if captions:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.myVideo.video_id)
            transcript = transcript_list.find_transcript(['en'])
            with open(self.abs_path_suffix,'w') as f:
                for line in transcript.fetch():
                    f.write('%s\n' % line)
        else:
            print("No captions available in English")
            with open(self.abs_path_suffix, 'w') as f:
                f.write("No captions available in English")
        return True



    def get_n_images(self, every_x_frame):
        n_images = math.floor(self.n_frames / every_x_frame) + 1
        print(f'Extracting every {every_x_frame} (nd/rd/th) frame would result in {n_images} images.')

    def extract_frames(self, every_x_frame=100, img_name='flask', img_ext='.jpg',color=None):
        self.download()
        self.get_n_images(every_x_frame)
        self.img_path = self.base_path / 'image'
        if not self.img_path.is_dir():
            pathlib.Path.mkdir(self.img_path)

        self.img_path = self.img_path / self.filename
        if not self.vid_cap.isOpened():
            self.vid_cap = cv2.VideoCapture(self.video_path)

        if self.img_path is None:
            self.img_path = pathlib.Path.cwd()
        else:
            if not self.img_path.is_dir():
                pathlib.Path.mkdir(self.img_path)
                print(f'Created the following directory: {self.img_path}')

        print(self.img_path)

        frame_cnt = 0
        img_cnt = 0

        while self.vid_cap.isOpened():

            success, image = self.vid_cap.read()

            if not success:
                break

            if frame_cnt % every_x_frame == 0:
                img_file = ''.join([img_name, '_', str(img_cnt), img_ext])
                img_abs_path = self.img_path/img_file
                if color == 'gray':
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(str(img_abs_path), gray)
                else:
                    cv2.imwrite(str(img_abs_path), image)
                img_cnt += 1

            frame_cnt += 1

        self.vid_cap.release()
        cv2.destroyAllWindows()



# video_url = 'https://www.youtube.com/watch?v=FUiu-cdu6mA'
audio_url = 'https://www.youtube.com/watch?v=fT67ta4VrQQ'
text_url ='https://www.youtube.com/watch?v=3EbTr79wLkU'
vid_aud_url = 'https://www.youtube.com/watch?v=fT67ta4VrQQ'
# 'https://www.youtube.com/watch?v=fT67ta4VrQQ'
# fe = Extractor(text_url,3)
# fe = Extractor(video_url,0)
# fe = Extractor(vid_aud_url,2)
# fe.download()
# fe.extract_frames(100,'trail')