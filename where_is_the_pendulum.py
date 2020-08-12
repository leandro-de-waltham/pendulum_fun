from pylab import *
import glob 
import os

# this script is useful to analyze the movement of a simple pendulum using a camera. 
# I used ffmpeg to encode and decode the videos on a unix os

#this is where I store my data. I extracted the images from the movie and put them in this folder
pathtodata = '/Users/leandro/Documents/pendulums/data/'
frames = sorted(glob.glob(pathtodata+'*.png'))

#this is where I want to store my stuff. I make sure to create the folder if it doesn't exist
pathtostore='/Users/leandro/Documents/pendulums/data/derivative/'
if not os.path.exists(pathtostore):os.makedirs(pathtostore)

#These functions read the sequence of images and do some operations, like substraction, multiplication, etc
#I used these functions to generate frames, and then used ffmpeg to make the clips in my INSTAGRAM post 
def takederivative(frames):
	for i in range(len(frames)-1):
		currentframe = imread(frames[i])
		nextframe = imread(frames[i+1]) 
		derivative = nextframe - currentframe
		figure()
		imshow(derivative*100)
		savefig(pathtostore+'derivative.' +str(i) + '.png')
		close('all')

def takederivative_and_amplify(frames):
	for i in range(len(frames)-1):
		currentframe = imread(frames[i])
		nextframe = imread(frames[i+1]) 
		derivative = nextframe - currentframe
		figure()
		plt.margins(0,0)
		axis('off')
		imshow(derivative*100)
		savefig(pathtostore+'derivative.amp.' +str(i) + '.png', bbox_inches = 'tight',pad_inches = 0)
		close('all')

def takederivative_and_clip(frames):
	clipped_derivatives=[] 
	for i in range(len(frames)-1):
		currentframe = imread(frames[i])
		nextframe = imread(frames[i+1]) 
		derivative = nextframe - currentframe
		figure()
		threshold = 0.1  #I determined the threshold by looking at the numbers in the array, and looking at its max and min values. Trial and error. 
		clipped_derivative = derivative[:,:,2]>threshold
		clipped_derivatives.append(clipped_derivative)
		imshow(clipped_derivative)
		savefig(pathtostore+'derivative.clip.' +str(i) + '.png')
		close('all')
	return clipped_derivatives

def takederivative_clip_and_trim(frames):
	clipped_and_trimmed_derivatives=[] 
	for i in range(len(frames)-1):
		currentframe = imread(frames[i])
		nextframe = imread(frames[i+1]) 
		derivative = nextframe - currentframe
		figure()
		clipped_and_trimmed_derivative = derivative[400:800, 500:1250,2]>0.1
		clipped_and_trimmed_derivatives.append(clipped_and_trimmed_derivative)
		imshow(clipped_and_trimmed_derivative)
		savefig(pathtostore+'derivative.clip.and.trim.' +str(i) + '.png')
		close('all')
	return clipped_and_trimmed_derivatives	


#I want to measure the position of the pendulum to illustrate a nonlinear oscillation 
ctd = takederivative_clip_and_trim(frames)

# I think that if I take the average position of the yellow dots (take derivative, clip using threshold) that should give me a good estimate of the position 
positions =[] 
for ctdframe in ctd: 
	brightpixels_locations = argwhere(ctdframe)
	x = brightpixels_locations[:, 0]
	y = brightpixels_locations[:, 1]
	position = [mean(x) , mean(y)]
	positions.append(position)
positions=array(positions)

#I need to know the sampling rate to put units in my plots
sampling_rate = 298. / 13. #number of frames in my clip divided by total duration of the clip
time = linspace(0, 13, len(positions))
figure(figsize=(5,5))
plot(time, positions[:,1])
xlabel('time [sec]')
ylabel('position [pixel index]')
show()
savefig(pathtostore+'nonlinear_oscillation.png')



# def whereisthependulum(pathtoimage): 

# 	return [x,y] 