# data_generator
It is a simple random data generator to csv written in python.

You set table's the attributes in a xml config file and the data_generator generates the data this table.

# Download
Just clone this git repository: git clone `https://github.com/gerley/data_generator.git`

# Example
Set the config file as follow:

config.xml:
```xml
<xml>
    <table name="table_name" records="20">
        <field name="field_auto_increment" type="auto_increment" min_val="1"/>
        <field name="field_integer" type="integer" min_val="1" max_val="100"/>
        <field name="field_varchar" type="varchar" min_len="10" max_len="30"/>
        <field name="field_float" type="float" min_val="1" max_val="100"/>
        <field name="field_bool" type="bool"/>
        <field name="field_select_int" type="select" type_value="integer">
            <option value="10"/>
            <option value="20"/>
            <option value="30"/>
        </field>
        <field name="field_select_varchar" type="select" type_value="varchar">
            <option value="value1"/>
            <option value="value2"/>
            <option value="value3"/>
        </field>
        <field name="field_fixed_varchar" type="fixed" type_value="varchar" value="fixed_value"/>
        <field name="field_fixed_int" type="fixed" type_value="integer" value="10"/>
        <field name="field_date" type="date" format="%Y-%m-%d %H:%M" min_val="2010-01-01 00:00" max_val="2015-01-01 23:59"/>
    </table>
</xml>
```

Execute this script:
```bash
python data_generator.py -o .
```

It were generating the table_name.csv file with twenty registers as follow.

table_name.csv:
```csv
field_auto_increment,field_integer,field_varchar,field_float,field_bool,field_select_int,field_select_varchar,field_fixed_varchar,field_fixed_int,field_date
1,97,UulsfCNtsQkQNJ,35.190089978167904,False,30,value2,fixed_value,10,2011-08-19 16:36
2,18,XuMuHjvInSdBfRRdBcFlvlAnuzgm,50.27090570360126,False,10,value1,fixed_value,10,2014-02-17 08:54
3,30,qCzzttPSfStFkikStlMjlm,94.35012169362565,False,20,value1,fixed_value,10,2012-08-30 20:08
4,7,XjfCrdTMUoREkBS,45.109387602690205,False,30,value1,fixed_value,10,2010-02-25 22:27
5,6,fSDVitQdvmIPQKbocpNjzH,4.105064993337037,True,10,value1,fixed_value,10,2013-12-02 18:33
6,82,dcNhisBVjpJubgQdRuGHvsBOvRPD,46.433332178143885,False,10,value3,fixed_value,10,2011-05-30 15:41
7,64,tAidzLNuUbBJMcGNBkSNJGiFzOMeJH,53.04148541019803,True,20,value2,fixed_value,10,2014-07-28 08:48
8,23,UHMefgqCRV,85.33298374313043,True,10,value2,fixed_value,10,2010-04-23 03:53
9,85,MJMNstRoesHRZXtHkoVraPEskpf,9.438720516758853,True,30,value3,fixed_value,10,2010-05-20 20:27
10,48,pUvakaqgVJPugBOANKQOeJ,91.66513218379174,True,30,value1,fixed_value,10,2014-11-02 13:10
11,97,xxMlmbOKHdPQmiaKhPRoLoJpxlbi,14.558638488933868,True,20,value2,fixed_value,10,2014-04-15 12:41
12,94,UFpBGNABaIRbgQuVDiTCLE,11.001550200653439,True,30,value2,fixed_value,10,2011-10-18 09:16
13,71,ATickfqqsXAL,23.34430029060044,False,20,value1,fixed_value,10,2013-03-07 07:34
14,89,KsgRClsZbogSZKlsLQ,33.15687552615437,False,10,value3,fixed_value,10,2013-09-06 22:28
15,94,xVRPZhfzDNgoZPjfom,99.02417998473732,True,20,value1,fixed_value,10,2011-06-30 17:32
16,65,rqaQSEeZQiIKcqDTeMTV,31.462926639054817,False,10,value1,fixed_value,10,2011-12-15 01:27
17,14,mrLdMJjRKpNFfDAhoSq,21.439629297771504,True,20,value3,fixed_value,10,2013-09-29 15:41
18,4,RqAegmGzcuTvxBznxrqdvBLqLMBPQ,19.742439869400098,True,30,value2,fixed_value,10,2010-07-22 18:20
19,5,DKufgJQshrvHUMNVxlFpaMb,89.51408648943622,True,20,value3,fixed_value,10,2011-10-08 17:45
20,97,zBVZsdgERUhAiMRJRpsdJhoGo,98.42960829849486,True,10,value1,fixed_value,10,2010-01-06 18:53
```
