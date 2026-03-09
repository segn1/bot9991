
import instaloader

def download_story(username):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    L.download_stories(userids=[profile.userid])
