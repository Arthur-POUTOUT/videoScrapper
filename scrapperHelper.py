from bs4 import BeautifulSoup
import requests
import re
import json
from itertools import islice

from youtube_comment_downloader import *


class videoScrapper:
    """
    Class using BeautifulSoup to scrap a yt video
    get its title, channel name, number of likes, description and list of links and timestamps in the decription
    """
    def __init__(self, link : str):
        """
        Parameters : 
        ------------------------
        link : url of the video to be scrap
        """
        # start url
        if not link.startswith("https://www.youtube.com/watch?v="):
            raise Exception("Not youtube url")
        response = requests.get(link)
        self.html = BeautifulSoup(response.text, 'html.parser')

        if self.html.find("meta", itemprop="name") is None:
            raise Exception("undefine video")

    def _getTitle(self) -> str:
        """
        Get the title of the video

        Return :
        ------------------------
        The title of the video
        """
        return str(self.html.find("meta", itemprop="name")['content'])


    def _getChannelName(self) -> str:
        """
        Get the name of the channel of the video creator

        Return :
        ------------------------
        The name of the channel name
        """
        return str(self.html.find("span", itemprop="author").next.next['content'])

    def _getNumLikes(self) -> int:
        """
        Get the number of likes of the video

        Return :
        ------------------------
        The number of likes of the video
        
        """
        data = re.search(r"var ytInitialData = ({.*?});", self.html.prettify()).group(1)
        data = json.loads(data)
        videoPrimaryInfoRenderer = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
        likes = int(re.sub("[^0-9]", "", likes_label))
        return int(likes)
    
    def _getDescription(self) -> str:
        """
        Get the decription of the video

        Return :
        ------------------------
        The description of the video
        """
        pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
        description = pattern.findall(str(self.html))[0].replace('\\n','\n')
        return str(description)

    def _getLinks(self, description : str) -> dict:
        """
        Get the links of the decription of the video

        Parameters : 
        ------------------------
        description : the description of the video (get from _getDescription())
        Return :
        ------------------------
        The links of the description of the video
        """
        links = re.findall(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", description)
        timestamps = re.findall(r"[0-9]+:[0-9]{2}", description)
        return {"Links": links, "Timestamps": timestamps}

    def _getComents(self, num):
        listComments = []
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url('https://www.youtube.com/watch?v=ScMzIvxBSi4', sort_by=SORT_BY_POPULAR)
        for comment in islice(comments, num):
            listComments.append(comment)
        return listComments

    def getData(self, numComments) -> dict:
        """
        Call the differents get function and put the result into a dict

        Parameters : 
        ------------------------
        numComments : number of comments to return
        Return :
        ------------------------
        The dict of the value wanted
        """
        dict = {}
        dict["Title"] = self._getTitle()
        dict["ChannelName"] = self._getChannelName()
        dict["NumberLikes"] = self._getNumLikes()
        dict["Description"] = self._getDescription()
        dict["DescriptionLinks"] = self._getLinks(dict["Description"])
        dict["Comments"] = self._getComents(numComments)

        return dict