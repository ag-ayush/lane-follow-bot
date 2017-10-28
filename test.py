import imageio
import pylab

filename = '/home/agoel/git/lane-follow-bot/assets/videos/Video_1.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')
len = vid.get_meta_data()
frames = len['nframes']

image = vid.get_data(10)
fig = pylab.figure()
fig.suptitle('image #{}'.format(10), fontsize=20)
pylab.imshow(image)
pylab.show()




# cap = skvideo.io.VideoCapture('/home/agoel/git/lane-follow-bot/assets/videos/Video_1.mp4')
# cap.open('/home/agoel/git/lane-follow-bot/assets/videos/Video_1.mp4')

# ret, frame = cap.read()
# # Check if camera opened successfully
# if (cap.isOpened() == False):
#   print("Error opening video stream or file")
#
# count = 0
# while True:
#     ret,frame = cap.read()
#     cv2.imshow('window-name',frame)
#     # cv2.imwrite("assets/images/test/frame%d.jpg" % count, frame)
#     count = count + 1
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
#
#
# cap.release()
# # cap.destroyAllWindows()