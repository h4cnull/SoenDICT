### 说明

SoenDICT 通过元素文件和模板文件来生成字典，可以设置元素的概率，生成带概率值的密码字典。元素文件定义了元素的名称和字段，模板定义相应元素的位置。如：
```text
#元素文件 json格式
{
    "name":["admin","Admin"],
    "char":["@","!"],
    "num":["123","123456"],
    "year":"years.txt"
}

#模板文件格式
name
name num
name char num
num char name
name year
```
如果元素是字符串，如上:years.txt，则该字符串为存放字段的文件路径，是元素文件的“相对路径”，所以years.txt和元素文件在同一目录下。
模板中的存放元素名称以“空格”分隔，示例模板会生成如下格式的口令：
```text
admin
...
Admin123
...
admin@123
...
123@admin
...
admin2022
```
### 用法
```text
-e,--element      指定元素文件
-t,--template     指定模板文件
```
通用模板如下
```text
name
name num
name char num
name num char
name str
name char str
str char name
name str char
str
str num
num str
str char num
str num char
char str num
name sfz
name char sfz
name sfz char
birth
name birth
birth name
name char birth
char name birth
name birth char
phone
name phone
qq
QQ qq

======================
name   姓名
num    数字
char   特殊字符
str    特殊字符串
sfz    身份证
birth  出生日期
phone  手机号码
qq     qq号码
QQ     与qq号码组合的字符串
通常来说 name num char str就能满足需求
```

### 特点

基于 "互联网**开放的纯密码** sgk" 分析统计出来：字符，数字，字母，短字符串 出现的次数，生成一个公共元素概率“顺序表”。

<img src=prob.jpg>

如果元素文件中的元素在表中，则生成密码的概率值加上相应的概率，最后取平均值。生成的字典如下，为csv格式，方便查看和排序，注意，如果没有元素在概率表里，说明是人为指定，概率则为1，请自行取舍。如果你有比较好的裤子，自己统计分析设置概率表，可以生成更具人性化的字典。

<img src=output.jpg>
