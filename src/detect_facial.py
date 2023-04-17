from feat import Detector

if __name__ == '__main__':
  face = Detector(
    face_model = 'retinaface',
    landmark_model = 'mobilefacenet',
    au_model = 'xgb',
    emotion_model = 'resmasknet',
    facepose_model = 'img2pose',
  ).detect_image('画像ファイルフルパス')

  result = {'笑顔': face.emotions['happiness'][0]}
  print(result)
