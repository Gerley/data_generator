#!/usr/bin/env python


################################################################################
# The MIT License (MIT)
#
# Copyright (c) 2015 Gerley Machado
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################


import argparse
import csv
import os
import random
import sys
import time
from xml.dom import minidom


VERSION = "0.1.0"


class ReaderConfig:
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def execute(self):
        tableList = []
        xmldoc = minidom.parse(self.inputFile)
        for tableDoc in xmldoc.getElementsByTagName('table'):
            tableList.append(self.getTable(tableDoc))
        return tableList

    def getTable(self, tableDoc):
        name = tableDoc.attributes['name'].value
        lenRecords = int(tableDoc.attributes['records'].value)
        fieldList = []
        for fieldDoc in tableDoc.getElementsByTagName('field'):
            fieldList.append(self.getField(fieldDoc))
        return {'name': name, 'lenRecords': lenRecords, 'fields': fieldList}

    def getField(self, fieldDoc):
        if fieldDoc.attributes['type'].value == 'auto_increment':
            return self.getAutoIncrementField(fieldDoc)
        elif fieldDoc.attributes['type'].value in ('integer', 'float'):
            return self.getNumericField(fieldDoc)
        elif fieldDoc.attributes['type'].value == 'varchar':
            return self.getVarCharField(fieldDoc)
        elif fieldDoc.attributes['type'].value == 'bool':
            return self.getBoolField(fieldDoc)
        elif fieldDoc.attributes['type'].value == 'fixed':
            return self.getFixedField(fieldDoc)
        elif fieldDoc.attributes['type'].value == 'date':
            return self.getDateField(fieldDoc)
        elif fieldDoc.attributes['type'].value == 'select':
            return self.getSelectField(fieldDoc)
        raise Exception('Invalid field name: ' + fieldDoc.attributes['type'].value)

    def getAutoIncrementField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        mininumValue = int(fieldDoc.attributes['min_val'].value)
        return {'name': name, 'mininumValue': mininumValue, 'type': 'auto_increment'}

    def getNumericField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        type = fieldDoc.attributes['type'].value
        mininumValue = int(fieldDoc.attributes['min_val'].value)
        maximunValue = int(fieldDoc.attributes['max_val'].value)
        return {'name': name, 'type': type, 'mininumValue': mininumValue, 'maximunValue': maximunValue}

    def getVarCharField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        mininumLen = int(fieldDoc.attributes['min_len'].value)
        maximunLen = int(fieldDoc.attributes['max_len'].value)
        return {'name': name, 'mininumLen': mininumLen, 'maximunLen': maximunLen, 'type': 'varchar'}

    def getBoolField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        return {'name': name, 'type': 'bool'}

    def getFixedField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        typeValue = fieldDoc.attributes['type_value'].value
        value = fieldDoc.attributes['value'].value
        return {'name': name, 'typeValue': typeValue, 'value': value, 'type': 'fixed'}

    def getDateField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        format = fieldDoc.attributes['format'].value
        mininumValue = fieldDoc.attributes['min_val'].value
        maximunValue = fieldDoc.attributes['max_val'].value
        return {'name': name, 'type': 'date', 'mininumValue': mininumValue, 'maximunValue': maximunValue, 'format': format}

    def getSelectField(self, fieldDoc):
        name = fieldDoc.attributes['name'].value
        typeValue = fieldDoc.attributes['type_value'].value
        options = map(lambda x: x.attributes['value'].value, fieldDoc.getElementsByTagName('option'))
        return {'name': name, 'typeValue': typeValue, 'options': options, 'type': 'select'}


class Generater:
    def __init__(self, tableList, outputPath):
        self.tableList = tableList
        self.outputPath = outputPath

    def execute(self):
        self.generaterFieldValue = GeneraterFieldValue()
        for table in self.tableList:
            self.generateFile(table)

    def generateFile(self, table):
        generaterCSV = GeneraterCSV(table, self.outputPath)
        for recordIndex in xrange(table['lenRecords']):
            generaterCSV.append(self.generateRegister(table, recordIndex))

    def generateRegister(self, table, recordIndex):
        register = []
        for field in table['fields']:
            register.append(self.generaterFieldValue.getValue(field, recordIndex))
        return register


class GeneraterFieldValue:
    def getValue(self, field, recordIndex):
        if field['type'] == 'auto_increment':
            return self.getAutoIncrementValue(field, recordIndex)
        elif field['type'] == 'integer':
            return self.getIntegerValue(field)
        elif field['type'] == 'float':
            return self.getFloatValue(field)
        elif field['type'] == 'varchar':
            return self.getVarcharValue(field)
        elif field['type'] == 'bool':
            return self.getBoolValue()
        elif field['type'] == 'fixed':
            return self.getFixedValue(field)
        elif field['type'] == 'date':
            return self.getDateValue(field)
        elif field['type'] == 'select':
            return self.getSelectValue(field)
        raise Exception('Invalid field name: ' + field['type'])

    def getAutoIncrementValue(self, field, recordIndex):
        return recordIndex + field['mininumValue']

    def getIntegerValue(self, field):
        return random.randint(field['mininumValue'], field['maximunValue'])

    def getFloatValue(self, field):
        return random.uniform(field['mininumValue'], field['maximunValue'])

    def getVarcharValue(self, field):
        length = self.getIntegerValue({'mininumValue': field['mininumLen'], 'maximunValue': field['maximunLen']})
        listChar = [random.choice('ABCDEFGHIJKLMNOPQRSTUVXZabcdefghijklmnopqrstuvxz') for i in xrange(length)]
        return ''.join(listChar)

    def getBoolValue(self):
        return random.choice([True, False])

    def getFixedValue(self, field):
        if(field['typeValue'] == 'varchar'):
            return field['value']
        return int(field['value'])

    def getDateValue(self, field):
        prop = random.random()
        stime = time.mktime(time.strptime(field['mininumValue'], field['format']))
        etime = time.mktime(time.strptime(field['maximunValue'], field['format']))
        ptime = stime + prop * (etime - stime)
        return time.strftime(field['format'], time.localtime(ptime))

    def getSelectValue(self, field):
        return random.choice(field['options'])


class GeneraterCSV:
    def __init__(self, table, outputPath):
        self.table = table
        self.outputPath = outputPath
        pathFile = os.path.join(outputPath, table['name'] + '.csv')
        self.file = csv.writer(open(pathFile, 'w'))
        listField = map(lambda x: x['name'], table['fields'])
        self.file.writerow(listField)

    def append(self, register):
        self.file.writerow(register)


def main(inputfile, outputpath):
    tableList = ReaderConfig(inputfile).execute()
    Generater(tableList, outputpath).execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("-i", "--ifile", dest="inputfile", default="config.xml", help="input config file")
    parser.add_argument("-o", "--opath", dest="outputpath", required=True, help="output path folder")
    parser.add_argument('-v', "--version", action="version", version="%(prog)s {0}".format(VERSION))
    options = parser.parse_args()
    main(options.inputfile, options.outputpath)
