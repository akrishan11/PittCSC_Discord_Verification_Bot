import os
import webbrowser
import discord
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
from dotenv import load_dotenv, set_key
import requests
import time

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
VERIFIED_ROLE_ID = os.getenv("VERIFIED_ROLE_ID")
SERVER_ID = os.getenv("SERVER_ID")
SEARCH_URL_TEMPLATE = "https://experience.pitt.edu/mobile_ws/v17/mobile_group_page_members?range=0&limit=10&order=&search_word={name}&param=35612&1721357427716"
SIGN_ON_URL = "https://experience.pitt.edu/login_only?redirect=%2fweb_app%3fid%3d24043%26menu_id%3d59203%26if%3d0%26"

cg_session_id = os.getenv("CG_SESSION_ID")
if cg_session_id == "" or cg_session_id == None:
    print("Log in > right-click > Inspect > Application > Cookies> Copy CG.SessionID")
    time.sleep(4)
    webbrowser.open(SIGN_ON_URL)
    session_id = input("CG.SessionID: ")
    set_key(".env", "CG_SESSION_ID", session_id)
    cg_session_id = session_id
COOKIES = {"CG.SessionID": cg_session_id}


async def validate_member(name, email) -> bool:
    search_url = SEARCH_URL_TEMPLATE.format(name=name)

    while True:
        try:
            search_response = (requests.get(search_url, cookies=COOKIES)).json()
            for result in search_response:
                response_name = (result["p0"] + " " + result["p1"]).lower()
                response_email = result["p9"].lower()
                if name.lower() == response_name and email.lower() == response_email:
                    return True
            return False
        except HttpError as err:
            print(err)


async def get_creds() -> Credentials:
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


async def get_sheet() -> dict[any, any]:
    creds = await get_creds()
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A2:J").execute()
        )
        return result

    except HttpError as err:
        print(err)


async def write_to_sheet(values: list[str], range: str) -> dict[any, any]:
    creds = await get_creds()
    try:
        gspread.authorize(creds)
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        body = {"values": values}

        result_write = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=range,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        return result_write
    except HttpError as err:
        print(err)


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    result = await get_sheet()

    validated_values = []
    verified_values = []

    guild = client.get_guild(SERVER_ID)
    if guild == None:
        raise Exception("Guild not found")

    role = guild.get_role(VERIFIED_ROLE_ID)
    if role == None:
        raise Exception("Guild not found")

    for row in result["values"]:
        name = row[1]
        email = row[3]
        username = row[4]
        is_verified = row[8]
        is_validated = row[9]

        if row[0] != "":
            if is_verified == "TRUE":
                validated_values.append(["TRUE"])
                verified_values.append(["TRUE"])
            else:
                if is_validated == "TRUE" or await validate_member(name, email):
                    validated_values.append(["TRUE"])
                    member = guild.get_member_named(username)
                    if member != None and member.name == username:
                        await member.add_roles(role)
                        verified_values.append(["TRUE"])
                    else:
                        verified_values.append(["FALSE"])
                else:
                    validated_values.append(["FALSE"])
                    verified_values.append(["FALSE"])
    await write_to_sheet(validated_values, "J2:J")
    await write_to_sheet(verified_values, "I2:I")
    print("Verification Complete!")


load_dotenv()
client.run(os.getenv("DISCORD_BOT_TOKEN"))
