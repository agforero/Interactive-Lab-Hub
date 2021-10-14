# Chatterboxes
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

Bonus Activity:

If you are really excited about Speech to Text, you can try out [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) and [voice2json](http://voice2json.org/install.html)
There is an included [dspeech](./dspeech) demo  on the Pi. If you're interested in trying it out, we suggest you create a seperarate virutal environment for it . Create a new Python virtual environment by typing the following commands.

```
pi@ixe00:~ $ virtualenv dspeechexercise
pi@ixe00:~ $ source dspeechexercise/bin/activate
(dspeechexercise) pi@ixe00:~ $ 
```

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

![fig1](l3p1_storyboard.png)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

The idea was that the user would follow a specific dialogue tree when asking about the weather. <mark>Highlighted</mark> words signify specific terms the speech to text algorithm would look for. As you can tell from the arrows, some commands would naturally lead to others, e.g.:

> What is the <mark>weather</mark> <mark>today?</mark>

> In New York City, it's currently 75 degrees and sunny. You can expect a high of 79 degrees and a low of 68 degrees.

At this point, they might extend the original question with a specific hour. Let's take the above example, only expanding it out a bit:

> What is the <mark>weather</mark> <mark>today</mark> at <mark>4PM</mark>?

> At 4PM, you can expect a sunny forecast without clouds. It will be 77 degrees, with a high of 79 degrees and a low of 72 degrees.

I naturally supposed that they would *then* ask a question about if they needed a sweater/jacket/coat. Something like:

> Will I need a <mark>jacket</mark> today?

> No.

When you scroll down to the video demo, though, you see how dialogue wasn't inherently a tree. There were some holes in my plan.

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

### [Here is a link](https://youtu.be/caF24ku7pfs) to the video demo! 🎬

There are a few commands that my friend gives that WeatherBot 9000 is incapable of answering. Here's a table showing what worked/didn't work:

| Command | Did it work? | Notes |
| ------- | ------------ | ----------- |
| WeatherBot, please tell me the temperature. | Yes | In the video demo, this works, but only because I assume that WeatherBot would impose "today" as the chosen time if no other time is given. In reality, the decision tree would not catch this, since he never specifies a time. |
| WeatherBot, will I need an umbrella tomorrow? | No | "Umbrella" is not a key term. There is also no explicit mention of the word "weather".|
| WeatherBot, is it sunny? | No | He leads by asking to confirm the forecast, instead of asking about it. The implication is something along the lines of, "Is the weather today sunny?" The question leaves out some key terms, so WeatherBot gets confused. |
| WeatherBot, what's the weather going to be tomorrow? | Yes | This is exactly the kind of question I planned for. |
| WeatherBot, is it going to rain tomorrow? | No | Again, no explicit mention of "weather" or "temperature". The Bot still doesn't know how to confirm or deny a forecast, instead of just telling someone what the forecast will be. |
| Will I need a sweater tomorrow? | Yes | This is also (weirdly enough) exactly the kind of question I planned for. If anything, it's because I always wished I could ask my Amazon Echo if I'll need a sweater, and have it give me an explicit "yes", "no" or something else. |
| Thanks! | No | I didn't plan that the user would be so cordial. I know the Echo thanks people if people thank it, so maybe I could do the same. |

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

The device needs to be a lot more adaptive to what people say. The queries can't be terribly sequential in nature; the ability to read one word shouldn't hinge on having previously read a word before. The user should be able to ask about a wide range of days in the past, present and future, and use different words commonly attributed to these days ("yesterday", "tomorrow", "next Tuesday", etc.).

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

It could use a light to communicate that queries were read in successfully, or that it is currently talking.

3. Make a new storyboard, diagram and/or script based on these reflections.

![IMG_4155](https://user-images.githubusercontent.com/55858146/137249106-9fadac80-ff8b-4fba-baab-79dd65eed22b.png)

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

The program works on a multi-step process:

1. User asks a question about New York City weather.

    a. If not relying on the speech-to-text algorithm, the wizard manually types the user's query as a command-line argument.

2. The query is parsed, and key words are digested to understand the nature of the question: what day is being asked about, if the question concerns forecast, if the user is asking if they should wear warm clothes, etc. \*

3. Depending on the nature of the question, WeatherBot prepares 4 distinct answers to address what the user said.

4. The output of this script is piped into `festival`, which relays the output as audio.

\* In order to get the data for the selected day, the program uses `requests` and `BeautifulSoup` to scrape [timeanddate.com](https://www.timeanddate.com/weather/usa/new-york/hourly).

As a command, the wizard executes (the quotes are important):

```bash
./weatherbot_working.sh "what will the weather be next tuesday"
```

The wizard can also execute the following command, which relies entirely on the VOSK speech-to-text API. The user just says their query in the 10 seconds allocated by the command. However, the microphone doesn't seem to fare well with picking up precise audio, and commands are usually either ignored or misinterpreted. Regardless, with a powerful microphone, the following command would work:

```bash
./weatherbot.sh
```

*Some constraints:*

The user can't ask about:

* Specific times

* Locations other than NYC

*Include videos or screencaptures of both the system and the controller.*

[Self Demo 1](https://youtu.be/kvi033h-6MA)

[Self Demo 2](https://youtu.be/V7a0g7tAGvQ)

[Self Demo 3](https://youtu.be/D_3NkHj-d_M)

[User Demo 1](https://youtu.be/rQsuBOtj9OE)

[User Demo 2](https://youtu.be/GurQBqxkCg4)

## Test the system

Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

It was able to very intelligently understand what day the user was talking about. The user can say any range of "last Tuesday" or "tomorrow" or "next Wednesday" and it can find weather data for these respective days, without using an API call. It's also pretty smart with understanding different variations of questions the user can ask: sometimes the user is asking about a specific forecast, or whether to wear warm clothing, or if it's going to rain, and WeatherBot can address all of these concerns.

My second user asked some questions that WeatherBot didn't know how to answer. For example, "What is the coldest place on Earth today?" is not within WeatherBot's repertoire. The second user also noticed I was typing something, but incorrectly guessed that I was typing out WeatherBot's response.

Both users found the `festival` voice funny, which, honestly, might not even be a bad thing.

### What worked well about the controller and what didn't?

`./weatherbot_working.sh "what will the weather be like next tuesday"` is not a very hard command to understand and execute. The wizard behind the curtain here is my act of transcribing what the user is saying as they say it, so that the program doesn't have to rely on the accuracy of the microphone and speech-to-text algorithm. `./weatherbot.sh` does actually try to use the mic, but the `_working` variation is a nice way to use the wizard to ensure accuracy. 

The downside is that typing out the entirety of what the user says might be tedious or difficult, and it isn't exactly subtle, either.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

If the system instead used a crisp microphone and powerful speech-to-text algorithm, it could be entirely independent of the wizard. The rest of the code is the same -- the only thing that changes is how it gets its input. Something I learned is to separate out these two. The means by which input is acquired should be independent of how the program actually processes these queries, so you can develop the logic of the program independent of any hardware or speech-detection issues.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

Over time, the model could adjust to the user's voice and more easily understand their queries. In addition, if given a sufficient control over grammar, it could creatively come up with responses without relying on hardset logic to deliver responses. Other than speech, though, the only other sensor I could think to add would be a button to start a query.
