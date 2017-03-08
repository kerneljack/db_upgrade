#!/usr/bin/python

import re
import glob
import os
import MySQLdb
import traceback

def getDBConnection():
  return MySQLdb.connect(host='localhost', user='root', passwd='', db='test')

def findMaxVersion():
  d = {}
  maxVersion = 0

  # read all file names, create a dict of 'num', 'filename'
  p = re.compile('\d+')
  os.chdir('scripts')
  for f in glob.glob("*.sql"):
    m = p.match(f)
    if m:
      version = m.group()
      d[version] = f
      if version > maxVersion:
        maxVersion = version
    else:
      print ('No match!')

  return d, maxVersion

def findCurrentDBVersion():
  try:
    db = getDBConnection()
    cur = db.cursor()
    cur.execute("SELECT version from version")
    for row in cur.fetchall():
      currentVersion = row[0]

    db.close() 
  except (MySQLdb.Error) as e:
    print (e)

  return currentVersion


def applyUpgrade(d, upgradeList):
  print ('Upgrades to be applied: ')
  print(upgradeList)

  db = getDBConnection()

  for i in upgradeList:
    fileName = d[i]
    with open (fileName, "r") as myfile:
      sql = myfile.readlines()
      myfile.close()

      print ('\nApplying upgrade ' + fileName + ': ')
      for line in sql:
        print(line.strip())

        cursor = db.cursor()
        try:
          cursor.execute(line)
          db.commit()
        except (MySQLdb.Error) as e:
          db.rollback()
          db.close()
          print(e)
          return None
      
  db.close()


def updateDBVersion(maxVersion):
  print('Updating DB Version to: ' + maxVersion)

  db = getDBConnection()
  sql = "UPDATE version SET version = '" + maxVersion + "'"

  cursor = db.cursor()
  try:
    cursor.execute(sql)
    db.commit()
  except (MySQLdb.Error) as e:
    db.rollback()
    db.close()
    print(e)
    return None
      
  db.close()


def main():

  # find the Max version and the Current version
  d, maxVersion = findMaxVersion()
  print('Max version: ' + maxVersion)

  currentVersion = findCurrentDBVersion()
  print ('Current version: ' + currentVersion)

  # if there are upgrades to be applied
  if currentVersion < maxVersion:
    list = d.keys()
    list.sort()

    # create a list of numbers which refers ONLY to the files
    # that we are going to use in the upgrade
    upgradeList = []
    for i in list:
      if i > currentVersion:
        upgradeList.append(i)
        
    # call the applyUpgrade function with our list of 
    # file numbers that we are going to use
    applyUpgrade (d, upgradeList)

    # update our DB with the latest version
    updateDBVersion(maxVersion)

  # if there are NO upgrades to be applied, we end here
  elif currentVersion == maxVersion:
    print('We are up to date! NO upgrades required!')
  
    
if __name__ == "__main__":
  try:
    main()
  except:
    traceback.print_exc()


