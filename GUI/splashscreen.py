from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt


class VideoSplashScreen(QDialog):
    def __init__(self, video_file, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Splash Screen")
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setFixedSize(700, 500)

        # Create video widget
        self.video_widget = QVideoWidget(self)

        # Create media player
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # Load video
        self.media_player.setSource(QUrl.fromLocalFile(video_file))

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)

        # Connect media player end event
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)

    def showEvent(self, event):
        self.media_player.play()
        super().showEvent(event)

    def on_media_status_changed(self, status):
        # Check if the video is finished
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.accept()  # Close the video dialog
