from textwrap import dedent


def main():
    with open("output.txt", 'r') as f:
        raw = f.read().split()
        numer, denom = int(raw[0]), int(raw[1])

    if denom == 0:
        print("You haven't yet run the Emotion Detector!")
        return

    p = round((numer/denom)*100, 2)
    print(dedent(f"""\

        ============= OFFICIAL CORNELL UNIVERSITY HAPPINESS APTITUDE TEST =============

        While the Emotion Detector was monitoring your feelings, you were {p}% happy.

        =============== THE GHOST OF EZRA CORNELL HOPES YOU'RE DOING OK ===============
        """))


if __name__ == "__main__":
    main()
