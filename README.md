# Schools

Writing the installation instructions I realize that this probably won't work. You might just need to download
the source and then try to figure it out, but I can help if you have questions

## Installation

I'd recommend doing going the [homebrew](https://brew.sh/) route here, which is a installation tool for mac.
There are instructions on the website for downloading it.

1.
```
brew install python3 && sudo pip install virtualenv
```

2.
```
git clone git@github.com:neilfulwiler/schools
```

3.
```
cd schools && virtualenv --python=$(which python3) .
```

4.
```
source bin/activate
```

5.
```
pip install -r requirements.txt
```

6.
```
python main.py
```
