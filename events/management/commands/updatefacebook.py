from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import facebook
from datetime import datetime
from django.core.cache import cache
from fragmentet.settings import TOP_FOLDER



def get_wall_posts():
    f = open( TOP_FOLDER + '/events/facebook_token.txt', 'r+')
    access_token = f.read()[:-1]
    graph = facebook.GraphAPI(access_token)
    posts = graph.request("126467437553756", {"fields":"posts.limit(4).fields(type,status_type,story,message,link,caption,created_time)", "locale":"da_DK"})
    data = posts["posts"]["data"]
    # Convert dates to struct_time objects
    for post in data:
        post["created_time"] = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
    return data

class Command(NoArgsCommand):

    help = 'Updates the facebook wall feed in the cache.'
    def handle_noargs(self, **options):
        try:
            posts = get_wall_posts()
            if posts:
                cache.set('facebook_data', posts)
            self.stdout.write('facebook data updated.\n')
        except Exception as e:
           self.stdout.write("FBError: "+ str(e) + '\n')
