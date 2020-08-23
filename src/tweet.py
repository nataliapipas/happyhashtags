class Tweet:
    def __init__(self, status):
        self.status = status
        self.text = self.get_text()
        self.hashtags = self.get_hashtags()
        self.created_at_hour = self.get_hour()

    def get_hour(self):
        """
        Truncates the minutes and seconds attributes from a datetime object.
        :param tweet_datetime: The datetime to be truncated
        :return:
        """
        return str(self.status.created_at)[:13] + ":00:00"

    def get_text(self):
        if hasattr(self.status, "extended_tweet"):
            text = self.status.extended_tweet["full_text"]
        else:
            text = self.status.text
        return text

    def get_hashtags(self):
        hashtags = [word for word in self.text.split() if word[0] == '#']
        return hashtags
