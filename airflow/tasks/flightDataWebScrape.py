import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from pipelineActions import *


#This file will scrape data from planecrashinfo.com to a csv file, then upload csv file into S3 as bronze data
infoList = [] #List contain that will be contain dic of data 
def main():
    url = "https://www.planecrashinfo.com/"
    end = ".htm"
    s = "/"
    
    #get date from the all the yearly tables
    for year in (range(1920,2024+1)):
        try: 
            r = requests.get(url + str(year) + s + str(year) + end)
            sleep(2)
            soup = BeautifulSoup(r.content, 'html.parser')
            rows = soup.select("table tr")
            if rows == [] : raise Exception("Error fetching" + str(year) + "'s data")
            else: print(str(year) + " data accessed")
        except requests.ConnectionError as e:
            raise SystemExit(e)
            print("Error accessing page")
       
        
        
        #follow each link to access detailed data of each accident
        for i in range(1,len(rows)):
            row = rows[i]
            date = row.select_one('td').text.strip()
            end2 = row.select_one('td a')['href']

            #access each link in the row for detail information
            r = requests.get(url + str(year) + s + end2)
            sleep(2)
            soup2 = BeautifulSoup(r.content, 'html.parser')
            trs = soup2.select("table tr")
            
            #take data and rough format for JSON
            d = dict()
            for j in range(1,len(trs)):
                info = trs[j].get_text(strip=True).partition(":")[2].partition("(")[0].strip(" ")
                match j:
                    case 1:
                        d["date"] = info
                    case 2:
                        d["time"] = info
                    case 3:
                        d["location"] = info
                    case 4:
                        d["operator"] = info
                    case 5:
                        d["flight"] = info
                    case 6:
                        d["route"] = info
                    case 7:
                        d["aircraft"] = info
                    case 8:
                        d["registration"] = info
                    case 9:
                        d["cnln"] = info
                    case 10:
                        d["aboard"] = info
                    case 11:
                        d["fatalities"] = info
                    case 12:
                        d["ground"] = info
                    case 13:
                        d["summary"] = info
            if d  : infoList.append(d)
            else: print("fetched empty data in" + str(year))
            #print(len(infoList))

            sleep(1)


def loadCSV():
    headers = infoList[0].keys()
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header (column names)
        writer.writeheader()
        # Write the data rows
        writer.writerows(infoList)



main()  
saveToS3(infoList, 'bronze.csv')









