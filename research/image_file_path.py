'''
How to generate directory path for image

format: user_{id}/avatar/{year}/{month}/{date}/filename
'''

def user_avatar_directory_path(instance, filename):
    from time import gmtime, strftime
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    date_path = strftime("%Y/%m/%d", gmtime())
    return "user_{0}/avatar/{1}/{2}".format(instance, date_path, filename)

print(user_avatar_directory_path('1', 'avatar.jpg'))