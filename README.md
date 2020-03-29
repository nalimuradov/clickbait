# YouTube Video View Predictor

https://nariman.herokuapp.com/

Can take up to 30 seconds to load.
Some parts of the project such as the models or data are not in the repo due to size/privacy issues.

###  Predicting the Success of a YouTube Video

#### Introduction:

Clickbait has been around since the dawn of the internet and continues to strive as advertisers pay based on page view counts. Creators on platforms such as YouTube want to maximize views in order to earn money and grow their channel. 

If a YouTube creator wants to catch the attention of a new viewer, they must do so with the only things they see on their recommended bar: the **title of the video** and the **thumbnail image**. 

I wanted to see how significantly the 'first impression' of a video can affect the amount of views it will get, if at all.

![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img1.png "Sample recommended video")

Above is an example of what you see when you are recommended a video. The title and the thumbnail are what decide if you click on it or not, assuming you are not familiar with the channel.

NOTE: I am not affiliated with any of the channels used in the images.

#### The Data:

Obtaining suitable data was the most difficult part. The videos we want are the videos whose goal is to get viewed by as many people as possible. These are channels whose goal are to grow their platform through their content on the channel. As such, we must exclude videos like those for school projects, whose goal

Now that we have the videos, we need to extract the title, thumbnail URL, view count, and channel subscriber count for each one.
The title and thumbnail will be converted into vectors to be used as the features, and the view count will be the label. It's clear we need the subscriber count to put the view count in context; a 10 000 view video for a 100 000 subscriber channel is low, but it's high for a channel with only 1 000 subscribers. 

Video recency is also important when selecting videos. Older videos are in the context of fewer subscribers and we must account for the
growth of the channel over time.


##### Extracting information from the video title

I decided against using a bag of words as I didn't have nearly enough data to prevent overfitting. Instead I used NLTK's part-of-speech tagger and did a count on those tags. I thought that instead of finding certain words that attract more views, I could find a certain sentence structure that would.

I used 21 of the 36 Penn Treebank POS tags, excluding very rare parts of speech to have a smaller feature vector. This is important as I then expanded the feature vector to count sequential pairs of tags found in the title. For example, I would now also track how many times a noun followed by another noun appears. This would pseudo-track the word position and hopefully find sequences of tags that get more views than others.

##### Extracting information from the thumbnail image

The thumbnail was extracted as a 480x360 matrix of RGB pixels as some videos couldn't guarantee having higher resolution thumbnails. Keeping it simple, I decided against using a pretrained net and relied on a basic regressor to see if any correlations are found. This part was fairly straightforward.



#### Results:
![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img2.png "Successful videos")

Bad Videos - I don't want to show videos as 'bad' as they aren't but less successful. eg. titles like 'vidcon vlog 9: joe smith'
Not many people have bad titles and thumbnails nowadays. 

![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img3.png "More successful video")
![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img4.png "Less successful video")

If content is good, title or thumbnail will be mostly irrelevant.

Some titles and thumbnails can generate more views than others, but alone cannot predict how successful a video will be. The content
of the video will be the main driving force and no title or thumbnail can save an awful video.

eg. Minecraft creeper walkthrough part 55 vs. I TAME A MINECRAFT CREEPER (SUPER RARE)

Second title will get more views but if the video was bad from the get go it won't matter much. What matters is are you interesting? Is the video interesting?

Creators have already caught on to ways of making their videos more appealing, so it's becoming rare. The videos with the lowest view counts usually had titles that were somehwat interesting with good thumbnails, but the content was bland. That's why there are videos with enticing titles or thumbnails with no views and vice versa.


