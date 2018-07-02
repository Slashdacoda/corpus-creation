# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ElementTree
import sys
import os


class ssoarMetaFileFormatter:
    
    def __init__(self, rootDir, targetDir):
        self.rootDir = rootDir
        self.targetDir = targetDir
        self.counter = 0
        
    def formatMetadata(self):
        for filename in os.listdir(self.rootDir):
            #print " F: " + filename
            for recordId, recordMetadata in self.parseMetadata(os.path.join(self.rootDir, filename)):
                #print " Rid: " + recordId
                #print " 2F: " + filename
                self.writeToFile(recordId, recordMetadata)
    
    def getRootElements(self, root):
        return root
        
    def writeToFile(self, recordId, recordMetadata):
        towrite = ElementTree.ElementTree(recordMetadata)
        print " self.targetDir: " + self.targetDir
        print " recordId: " + recordId
        towrite.write(os.path.join(self.targetDir, recordId + ".xml"), "utf-8")
        self.counter += 1
        print "wrote %s (file no. %d)." %(os.path.join(self.targetDir, recordId + ".xml"), self.counter)
        
    def parseMetadata(self, filename):
        try:
            tree = ElementTree.parse(filename)
            root = tree.getroot()
            for element in root.getchildren():
                for attribute in element.getchildren():
                    if attribute.tag == "{http://www.openarchives.org/OAI/2.0/}record":
                        for part in attribute.getchildren():
                            if part.tag == "{http://www.openarchives.org/OAI/2.0/}metadata":
                                for dcElement in part.getchildren():
                                    for dcValue in dcElement.getchildren():
                                        if dcValue.get("qualifier") == "uri":
                                            if "handle" in dcValue.text:
                                                recordId = dcValue.text.replace("http://www.ssoar.info/ssoar/handle/document/", "")
                                                recordId = recordId.replace("https://www.ssoar.info/ssoar/handle/document/", "")
                                                yield recordId, attribute
        except Exception as ee:
            print "Caught error in filename " + filename
            print " E: " + str(ee)

def usage():
    print "usage: ssoarMetaFileFormatter.py <inputDir> <outputDir>"
        
if __name__=="__main__":
    try:
        inputDir = sys.argv[1]
        outputDir = sys.argv[2]
        formatter = ssoarMetaFileFormatter(inputDir, outputDir)
        formatter.formatMetadata()
    except Exception as e:
	usage()
	print " E: " + str(e)
    
