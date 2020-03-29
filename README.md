# YouTube Video View Predictor

https://nariman.herokuapp.com/

Can take up to 30 seconds to load.
Some parts of the project such as the models or data are not in the repo due to size/privacy issues.

###  Predicting the Success of a YouTube Video

#### Introduction:

Garnering YouTube views . To test the effects, I made regression models that only use features the user can see before clicking on the video: the title of the video and the thumbnail image. Using these basic regressors, I wanted to see how significantly the 'first impression' of a video can affect the amount of views it will get, if at all. Below are the results.

Inline-style: 
![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/img1.png "Logo Title Text 1")

[Image here of youtueb title and video]

#### The Data:

Hardest part was to find 'suitable data'. (eg. music artists, people aren't watching one video over the other because of the title)
Video data was obtained using the Youtube API. I found various 'creator' channels on YouTube who are representative of . These aren't 
music videos or random uploads for a school project. These are 
Many videos on the platform . Picking random videos 

These are channels whose goal are to grow their platform through their content on the channel. This is as opposed to musicians like
Drake who don't need to aptly name their videos. His content  


For each video, I extracted the title, the thumbnail URL, the viewcount, and the channel subscriber count. 

The TITLE (NLP SIDE)
penn treebank pos tags
poscounts of only popular ones (36 -> 22)
 - saves lots of space, can even fuse like NN and NNS
find pairs for pseudo position
 - eg. NN followed by JJ followed by...
decided not to use words themselves as it will overfit
 - eg. cant assume will get all youtube videos
 - as such not perfectly random, as nearly everything

The THUMBNAIL (CV SIDE)
480x360 image
no pretraining
just threw in pixel map as features and view coutn as labels
to see if any pattern found

[Insert Image Here]

It's clear we need the subscriber count to put the view count in context; a 10 000 view video for a 100 000 subscriber channel is low, but it's high for a channel with only 1 000 subscribers. The selection process was not random

Video recency is also important when selecting videos. Older videos are in the context of fewer subscribers and we must account for the
growth of the channel over time. Post frequency also important. If you post 5 videos a day, each video will have fewer views.

#### Results:
[Show images of videos]

Bad Videos - I don't want to show videos as 'bad' as they aren't but less successful. eg. titles like 'vidcon vlog 9: joe smith'
Not many people have bad titles and thumbnails nowadays. 



If content is good, title or thumbnail will be mostly irrelevant.

Some titles and thumbnails can generate more views than others, but alone cannot predict how successful a video will be. The content
of the video will be the main driving force and no title or thumbnail can save an awful video.

eg. Minecraft creeper walkthrough part 55 vs. I TAME A MINECRAFT CREEPER (SUPER RARE)

Second title will get more views but if the video was bad from the get go it won't matter much. What matters is are you interesting? Is the video interesting?

Creators have already caught on to ways of making their videos more appealing, so it's becoming rare. The videos with the lowest view counts usually had titles that were somehwat interesting with good thumbnails, but the content was bland. That's why there are videos with enticing titles or thumbnails with no views and vice versa.


