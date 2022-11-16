import pytest
from scrapperHelper import videoScrapper

class TestvideoScrapper:

    def testUrlGoogle(self):
        url = "https://www.google.com/"
        with pytest.raises(Exception, match="Not youtube url"):
            scrapper = videoScrapper(url)

    def testUndefineVid(self):
        url = "https://www.youtube.com/watch?v=kldjfmqlksf"
        with pytest.raises(Exception, match="undefine video"):
            scrapper = videoScrapper(url)


    def testTitle(self):
        url = "https://www.youtube.com/watch?v=6gjsAA_5Agk"
        scrapper = videoScrapper(url)
        assert (scrapper._getTitle() == "Can you beat Pokemon FireRed while blind and deaf?") is True

    def testChannelName(self):
        url = "https://www.youtube.com/watch?v=6gjsAA_5Agk"
        scrapper = videoScrapper(url)
        assert (scrapper._getChannelName() == "MartSnack") is True

    def testGetNumLike(self):
        url = "https://www.youtube.com/watch?v=zfMhwHzS8J4"
        scrapper = videoScrapper(url)
        assert (scrapper._getNumLikes() == 1) is True

    def testGetDescription(self):
        url = "https://www.youtube.com/watch?v=zfMhwHzS8J4"
        scrapper = videoScrapper(url)
        assert (scrapper._getDescription() == "Test de mon avion \u00e0 d\u00e9collage horizontal et vertical, avec le \\\"nouveaux\\\" dlc breaking ground expansion") is True


    def testGetLinksNoLinks(self):
        url = "https://www.youtube.com/watch?v=zfMhwHzS8J4"
        scrapper = videoScrapper(url)
        links = scrapper._getLinks(str(scrapper._getDescription())) 
        assert (len(links["Links"]) == 0) is True
        assert (len(links["Timestamps"]) == 0) is True

    def testGetLinks(self):
        url = "https://www.youtube.com/watch?v=6gjsAA_5Agk"
        scrapper = videoScrapper(url)
        links = scrapper._getLinks(str(scrapper._getDescription()))
        assert (len(links["Links"]) == 14) is True
        assert (len(links["Timestamps"]) == 5) is True

    def testGetComments(self):
        url = "https://www.youtube.com/watch?v=6gjsAA_5Agk"
        scrapper = videoScrapper(url)
        comments = scrapper._getComents(10)
        assert (len(comments) == 10) is True