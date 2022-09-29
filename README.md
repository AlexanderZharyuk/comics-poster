# COMICS POSTER

Script for downloading a random comic from the site [XKCD](https://xkcd.com/) and posting it to [VK](https://vk.com/) group.

## Setting up your development environment
1. Install the required libraries:

To do this, use the command:
```shell
pip install -r requirements.txt
```
2. Set up `.env` -file:

Inside this file there should be variables with your secret data from the VK API:
```
VK_ACCESS_TOKEN=<YOUR-VK-ACCESS-TOKEN>
GROUP_ID=<YOUR-GROUP-ID>
```

Useful links:
1. To get [Access Token VK](https://vk.com/dev/implicit_flow_user)
2. To get [VK GROUP ID](https://regvk.com/id/)

## Beginning of work
After you have set your environment variables, run the script with the following command:
```shell
python3 main.py
```
If no errors appear in the console, then the post with the comment is already in your public in VK, rather, look at it and like it!

## Created with
* [VK API](https://vk.com/) - Social network
* [XKCD](https://xkcd.com/) - Comic site

## Author
[Alexander Zharyuk](https://github.com/AlexanderZharyuk/)
