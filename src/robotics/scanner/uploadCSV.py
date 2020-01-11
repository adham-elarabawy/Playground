import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/adhamelarabawy/Documents/Work/Robotics/Attendance_Scanner-d87a14b3476f.json', scope)
gc = gspread.authorize(credentials)

# Read CSV file contents
content = open('input/newscans.csv', 'r').read()

gc.import_csv('1IW-zEbQpjJ4xDjcm_PdOr6QjNIQeZ4zISSgSNNAhlD8', content)
