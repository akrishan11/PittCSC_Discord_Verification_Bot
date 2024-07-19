import requests
import json 


VERIFY_URL_HEADER = ""
COOKIES = {'cookie': "-7867-65ab4c4f2c27; _ga_TWWN6KT393=GS1.2.1697387528.1.0.1697387528.0.0.0; _ga_53H0RJTF2X=GS1.1.1704999044.1.0.170AWS4999047.0.0.0; _ga_8HF75KJQHS=GS1.1.1706314849.1.0.1706314851.0.0.0; _ga_6RBM1FGDX8=GS1.1.1707423968.1.1.1707424593.0.0.0; _ga_FPS1F8F9PR=GS1.1.1707423969.1.1.1707424593.0.0.0; _ga_Y34E181K1E=GS1.1.1707864836.1.1.1707864902.0.0.0; _ga_XVZWT6FBB2=GS1.1.1711598488.1.1.1711598500.0.0.0; _ga_7KC19YJDHR=GS1.2.1711728050.1.0.1711728050.0.0.0; _ga_PKTKBFL5ZC=GS1.1.1711728050.1.0.1711728052.0.0.0; _ga_25RBN1QV6D=GS1.2.1712203213.3.0.1712203213.0.0.0; _ga_PMP6DZHDPB=GS1.2.1712270584.4.1.1712270615.0.0.0; _ga_BF1YESD0CP=GS1.1.1712459163.11.0.1712459167.0.0.0; _hp2_props.3001039959=%7B%22Base.appName%22%3A%22Canvas%22%7D; _ga_D2R7656T15=GS1.1.1712856818.2.0.1712856818.0.0.0; _hp2_id.3001039959=%7B%22userId%22%3A%228107539944649471%22%2C%22pageviewId%22%3A%22372770867858475%22%2C%22sessionId%22%3A%221637017421943310%22%2C%22identity%22%3A%22uu-2-ad9f547186183c9f12ec1ebc39357b38c1f83d30bad747a7943364c473ca9ea3-NwCkvNlRYfYOZfciI9p2znXFlWRUePHoMbCOxCA7%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _ga_Z1C4805JCV=GS1.1.1714079693.3.1.1714079709.0.0.0; _ga_PWZXV5W5DQ=GS1.1.1714082021.2.0.1714082021.0.0.0; _ga_3KY3YLN0S9=GS1.1.1714330567.2.0.1714330570.0.0.0; _ga_DYX3DC5HN2=GS1.1.1714346263.1.0.1714346271.0.0.0; _ga_M3PWYZFKTE=GS1.1.1714360938.2.0.1714360938.0.0.0; _ga_RR065MX47S=GS1.1.1714586988.11.0.1714586988.0.0.0; _ga_NHFDE734EE=GS1.1.1714586988.10.0.1714586988.0.0.0; _ga_437RLT24PZ=GS1.1.1714697658.2.0.1714697658.0.0.0; _ga_L4THKKBHVL=GS1.1.1714846378.10.0.1714846378.0.0.0; _ga_E1MBXYS34N=GS1.1.1716480033.3.0.1716480033.0.0.0; _ga_09VY67WNY2=GS1.1.1716765816.17.0.1716765816.0.0.0; _ga_WSJN4XLMZB=GS1.2.1716842380.69.1.1716842382.0.0.0; _ga_8ZBR9LY5WQ=GS1.1.1717352999.6.1.1717353006.0.0.0; _ga_LV9ZN08C21=GS1.2.1718146887.2.0.1718146887.0.0.0; _ga=GA1.1.1677538969.1693706987; _ga_PZQFKP0Y8Y=GS1.1.1718146782.12.1.1718148599.0.0.0; _ga_FD7D01SDGC=GS1.1.1718146816.3.1.1718148614.0.0.0; CG.SessionID=ignhvhygkcby2mtlxr4a4fye-8e28%2fSIQGeDoz8Ba3P0V7S8fKLM%3d;"}

def verify_member(name, email):

    verified = False

    SEARCH_URL = f"https://experience.pitt.edu/mobile_ws/v17/mobile_group_page_members?range=0&limit=10&order=&search_word={name}&param=35612&1721357427716" 

    print(SEARCH_URL)

    search_response = (requests.get(SEARCH_URL, cookies=COOKIES)).json()

    print(search_response)

    for result in search_response:
        response_name = (result['p0']+ " " + result["p1"]).lower()
        print(response_name)
        response_email = result['p9'].lower()
        if name == response_name and email == response_email:
            verified = True
            break
    
    print(verified)
    return verified


