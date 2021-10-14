#!/usr/bin/env python3

from query import Query
from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json


def main():
    if not os.path.exists("model"):
        print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
        exit (1)

    wf = wave.open(sys.argv[1], "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    # You can also specify the possible word list
    words = "yesterday today tomorrow last next monday tuesday wednesday thursday friday saturday sunday "
    
    warm_clothing = [
        "sweater",
        "jacket",
        "coat",
        "hoodie",
        "cardigan",
        "overcoat",
    ]

    for word in warm_clothing:
        words += f"{word} "

    forecasts = [
        "sun",
        "sunny",
        "rainy",
        "raining",
        "rain",
        "showers",
        "showering",
        "pouring",
        "storming",
        "storms",
        "storm",
        "thunderstorm",
        "thunderstorming",
        "lightning",
        "thunder",
        "cloudy",
        "clouds",
        "overcast",
        "grey",
        "gray",
        "snowy",
        "snowing",
        "snow",
        "hail",
        "hailing",
        "windy",
        "gusty",
        "humid",
        "humidity",
    ]

    for word in forecasts:
        words += f"{word} "
    
    rec = KaldiRecognizer(model, wf.getframerate(), words + "[unk]")

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        """
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
        """

    rec_dict = json.loads(rec.FinalResult())
    
    print("RECEIVED TEXT:")
    print(rec_dict["text"] + "\n")

    Q = Query()
    Q.process_query(rec_dict["text"])


if __name__ == "__main__":
    main()
