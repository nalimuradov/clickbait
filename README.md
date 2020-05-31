# YouTube View Predictor

Regressor that gauges how successful a YouTube video title and thumbnail will be in getting views.

Try it at: https://nariman.herokuapp.com/

**Can take a few seconds to load.**
Several parts of the project such as the models or data are not in the repo due to size/privacy.

##  Predicting the Success of a YouTube Video

Clickbait has been around since the dawn of the internet and continues to thrive as advertisers pay based on page view counts. Creators on platforms such as YouTube want to maximize views in order to earn money and grow their channel. 

If a YouTube creator wants to catch the attention of a new viewer, they must do so with the only things they see on their recommended bar: the **title of the video** and the **thumbnail image**. 

The goal of this model was to see how significantly those two factors can affect the view count, if at all.

![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img1.png "Sample recommended video")

>Above is an example of what you see when you are recommended a video. The title and the thumbnail are what decide if you click on it or not, assuming you are not familiar with the channel.

**NOTE:** I am not affiliated with any of the channels used in these images.



## The Data

The videos we want to use as test data should be from *content creator channels*. As such, I've excluded things like **tutorials** or **music videos** as the amount of views those videos will get will be almost entirely dependent on the subject matter. 

> A music video by Drake will always get more views than a music video by me, regardless of what the title or thumbnail are.

From these videos, we need to extract the **title**, **thumbnail URL**, **view count**, and **channel subscriber count** for each one.
The title and thumbnail will be converted into vectors to be used as the features, and the view count will be the label. 

It's clear we need the subscriber count to put the view count into context; 10 000 views on a video is low for a 100 000 subscriber channel, but it's high for a channel with only 1 000 subscribers. 

![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img5.png "Sample data for a video")

>An example of the data for one random video to be used when training the models; the video_id as the key followed by the title, sub count, thumbnail URL, and view count in a list.

It is also important to factor in **post recency** when selecting videos. Older videos were viewed by fewer subscribers and we must account for the growth of the channel over time.

#### Extracting information from the video title

Rather than use a word count (which would require a large amount of data to prevent overfitting), I used NLTK's part-of-speech tagger and did a count on those tags. I thought that instead of finding certain words that attract more views, I could find a certain sentence structure that would.

I used 22 of the 36 Penn Treebank POS tags, excluding very rare parts of speech to have a smaller feature vector. This is important as I then expanded the feature vector to count **sequential pairs of tags** found in the title. For example, I would now also track how many times a noun followed by another noun appears. This would pseudo-track the word position and hopefully find the value of having certain sequences of tags in the title.

#### Extracting information from the thumbnail image

The thumbnail was extracted as a 480x360 matrix of RGB pixels as some videos couldn't guarantee having higher resolution thumbnails. The images were sent through the ResNet50 architecture trained on ImageNet (without the last layer) to get a dense and vastly more useful feature matrix. These new feature matrices were then used to fit the regressor.



## Results

Interested in what makes a good title, I used the training data to find the largest tag count discrepencies between the popular and unpopular videos. 

My initial impressions were that adjectives would be common in popular videos, as descriptive titles are more eye-catching.
This was not the case. Most tags (including adjectives) were fairly evenly distributed among both sides, but there were some standouts.

**Wh-adverbs** were more common in the heavily viewed videos. 
> Wh-adverb: "how", "when", "where", "why"

This is neat as it shows that titles that **answer a question** or **are a question themselves** garner attention, such as *"Why I eat eggs"*, or *"How does a tortoise live so long?"*

Strangely enough, **verbs** (both present and past-tense) seemed to make more appearances in the least-viewed video titles.

A **determiner** followed by a **noun** appeared more frequently in the successful videos, while a **noun** followed by another **noun** was much more common in the unpopular videos. In fact, a noun followed by another noun appeared **70 more times** in the 200 worst videos than they did in the 200 best videos.

> Determiner: "the", "these", "a"

While having two nouns back-to-back isn't going to ruin your video, having certain tag sequences gives insight into what kind of content a user can expect to see. 

![alt text](https://github.com/nalimuradov/Video-View-Predictor/blob/master/images/img2.png "Successful videos")
> Above are some videos that had major success in terms of views. Note the similarities in their title structure.

While good titles and thumbnails can bump up the view count, they will not single-handedly be responsible for the success of a video. The **quality of the content** will be the main driving force and no title or thumbnail can save an awful video.

Feel free to use my [regressor](https://nariman.herokuapp.com/) to see how your **title** and **thumbnail** compare to the ones I trained on!

